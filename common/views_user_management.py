import ast

from django.core.cache import cache
from django.http import HttpResponse
import math
import json
import operator
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
import pytz
import psycopg2
from django.shortcuts import get_object_or_404
from common.views_user import Group_AutoAuth, DeleteAuth, Group_modifyAuth

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
DBSettingTime = SETTING['DB']['DBSelectTime']

today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)


@csrf_exempt
def um(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../home/')
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    context = {'menu_list': unique_items}
    return render(request, 'user_management.html', context)

@csrf_exempt
def um_user(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    user = Xfactor_Xuser.objects.values('x_id', 'x_name', 'x_email', 'x_auth', 'create_date')
    #user = Xfactor_Common.objects.prefetch_related('purchase').filter(user_date__gte=today_collect_date)
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'x_id',
        3: 'x_name',
        4: 'x_email',
        5: 'x_auth',
        # Add mappings for other columns here
    }

    order_column = order_column_map.get(order_column_index, 'create_date')
    if order_column_dir == 'desc':
        user = user.order_by(order_column)
    else:
        user = user.order_by('-' + order_column)

    # Get start and length parameters from DataTables AJAX request
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))  # Default to 10 items per page

    # Paginate the queryset
    paginator = Paginator(user, length)
    page_number = (start // length) + 1

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Serialize the paginated data

    user_list = XuserSerializer(page, many=True).data
    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

@csrf_exempt
def user_auth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    x_id = request.POST.get("x_id")
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=x_id)
    auth_list= XuserAuthSerializer(xuser_auths, many=True).data
    response = {'auth_list': auth_list}
    return JsonResponse(response)

@csrf_exempt
def group_auth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    id = request.POST.get("id")
    xgroup_auth = Xfactor_Xgroup_Auth.objects.filter(xgroup_id=id).distinct('auth_use', 'xfactor_auth_id', 'xgroup_id')
    auth_list = XgroupAuthSerializer(xgroup_auth, many=True).data
    #auth_list= XgroupAuthSerializer(xgroup_auth, many=True).data
    response = {'auth_list': auth_list}
    return JsonResponse(response)

# @receiver(pre_save, sender=Xfactor_Xuser_Auth)
# def pre_save_handler(sender, instance, **kwargs):
#     if instance.pk:
#         original = Xfactor_Xuser_Auth.objects.get(pk=instance.pk)
#         instance._auth_use_origin = original.auth_use
#         instance._xfactor_auth_id_origin = original.xfactor_auth_id
#
# @receiver(post_save, sender=Xfactor_Xuser_Auth)
# def post_save_handler(sender, instance, created, **kwargs):
#     if not created:
#         if hasattr(instance, '_auth_use_origin') and instance._auth_use_origin != instance.auth_use:
#             auth_value = Xfactor_Auth.objects.filter(auth_id=instance.xfactor_auth_id).values('auth_name')[0]['auth_name']
#             cache.set(instance.xfactor_auth_id, f'[{auth_value}] - {instance._auth_use_origin} 에서 {instance.auth_use}로 변경', 3)
#             # cache.set(f'{instance.xfactor_auth_id}_origin', instance._auth_use_origin, 1)
#             # cache.set(f'{instance.xfactor_auth_id}_current', instance.auth_use, 1)
#         if hasattr(instance, '_xfactor_auth_id_origin') and instance._xfactor_auth_id_origin != instance.xfactor_auth_id:
#             print(f'xfactor_auth_id field was updated from {instance._xfactor_auth_id_origin} to {instance.xfactor_auth_id}')

