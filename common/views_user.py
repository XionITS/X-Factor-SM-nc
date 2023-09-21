import datetime

import requests
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import hashlib
import psycopg2
import json

from common.models import Xfactor_Log

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
        x_id = request.POST.get('x_id')
        x_pw = request.POST.get('x_pw')
        re_x_pw = request.POST.get('re_x_pw')
        x_name = request.POST.get('x_name')
        x_email = request.POST.get('x_email')
        x_auth = request.POST.get('x_auth')
        res_data = {}

        RS = createUsers(x_id, x_pw, x_name, x_email, x_auth)
        if RS == "1":
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
                    date = timezone.now()
                    print(date)
                    Xfactor_log = Xfactor_Log(
                        log_func=function,
                        log_item=item,
                        log_result=result,
                        log_user=user,
                        log_date=date
                    )
                    Xfactor_log.save()
                    return redirect('../dashboard')
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
                    return redirect('../dashboard')

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
                return redirect('../dashboard')
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
def createUsers(x_id, x_pw, x_name, x_email, x_auth):
    try:
        hashpassword = hashlib.sha256(x_pw.encode()).hexdigest()
        Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        query = """ 
        INSERT INTO 
            common_xfactor_xuser
            (x_id, x_pw, x_name, x_email, x_auth) 
        VALUES ( 
                '""" + x_id + """',
                '""" + hashpassword + """' ,
                '""" + x_name + """',
                '""" + x_email + """',
                '""" + x_auth + """'
                );
        """
        Cur.execute(query)
        Conn.commit()
        Conn.close()
        a = "1"
        return a
    except:
        print(UserTNM + ' Table connection(Select) Failure')
        a = "0"
        return a


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
