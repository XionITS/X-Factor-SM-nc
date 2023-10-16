from django.http import HttpResponse
import math
import json
import operator
from django.shortcuts import render
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
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    context = {'menu_list': menu.data}
    return render(request, 'user_management.html', context)

@csrf_exempt
def um_user(request):
    user = Xfactor_Xuser.objects.all()
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
    x_id = request.POST.get("x_id")
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=x_id)
    auth_list= XuserAuthSerializer(xuser_auths, many=True).data
    response = {'auth_list': auth_list}
    return JsonResponse(response)

@csrf_exempt
def group_auth(request):
    xgroup_name = request.POST.get("xgroup_name")
    xfactor_auth = Xfactor_Auth.objects.all()
    auth_list= AuthSerializer(xfactor_auth, many=True).data
    response = {'auth_list': auth_list}
    return JsonResponse(response)

@csrf_exempt
def save_user_auth(request):
    x_ids_str = request.POST.get('x_id')  # 쉼표로 구분된 문자열을 얻음
    print(x_ids_str)
    #x_ids = x_ids_str.split(',')
    auth_infos = request.POST.get('auth_info')
    auth_infos = json.loads(auth_infos)
    try:
        for item in auth_infos:
            auth_id = item["auth_id"]
            auth_use = item["auth_use"]
            record = get_object_or_404(Xfactor_Xuser_Auth, xfactor_xuser_id=x_ids_str, xfactor_auth__auth_id=auth_id)
            record.auth_use = auth_use
            record.save()
            #print(x_ids_str)
            # auth, created = Xfactor_Xuser_Auth.objects.update_or_create(
            #     xfactor_auth__auth_id=auth_id, xfactor_xuser=x_ids_str, defaults = {"auth_use": auth_use},  # 업데이트할 필드와 값을 설정합니다.
            # )
            # if created:
            #     #print(f"Created new record for auth_id {auth_id}")
            #     print(x_ids_str)
            # else:
            #     #print(f"Updated record for auth_id {auth_id} with auth_use {auth_use}")
            #     print(x_ids_str)


        function = 'User Auth Change'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'User Auth Change ' + x_ids_str
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
def save_group_auth(request):
    x_ids_str = request.POST.get('x_id_array')  # 쉼표로 구분된 문자열을 얻음
    x_ids = x_ids_str.replace('[', '').replace(']', '').replace('"', '').split(',')
    print(type(x_ids))
    auth_infos = request.POST.get('auth_info')
    auth_infos = json.loads(auth_infos)
    print(auth_infos)
    try:
        for x_id in x_ids:
            for item in auth_infos:
                auth_id = item["auth_id"]
                auth_use = item["auth_use"]
                Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=x_id, xfactor_auth_id=auth_id).update(auth_use=auth_use)

        function = 'Group Auth Change'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'Group Auth Change ' + x_ids_str
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
def create_auth(request):
    xgroup_name = request.POST['xgroup_name']
    xgroup_description = request.POST['xgroup_description']
    xuserIds = json.loads(request.POST['xuserIds'])


    # Computer Group 만들기
    text = ""
    # for index, xuser_id in enumerate(xuserIds):
    #     if index == len(xuser_id) - 1:
    #         text += f'Computer ID matches \\"{xuser_id}\\"'
    #     else:
    #         text += f'Computer ID matches \\"{xuser_id}\\" or '

    #DB넣기
    xgroup_insert = Xfactor_Xuser_Group()
    xgroup_insert.xgroup_name = xgroup_name
    xgroup_insert.xgroup_note = xgroup_description
    xgroup_insert.xuser_id_list = xuserIds
    xgroup_insert.save()
    message_code = "success"

    message = "Group이 생성되었습니다. \n 그룹이름 : " +xgroup_name+""

    function = 'Xuser_Group Create'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    item = 'Xuser_Group Create for the '+ xgroup_name
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

    return JsonResponse({"success":message_code, "message": message})




@csrf_exempt
def um_group(request):
    user = Xfactor_Xuser_Group.objects.all()
    #user = Xfactor_Common.objects.prefetch_related('purchase').filter(user_date__gte=today_collect_date)
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'xgroup_name',
        3: 'xgroup_note',
        4: 'xgroup_list',
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