@csrf_exempt
def save_user_auth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    x_ids_str = request.POST.get('x_id')  # 쉼표로 구분된 문자열을 얻음
    #x_ids = x_ids_str.split(',')
    auth_infos = request.POST.get('auth_info')
    auth_infos = json.loads(auth_infos)
    # print(auth_infos)
    a = []
    try:
        for item in auth_infos:
            auth_id = item["auth_id"]
            auth_use = item["auth_use"]
            # Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=x_ids_str, xfactor_auth__auth_id=auth_id).update(auth_use=auth_use)
            record = get_object_or_404(Xfactor_Xuser_Auth, xfactor_xuser_id=x_ids_str, xfactor_auth__auth_id=auth_id)
            record.auth_use = auth_use
            record.save()

            # if cache.get(record.xfactor_auth_id) != None:
            #     # for i in range(len(list(cache.get('value_list')))):
            #     a.append(cache.get(record.xfactor_auth_id))


        # print(auth_use_current)
        function = 'User Auth'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'Change user auth - [' + x_ids_str + ']'
        result = '성공'
        # result = '\n'.join(a)
        user = request.session.get('sessionid')
        now = datetime.now().replace(microsecond=0)
        date = now.strftime("%Y-%m-%d %H:%M:%S")
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
def save_group_auth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    xgroup_id = request.POST.get('id')
    x_ids_str = request.POST.get('x_id_array')  # 쉼표로 구분된 문자열을 얻음
    x_ids = x_ids_str.replace('[', '').replace(']', '').replace('"', '').split(',')

    auth_infos = request.POST.get('auth_info')
    auth_infos = json.loads(auth_infos)
    try:
        for x_id in x_ids:
            for item in auth_infos:
                auth_id = item["auth_id"]
                auth_use = item["auth_use"]
                Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=x_id, xfactor_auth_id=auth_id, xgroup_id=xgroup_id).update(auth_use=auth_use)

        function = 'Group Auth Change'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'Group Auth Change ' + x_ids_str
        result = '성공'
        user = request.session.get('sessionid')
        now = datetime.now().replace(microsecond=0)
        date = now.strftime("%Y-%m-%d %H:%M:%S")

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
def create_auth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    xgroup_name = request.POST['xgroup_name']
    xgroup_description = request.POST['xgroup_description']
    xgroup_name = escape(xgroup_name)
    xgroup_description = escape(xgroup_description)
    xuserIds = json.loads(request.POST['xuserIds'])

    if not xuserIds:
        xuserIds = ['']

    #DB넣기
    xgroup_insert = Xfactor_Xuser_Group()
    xgroup_insert.xgroup_name = xgroup_name
    xgroup_insert.xgroup_note = xgroup_description
    xgroup_insert.xuser_id_list = xuserIds
    xgroup_insert.save()
    id = xgroup_insert.pk

    RS = Group_AutoAuth(xuserIds,str(id))


    message_code = "success"

    message = "Group이 생성되었습니다. \n 그룹이름 : " +xgroup_name+""

    function = 'Xuser_Group Create'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    item = 'Xuser_Group Create for the '+ xgroup_name
    result = f"추가된 유저: {', '.join(xuserIds)}"
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

    return JsonResponse({"success":message_code, "message": message})

@csrf_exempt
def alter_auth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    xgroup_name = request.POST['xgroup_name']
    id = request.POST['id']
    xgroup_description = request.POST['xgroup_description']
    xgroup_name = escape(xgroup_name)
    xgroup_description = escape(xgroup_description)
    xuserIds = json.loads(request.POST['xuserIds'])

    xgroup_auth = Xfactor_Xgroup_Auth.objects.filter(xgroup_id=id).distinct('auth_use','xfactor_auth_id','xgroup_id')
    #print(xgroup_auth)
    #first_set = xgroup_auth[0:9]
    #first_set = list(set(xgroup_auth))
    auth_list = XgroupAuthSerializer(xgroup_auth, many=True).data
    auth = []
    for item in auth_list:
        auth_data = item['xfactor_auth']  # 'xfactor_auth' 키의 값을 가져옴
        auth_id = auth_data['auth_id']  # 'auth_id' 키의 값을 가져옴
        auth_use = item['auth_use']  # 'auth_user' 키의 값을 가져옴
        # auth_id와 auth_user만 따로 저장하거나 활용
        auth.append({'auth_id': auth_id, 'auth_use': auth_use})

    default_user_list = Xfactor_Xuser_Group.objects.get(id=id).xuser_id_list
    default_user_list = ast.literal_eval(default_user_list)

    # 삭제된 유저 확인
    deleted_user_ids = list(set(default_user_list) - set(xuserIds))
    # 추가된 유저 확인
    added_user_ids = list(set(xuserIds) - set(default_user_list))
    log_result = ''
    if added_user_ids:
        log_result += f"추가된 유저 : {', '.join(added_user_ids)}\n\n"
    if deleted_user_ids:
        log_result += f"삭제된 유저 : {', '.join(deleted_user_ids)}"

    #auth_id =
    # Computer Group 만들기
    text = ""
    # for index, xuser_id in enumerate(xuserIds):
    #     if index == len(xuser_id) - 1:
    #         text += f'Computer ID matches \\"{xuser_id}\\"'
    #     else:
    #         text += f'Computer ID matches \\"{xuser_id}\\" or '

    #DB넣기
    xgroup_update = Xfactor_Xuser_Group.objects.get(pk=id)
    xgroup_update.id = id
    xgroup_update.xgroup_name = xgroup_name
    xgroup_update.xgroup_note = xgroup_description
    xgroup_update.xuser_id_list = xuserIds
    xgroup_update.save()

    DeleteAuth(str(id))
    RS = Group_modifyAuth(xuserIds, str(id), auth)

    message_code = "success"

    message = "Group이 수정되었습니다. \n 그룹이름 : " +xgroup_name+""
    if deleted_user_ids == [] and added_user_ids == []:
        return JsonResponse({"success":message_code, "message": message})

    function = 'Xuser_Group Modify'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    item = 'Xuser_Group Modify for the '+ xgroup_name
    user = request.session.get('sessionid')
    date = timezone.now()
    Xfactor_log = Xfactor_Log(
        log_func=function,
        log_item=item,
        log_result=log_result,
        log_user=user,
        log_date=date
    )
    Xfactor_log.save()

    return JsonResponse({"success":message_code, "message": message})




