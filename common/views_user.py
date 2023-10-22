import datetime

import requests
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import hashlib
import psycopg2
import json
from django.http import JsonResponse
from urllib.parse import urlencode
from common.models import Xfactor_Log,Xfactor_Xuser

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBHost = SETTING['DB']['DBHost']
DBPort = SETTING['DB']['DBPort']
DBName = SETTING['DB']['DBName']
DBUser = SETTING['DB']['DBUser']
DBPwd = SETTING['DB']['DBPwd']
UserTNM = SETTING['DB']['UserTNM']
Login_Method = SETTING['PROJECT']['LOGIN']
apiUrl = SETTING['API']['apiUrl']
SesstionKeyPath = SETTING['API']['PATH']['SessionKey']


# hi
@csrf_exempt
def signup(request):
    if request.method == "GET":
        return render(request, 'common/signup.html')

    elif request.method == "POST":
        page = request.POST.get('page')
        x_id = request.POST.get('x_id')
        x_pw = request.POST.get('x_pw')
        re_x_pw = request.POST.get('re_x_pw')
        x_name = request.POST.get('x_name')
        x_email = request.POST.get('x_email')
        x_auth = request.POST.get('x_auth')
        res_data = {}

        RS = createUsers(x_id, x_pw, x_name, x_email, x_auth)
        if RS == "1":
            if page == 'um':
                res_data['error'] = "회원가입에 성공하였습니다."
                redirect_url = '../user_management'
                function = 'Add User'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
                item = 'Add user '+ x_id
                result = '성공'
                user = request.session.get('sessionid')
                date = timezone.now()
                Xfactor_log = Xfactor_Log(
                    log_func=function,
                    log_item=item,
                    log_result=result,
                    log_user=user,
                    log_date=date
                )
                Xfactor_log.save()
                AutoAuth(x_id)
                return redirect(redirect_url)
                #return render(request, 'user_management.html', res_data)
            else :
                function = 'Signup User'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
                item = 'Signup user ' + x_id
                result = '성공'
                user = x_id
                date = timezone.now()
                Xfactor_log = Xfactor_Log(
                    log_func=function,
                    log_item=item,
                    log_result=result,
                    log_user=user,
                    log_date=date
                )
                Xfactor_log.save()
                res_data['error'] = "회원가입에 성공하였습니다."
                return render(request, 'common/login.html', res_data)
        else:
            res_data['error'] = "아이디가 존재합니다."
            res_data['x_id'] = x_id
            res_data['x_name'] = x_name
            res_data['x_email'] = x_email
            res_data['x_auth'] = x_auth
            return render(request, 'common/signup.html', res_data)

@csrf_exempt
def login(request):
    if Login_Method == "WEB":
        if request.method == 'GET':
            return render(request, 'common/login.html')

        # POST 방식 요청 -> 사용자가 보내는 데이터와 데이터베이스의 정보 일치여부 확인
        elif request.method == 'POST':
            x_id = request.POST.get('x_id', None)
            x_pw = request.POST.get('x_pw', None)

            # 응답 데이터
            res_data = {}

            # 모든 필드를 채우지 않았을 경우
            if not (x_id and x_pw):
                res_data['error'] = '아이디 또는 비밀번호를 입력해 주세요.'
                return render(request, 'common/login.html', res_data)
            # 모든 필드를 채웠을 경우
            else:
                RS = selectUsers(x_id, x_pw)
                print(RS)
                if RS == None:
                    res_data['error'] = '아이디 또는 비밀번호가 일치하지 않습니다'
                    return render(request, 'common/login.html', res_data)

                else:
                    request.session['sessionid'] = RS[0]
                    request.session['sessionname'] = RS[2]
                    request.session['sessionemail'] = RS[3]
                    function = 'Login'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
                    item = 'admin 계정'
                    result = '성공'
                    user = RS[0]
                    now = timezone.now().replace(microsecond=0)
                    date = now.strftime("%Y-%m-%d %H:%M:%S")
                    print(date)
                    Xfactor_log = Xfactor_Log(
                        log_func=function,
                        log_item=item,
                        log_result=result,
                        log_user=user,
                        log_date=date
                    )
                    Xfactor_log.save()
                    return redirect('../home')
    elif Login_Method == "Tanium":
        if request.method == 'GET':
            returnData = {'Login_Method': Login_Method}
            return render(request, 'common/login.html', returnData)

        elif request.method == 'POST':

            x_id = request.POST.get('x_id', None)
            x_pw = request.POST.get('x_pw', None)

            # 응답 데이터
            res_data = {}

            # 모든 필드를 채우지 않았을 경우
            if not (x_id and x_pw):
                res_data['error'] = '아이디 또는 비밀번호를 입력해 주세요.'
                return render(request, 'common/login.html', res_data)
            # 모든 필드를 채웠을 경우
            else:
                TRS = taniumUsers(x_id, x_pw)
                if TRS == None:
                    res_data['error'] = '아이디 또는 비밀번호가 일치하지 않습니다'
                    return render(request, 'common/login.html', res_data)
                else:
                    request.session['sessionid'] = x_id
                    return redirect('../home')
    if Login_Method == "NANO":
        return redirect('../nano')

@csrf_exempt
def updateform(request):
    try:
        if request.method == "GET":
            # print(request.session.sessionid)
            return render(request, 'common/updateform.html')

        elif request.method == "POST":
            x_id = request.POST.get('x_id')
            x_pw = request.POST.get('x_pw')
            hashpassword = hashlib.sha256(x_pw.encode()).hexdigest()
            Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
            Cur = Conn.cursor()

            query = """
                        select
                            *
                        from
                            """ + UserTNM + """
                        where
                            x_id = '""" + x_id + """'
                        and
                            x_pw = '""" + hashpassword + """'

                    """
            Cur.execute(query)
            RS = Cur.fetchall()
            res_data = {}
            print(RS)
            if RS[0] != None:
                res_data['x_id'] = RS[0][0]
                res_data['x_name'] = RS[0][2]
                res_data['x_email'] = RS[0][3]
                res_data['x_auth'] = RS[0][4]
                # print(res_data)
                return render(request, 'common/update.html', res_data)
    except:
        res_data['error'] = '비밀번호를 다시한번 확인 해 주세요.'
        return render(request, 'common/updateform.html', res_data)

@csrf_exempt
def update(request):
    if request.method == "GET":
        # 404 에러페이지 넣을것
        return render(request, '')

    elif request.method == "POST":
        x_id = request.POST.get('x_id')
        x_pw = request.POST.get('x_pw')
        re_x_pw = request.POST.get('re_x_pw')
        x_name = request.POST.get('x_name')
        x_email = request.POST.get('x_email')
        x_auth = request.POST.get('x_auth')
        res_data = {}
        if not (x_id and x_pw and x_name and x_email and x_auth):
            res_data['x_id'] = x_id
            res_data['x_pw'] = x_pw
            res_data['x_name'] = x_name
            res_data['x_email'] = x_email
            res_data['x_auth'] = x_auth
            res_data['error'] = "모든 값을 입력해야 합니다."
            return render(request, 'common/update.html', res_data)
        if x_pw != re_x_pw:
            res_data['x_id'] = x_id
            res_data['x_pw'] = x_pw
            res_data['x_name'] = x_name
            res_data['x_email'] = x_email
            res_data['x_auth'] = x_auth
            res_data['error'] = '비밀번호가 다릅니다.'
            return render(request, 'common/update.html', res_data)
        else:
            RS = updateUsers(x_id, x_pw, x_name, x_email, x_auth)
            if RS == "1":
                request.session['sessionname'] = x_name
                request.session['sessionemail'] = x_email
                return redirect('../home')
            else:
                res_data['error'] = '회원정보 변경이 실패했습니다.'
                return render(request, 'common/update.html', res_data)