@csrf_exempt
def um_group(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    user = Xfactor_Xuser_Group.objects.all()
    #user = Xfactor_Common.objects.prefetch_related('purchase').filter(user_date__gte=today_collect_date)
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'xgroup_name',
        3: 'xgroup_note',
        5: 'create_date',
        # Add mappings for other columns here
    }

    order_column = order_column_map.get(order_column_index, 'create_date')
    if order_column_dir == 'desc':
        user = user.order_by(order_column)
    else:
        user = user.order_by('-' + order_column)

    # Get start and length parameters from DataTables AJAX request
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))  # Default to 10 items per page

    # Paginate the queryset
    paginator = Paginator(user, length)
    page_number = (start // length) + 1

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Serialize the paginated data

    user_list = XgroupSerializer(page, many=True).data
    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

@csrf_exempt
def search_box(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    if request.method == "POST":
        search_text = request.POST.get('searchText', None)
        user_data =Xfactor_Xuser.objects.filter(x_id__icontains=search_text).values('x_id')
        # user_data = XfactorServiceserializer(user, many=True).data
        return JsonResponse({'data': list(user_data)})



@csrf_exempt
def user_list(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    user = Xfactor_Xuser.objects.all()

    user_list = XuserSerializer(user, many=True).data
    # Prepare the response
    response = {'data': user_list}

    return JsonResponse(response)

@csrf_exempt
def db_list(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    user = Xfactor_ncdb.objects.exclude(userName__isnull=True).exclude(email__isnull=True)

    db_list = NcdbSerializer(user, many=True).data
    # Prepare the response
    response = { 'data': db_list}

    return JsonResponse(response)



#user_add
#createUsers
# @csrf_exempt
#
# def insertAuth(x_id, x_pw, x_name, x_email, x_auth):
#     try:
#         Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
#         Cur = Conn.cursor()
#         query = """
#         INSERT INTO
#             common_xfactor_xuser
#             (x_id, x_pw, x_name, x_email, x_auth, create_date)
#         VALUES (
#                 '""" + x_id + """',
#                 '""" + x_id + """' ,
#                 '""" + x_name + """',
#                 '""" + x_email + """',
#                 '""" + x_auth + """',
#                 now()
#                 );
#         """
#         Cur.execute(query)
#         Conn.commit()
#         Conn.close()
#         # Auth 자동생성
#         RS = AutoAuth(x_id)
#         if RS == "1":
#             a = "1"
#             return a
#     except:
#         print(UserTNM + ' Table connection(Select) Failure')
#         a = "0"
#         return a


@csrf_exempt
def insertAuth(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='settings', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='settings', auth_use='false')
    if not user_auth and not group_auth:
        return redirect('../../home/')

    user = Xfactor_Xuser.objects.all()


    Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()
    for item in user:
        query = """ 
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_report', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_daily', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_all_asset', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_longago', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_locate', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_office', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_month', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_win_ver', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_win_update', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_win_hotfix', '""" + item.x_id + """');
    
                INSERT INTO public.common_xfactor_xuser_auth
                (auth_use, xfactor_auth_id, xfactor_xuser_id)
                VALUES('true', 'dash_tanium', '""" + item.x_id + """');            
               """
        Cur.execute(query)
        Conn.commit()
    Conn.close()

    group = Xfactor_Xuser_Group.objects.all()


    Conn = psycopg2.connect('host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()
    for item in group:
        id = item.id

        query = """
                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_report', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_daily', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_all_asset', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_longago', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_locate', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_office', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_month', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_win_ver', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_win_update', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_win_hotfix', '1', '""" + str(id) + """');

                INSERT INTO public.common_xfactor_xgroup_auth
                (auth_use, xfactor_auth_id, xfactor_xgroup, xgroup_id)
                VALUES('false', 'dash_tanium', '1', '""" + str(id) + """');
                   """
        Cur.execute(query)
        Conn.commit()
    Conn.close()


    return 1