@csrf_exempt
def logout(request):
    if Login_Method == "WEB":
        if 'sessionid' in request.session:

            function = 'Logout'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
            item = 'admin 계정'
            result = '성공'
            user = request.session.get('sessionid')
            date = timezone.now()
            Xfactor_log = Xfactor_Log(
                log_func=function,
                log_item=item,
                log_result=result,
                log_user=user,
                log_date=date
            )
            Xfactor_log.save()
            del (request.session['sessionid'])
            del (request.session['sessionname'])
            del (request.session['sessionemail'])
            return render(request, 'common/login.html')
        else:
            return render(request, 'common/login.html')
    elif Login_Method == "Tanium":
        if request.method == 'GET':
            returnData = {'Login_Method': Login_Method}
            return render(request, 'common/login.html', returnData)
        if 'sessionid' in request.session:
            del (request.session['sessionid'])
            return render(request, 'common/login.html')
        else:
            return render(request, 'common/login.html')

    elif Login_Method == "NANO":
        if 'sessionid' in request.session:
            function = 'Logout'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
            item = 'admin 계정'
            result = '성공'
            user = request.session.get('sessionid')
            date = timezone.now()
            Xfactor_log = Xfactor_Log(
                log_func=function,
                log_item=item,
                log_result=result,
                log_user=user,
                log_date=date
            )
            Xfactor_log.save()

        id_token_hint = request.session.get('sessionidtoken', None)

        # id_token_hint가 None인 경우, 로그아웃 요청을 보낼 수 없으므로 에러 메시지를 출력하고 함수를 종료합니다.
        if id_token_hint is None:
            print("No ID token found in session. Cannot perform logout.")
        else:
            params = {
                'id_token_hint': id_token_hint,
                'post_logout_redirect_uri': 'https://tanium.ncsoft.com/dashboard/'
            }
            # Make a GET request to the logout endpoint
            response = requests.get('https://sso.nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/logout', params=params)

            # Check the response
            if response.status_code == 200:
                print('Logout successful')
                request.session.pop('sessionid', None)
                request.session.pop('sessionname', None)
                request.session.pop('sessionemail', None)
                request.session.pop('sessionidtoken', None)
            else:
                print('Logout failed')
            # return redirect("../login")
            # return redirect("https://sso.nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/logout?id_token_hint=tanium-dashboard&
            # post_logout_redirect_uri=https://tanium.ncsoft.com/dashboard/")

@csrf_exempt
def selectUsers(x_id, x_pw):
    try:
        hashpassword = hashlib.sha256(x_pw.encode()).hexdigest()
        # print(hashpassword)

        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()

        query = """
            select 
                *
            from
                """ + UserTNM + """
            where
                x_id = '""" + x_id + """'
            and
                x_pw = '""" + hashpassword + """'
                
            """

        Cur.execute(query)
        RS = Cur.fetchone()
        # print(RS)
        return RS
    except:
        print(UserTNM + ' Table connection(Select) Failure')


@csrf_exempt
def selectUsers_nano(x_id):
    try:
        #hashpassword = hashlib.sha256(x_pw.encode()).hexdigest()
        # print(hashpassword)

        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()

        query = """
            select 
                *
            from
                """ + UserTNM + """
            where
                x_id = '""" + x_id + """'


            """

        Cur.execute(query)
        RS = Cur.fetchone()
        # print(RS)
        return RS
    except:
        print(UserTNM + ' Table connection(Select) Failure')

@csrf_exempt
def createUsers(x_id, x_pw, x_name, x_email, x_auth):
    try:
        hashpassword = hashlib.sha256(x_pw.encode()).hexdigest()
        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        query = """ 
        INSERT INTO 
            common_xfactor_xuser
            (x_id, x_pw, x_name, x_email, x_auth, create_date) 
        VALUES ( 
                '""" + x_id + """',
                '""" + hashpassword + """' ,
                '""" + x_name + """',
                '""" + x_email + """',
                '""" + x_auth + """',
                now()
                );
        """
        Cur.execute(query)
        Conn.commit()
        Conn.close()
        # Auth 자동생성
        RS = AutoAuth(x_id)
        if RS == "1":
            a = "1"
            return a
    except:
        print(UserTNM + ' Table connection(Select) Failure')
        a = "0"
        return a

@csrf_exempt
def AutoAuth(x_id):
    Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()
    query = """ 
           INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'HS_asset', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'VER_asset', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'UP_asset', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES( 'false', 'PUR_asset', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'SEC_asset', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'SEC_asset_list', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'Asset', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'History', '""" + x_id + """');

            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'settings', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_report', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_daily', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_all_asset', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_longago', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_locate', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_office', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_month', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_win_ver', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_win_update', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_win_hotfix', '""" + x_id + """');
            
            INSERT INTO public.common_xfactor_xuser_auth
            (auth_use, xfactor_auth_id, xfactor_xuser_id)
            VALUES('false', 'dash_tanium', '""" + x_id + """');            
           """
    Cur.execute(query)
    Conn.commit()
    Conn.close()
    a= '1'
    return a



@csrf_exempt
def DeleteAuth(id):
    Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()
    query = """ 
        DELETE FROM public.common_xfactor_xgroup_auth
        WHERE xgroup_id = '""" + id +"""';
       """
    Cur.execute(query)
    Conn.commit()
    Conn.close()


@csrf_exempt
def Group_AutoAuth(xuser_id_list,id):
    Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()
    for xgroup_id in xuser_id_list:
        query = """ 
               INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'HS_asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'VER_asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'UP_asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES( 'false', 'PUR_asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'SEC_asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'SEC_asset_list', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'Asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'History', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'settings', '""" + xgroup_id + """', '""" + id + """');
                
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_report', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_daily', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_all_asset', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_longago', '""" + xgroup_id + """', '""" + id + """');
                
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_locate', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_office', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_month', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_win_ver', '""" + xgroup_id + """', '""" + id + """');
                
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_win_update', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_win_hotfix', '""" + xgroup_id + """', '""" + id + """');
    
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_tanium', '""" + xgroup_id + """', '""" + id + """');

               """
        Cur.execute(query)
        Conn.commit()
    Conn.close()
    a= '1'
    return a


@csrf_exempt
def Group_modifyAuth(xuser_id_list, id, auths):
    Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()

    print(xuser_id_list)
    for auth in auths:
        auth_use = auth['auth_use']
        xfactor_auth_id = auth['auth_id']
        for xgroup_id in xuser_id_list:
            query = """ 
               INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('""" + auth_use + """','""" + xfactor_auth_id + """', '""" + xgroup_id + """', '""" + id + """');           
               """
            Cur.execute(query)
            Conn.commit()
    Conn.close()
    a = '1'
    return a




@csrf_exempt
def updateUsers(x_id, x_pw, x_name, x_email, x_auth):
    try:
        hashpassword = hashlib.sha256(x_pw.encode()).hexdigest()
        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        query = """ 
        UPDATE
            common_xfactor_xuser 
        SET
            x_pw= '""" + hashpassword + """',
            x_name= '""" + x_name + """',
            x_email= '""" + x_email + """',
            x_auth= '""" + x_auth + """'
        WHERE
            x_id = '""" + x_id + """';
        """
        # print(query)
        Cur.execute(query)
        Conn.commit()
        Conn.close()
        a = "1"
        return a
    except:
        print(UserTNM + ' Table connection(Update) Failure')
        a = "0"
        return a

@csrf_exempt
def taniumUsers(x_id, x_pw):
    try:
        path = SesstionKeyPath
        urls = apiUrl + path
        headers = '{"username" : "' + x_id + '","domain":"",  "password":"' + x_pw + '"}'
        response = requests.post(urls, data=headers, verify=False)
        code = response.status_code
        if code == 200:
            a = response.json()
            sessionKey = a['data']['session']
            returnList = sessionKey
            return returnList
        elif code == 403:
            print()

    except ConnectionError as e:
        print(e)

@csrf_exempt
def delete(request):
    x_ids_str = request.POST.get('x_id')  # 쉼표로 구분된 문자열을 얻음
    x_ids = x_ids_str.split(',')
    try:
        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        for x_id in x_ids:
            query = """ 
                    DELETE FROM
                        common_xfactor_xuser_auth
                    WHERE
                        xfactor_xuser_id = %s;
                    """
            Cur.execute(query, (x_id,))
            query = """ 
                    DELETE FROM
                        common_xfactor_xuser
                    WHERE
                        x_id = %s;
                    """
            Cur.execute(query, (x_id,))
        Conn.commit()
        Conn.close()

        function = 'User Delete'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'Delete user ' + x_id
        result = '성공'
        user = request.session.get('sessionid')
        now = datetime.now().replace(microsecond=0)
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        print(date)
        Xfactor_log = Xfactor_Log(
            log_func=function,
            log_item=item,
            log_result=result,
            log_user=user,
            log_date=date
        )
        Xfactor_log.save()

        return JsonResponse({'result': 'success'}, status=200)  # 성공적으로 삭제되었을 때 응답
    except Exception as e:
        print(str(e))  # 에러 메시지 출력 (디버깅 용)
        return JsonResponse({'result': 'failure'}, status=400)  # 삭제 중 오류가 발생했을 때 응답

@csrf_exempt
def group_delete(request):
    xgroup_ids_str = request.POST.get('group_ids')  # 쉼표로 구분된 문자열을 얻음
    xgroup_ids = xgroup_ids_str.split(',')

    try:
        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        for xgroup_id in xgroup_ids:
            query = """ 
                    DELETE FROM
                        common_xfactor_xuser_group
                    WHERE
                        id = %s;
                    """
            Cur.execute(query, (xgroup_id,))
            query = """ 
                    DELETE FROM
                        common_xfactor_xgroup_auth
                    WHERE
                        xgroup_id = %s;
                    """
            Cur.execute(query, (xgroup_id,))
        Conn.commit()
        Conn.close()

        function = 'Group Delete'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'Delete group ' + xgroup_id
        result = '성공'
        user = request.session.get('sessionid')
        now = datetime.now().replace(microsecond=0)
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        print(date)
        Xfactor_log = Xfactor_Log(
            log_func=function,
            log_item=item,
            log_result=result,
            log_user=user,
            log_date=date
        )
        Xfactor_log.save()

        return JsonResponse({'result': 'success'}, status=200)  # 성공적으로 삭제되었을 때 응답
    except Exception as e:
        print(str(e))  # 에러 메시지 출력 (디버깅 용)
        return JsonResponse({'result': 'failure'}, status=400)  # 삭제 중 오류가 발생했을 때 응답


def nano(request):
    auth_url = "https://sso.nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/auth"
    client_id = "tanium-dashboard"
    redirect_uri = "https://tanium.ncsoft.com/dashboard/"

    # 사용자를 인증 페이지로 리디렉션합니다.
    return redirect(f"{auth_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid")


def nano_user(request):
    code = request.GET.get('code')
    print(code)
    access_token, id_token = exchange_code_for_token(code)
    print(access_token)
    print(id_token)
    userinfo_url = "https://sso.nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(userinfo_url, headers=headers)
    userinfo_data = response.json()
    sub = userinfo_data.get("sub")
    name = userinfo_data.get("display_name").split("(")[0]
    dept = userinfo_data.get("display_department")
    email = userinfo_data.get("email")
    print("User Sub:", sub)
    
    #유저 체크
    RS_user = selectUsers_nano(sub)
    if RS_user==None:
        RS = createUsers(sub, sub, name, email, dept)
        # xuser_instance = Xfactor_Xuser(
        #     x_id=sub,
        #     x_email=email,
        # )
        # xuser_instance.save()
    else :
        print("생성되어 있는 ID입니다.")
    request.session['sessionid']=sub
    request.session['sessionname']=name
    request.session['sessionemail']=email
    request.session['sessionidtoken']=id_token
    return redirect('../home')


def exchange_code_for_token(code):
    token_url = "https://sso.nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/token"
    client_id = "tanium-dashboard"
    client_secret = "BzKFaj19XgtFfXuA3TUYKVACfEeANqga"  # 클라이언트 시크릿 키

    # 토큰 요청 파라미터 설정
    token_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://tanium.ncsoft.com/dashboard/",
        "client_id": client_id,
        "client_secret": client_secret
    }
    token_payload_encoded = urlencode(token_payload)
    # 토큰 요청 보내기
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"  # 헤더에 Content-Type 설정
    }
    response = requests.post(token_url, data=token_payload_encoded, headers=headers)

    # 토큰 요청의 응답을 확인합니다.
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        id_token = token_data["id_token"]
        # id_token = token_data.get("id_token")
        return access_token, id_token
    else:
        return None