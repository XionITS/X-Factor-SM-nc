from django.http import HttpResponse
import math
import json
import operator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q , F , ExpressionWrapper, fields
from django.db.models.functions import Lower
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
import pytz
from common.custom_sort_key import custom_sort_key as cus_sort
with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']


@csrf_exempt
def pur_asset(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                 xfactor_auth_id='PUR_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='PUR_asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../home/')
    #메뉴
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    print(unique_items)
    # #테이블아래 자산현황
    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)


    asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')[:5]
    total_asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(total_asset.values_list('item_count', flat=True))

    context = {'menu_list' : unique_items}
    #context = {'menu_list' : menu.data, 'asset' : asset, 'total_item_count' : total_item_count}
    return render(request, 'pur_asset.html', context)

@csrf_exempt
def pur_asset_paginghw(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='PUR_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='PUR_asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    start_of_today1 = now.strftime('%Y-%m-%d %H')
    start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
    start_of_today = timezone.make_aware(start_of_today2)
    start_of_day = start_of_today - timedelta(days=7)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    seven_days_ago = timezone.now() - timedelta(days=7)

    filter_column =request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)
    user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
    if filter_text and filter_column:
        if filter_column == "user_date":
            user = user
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Common.objects.prefetch_related('purchase').filter(user_date__gte=today_collect_date)
            user = user.filter(query)
            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(chw_cpu__icontains=term) |
                                                   Q(hw_mb__icontains=term) |
                                                   Q(hw_ram__icontains=term) |
                                                   Q(hw_disk__icontains=term) |
                                                   Q(chw_gpu__icontains=term) |
                                                   Q(first_network__icontains=term) |
                                                   Q(mem_use__icontains=term) |
                                                   Q(disk_use__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(chw_cpu__icontains=term) |
                                                   Q(hw_mb__icontains=term) |
                                                   Q(hw_ram__icontains=term) |
                                                   Q(hw_disk__icontains=term) |
                                                   Q(chw_gpu__icontains=term) |
                                                   Q(first_network__icontains=term) |
                                                   Q(mem_use__icontains=term) |
                                                   Q(disk_use__icontains=term)
                                                   for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                             Q(logged_name_id__deptName__icontains=filter_value) |
                             Q(logged_name_id__userName__icontains=filter_value) |
                             Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(hw_cpu__icontains=filter_value) |
                             Q(hw_mb__icontains=filter_value) |
                             Q(hw_ram__icontains=filter_value) |
                             Q(hw_disk__icontains=filter_value) |
                             Q(hw_gpu__icontains=filter_value) |
                             Q(first_network__icontains=filter_value) |
                             Q(mem_use__icontains=filter_value) |
                             Q(disk_use__icontains=filter_value))
                user = user.filter(query)
    else:
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(chw_cpu__icontains=term) |
                                               Q(hw_mb__icontains=term) |
                                               Q(hw_ram__icontains=term) |
                                               Q(hw_disk__icontains=term) |
                                               Q(chw_gpu__icontains=term) |
                                               Q(first_network__icontains=term) |
                                               Q(mem_use__icontains=term) |
                                               Q(disk_use__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(chw_cpu__icontains=term) |
                                               Q(hw_mb__icontains=term) |
                                               Q(hw_ram__icontains=term) |
                                               Q(hw_disk__icontains=term) |
                                               Q(chw_gpu__icontains=term) |
                                               Q(first_network__icontains=term) |
                                               Q(mem_use__icontains=term) |
                                               Q(disk_use__icontains=term)
                                               for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(logged_name_id__deptName__icontains=filter_value) |
                         Q(logged_name_id__userName__icontains=filter_value) |
                         Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hw_cpu__icontains=filter_value) |
                         Q(hw_mb__icontains=filter_value) |
                         Q(hw_ram__icontains=filter_value) |
                         Q(hw_disk__icontains=filter_value) |
                         Q(hw_gpu__icontains=filter_value) |
                         Q(first_network__icontains=filter_value) |
                         Q(mem_use__icontains=filter_value) |
                         Q(disk_use__icontains=filter_value))
            user = user.filter(query)


    # user = user.exclude(ip_address='unconfirmed')
    # user = user.exclude(hw_list='unconfirmed')
    # user = user.exclude(os_total='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'chassistype',
        3: 'logged_name_id__deptName',
        4: 'logged_name_id__userName',
        5: 'logged_name_id__userId',
        6: 'computer_name',
        7: 'ip_address',
        8: 'first_network',
        9: 'mem_use',
        10: 'disk_use',
        12: 'user_date',
        13: 'memo',
        # Add mappings for other columns here
    }

    order_column = order_column_map.get(order_column_index, 'computer_name')
    if order_column == 'first_network':

        for a in user:
            try:
                date_strings = a.first_network
                date_objects = datetime.strptime(date_strings, '%m/%d/%Y')
                latest_date_formatted = date_objects.strftime('%Y-%m-%d')
                a.latest_first_network = latest_date_formatted  # 새로운 필드 생성
            except ValueError:
                a.latest_first_network=a.first_network
                continue

        # user를 latest_hotfix_date 필드를 기준으로 정렬
        if order_column_dir == 'asc':
            user = sorted(user, key=lambda x: x.latest_first_network or '0000-00-00')
        else:
            user = sorted(user, key=lambda x: x.latest_first_network or '9999-99-99', reverse=True)


    else:
        if order_column_dir == 'asc':
            user = user.order_by(order_column, '-computer_id')
        else:
            user = user.order_by('-' + order_column, 'computer_id')
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

    user_list = Commonserializer2(page, many=True).data


    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


@csrf_exempt
def pur_asset_pagingsw(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='PUR_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='PUR_asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    start_of_today1 = now.strftime('%Y-%m-%d %H')
    start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
    start_of_today = timezone.make_aware(start_of_today2)
    start_of_day = start_of_today - timedelta(days=7)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    seven_days_ago = timezone.now() - timedelta(days=7)
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)

    if filter_text and filter_column:
        if filter_column == "user_date":
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            #filter_column = 'computer__' + filter_column
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            #print(user)
            # service = Xfactor_Service.objects.filter(computer=user.computer_id)
            # print(service.essential1)
            user = user.filter(query)
            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(sw_list__icontains=term) |
                                                   Q(sw_ver_list__icontains=term) |
                                                   Q(sw_install__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                  Q(computer_name__icontains=term) |
                                                  Q(ip_address__icontains=term) |
                                                  Q(sw_list__icontains=term) |
                                                  Q(sw_ver_list__icontains=term) |
                                                  Q(sw_install__icontains=term) |
                                                  Q(memo__icontains=term)
                                                  for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                             Q(logged_name_id__deptName__icontains=filter_value) |
                             Q(logged_name_id__userName__icontains=filter_value) |
                             Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(sw_list__icontains=filter_value) |
                             Q(sw_ver_list__icontains=filter_value) |
                             Q(sw_install__icontains=filter_value) |
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        #user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

        # print(user.values_list('computer_id', flat=True))
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(sw_ver_list__icontains=term) |
                                               Q(sw_install__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(sw_list__icontains=term) |
                                              Q(sw_ver_list__icontains=term) |
                                              Q(sw_install__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(logged_name_id__deptName__icontains=filter_value) |
                         Q(logged_name_id__userName__icontains=filter_value) |
                         Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(sw_list__icontains=filter_value) |
                         Q(sw_ver_list__icontains=filter_value) |
                         Q(sw_install__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)

    # user = user.exclude(ip_address='unconfirmed')
    # user = user.exclude(os_total='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'chassistype',
        3: 'logged_name_id__deptName',
        4: 'logged_name_id__userName',
        5: 'logged_name_id__userId',
        6: 'computer_name',
        7: 'ip_address',
        12: 'user_date',
        13: 'memo',
        # Add mappings for other columns here
    }
    #order_column = order_column_map.get(order_column_index, 'computer_name')
    #if order_column_dir == 'asc':
    #    user = sorted(user, key=lambda x: cus_sort(x, order_column))
        #user = user.order_by(order_column, '-computer_id')
    #else:
    #    user = sorted(user, key=lambda x: cus_sort(x, order_column), reverse=True)
    order_column = order_column_map.get(order_column_index, 'computer_name')
    if order_column_dir == 'asc':
        user = user.order_by(order_column, '-computer_id')
    else:
        user = user.order_by('-' + order_column, 'computer_id')
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
    #user_list = LimitedCommonSerializer(page, many=True).data
    #user_list = CommonSerializer(page, many=True).data
    user_list = Commonserializer2(page, many=True).data

    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

@csrf_exempt
def hw_pur_asset_select_all(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='PUR_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='PUR_asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    start_of_today1 = now.strftime('%Y-%m-%d %H')
    start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
    start_of_today = timezone.make_aware(start_of_today2)
    start_of_day = start_of_today - timedelta(days=7)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    seven_days_ago = timezone.now() - timedelta(days=7)

    filter_column =request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)
    user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
    if filter_text and filter_column:
        if filter_column == "user_date":
            user = user
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Common.objects.prefetch_related('purchase').filter(user_date__gte=today_collect_date)
            user = user.filter(query)
            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(chw_cpu__icontains=term) |
                                                   Q(hw_mb__icontains=term) |
                                                   Q(hw_ram__icontains=term) |
                                                   Q(hw_disk__icontains=term) |
                                                   Q(chw_gpu__icontains=term) |
                                                   Q(first_network__icontains=term) |
                                                   Q(mem_use__icontains=term) |
                                                   Q(disk_use__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(chw_cpu__icontains=term) |
                                                   Q(hw_mb__icontains=term) |
                                                   Q(hw_ram__icontains=term) |
                                                   Q(hw_disk__icontains=term) |
                                                   Q(chw_gpu__icontains=term) |
                                                   Q(first_network__icontains=term) |
                                                   Q(mem_use__icontains=term) |
                                                   Q(disk_use__icontains=term)
                                                   for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                             Q(logged_name_id__deptName__icontains=filter_value) |
                             Q(logged_name_id__userName__icontains=filter_value) |
                             Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(hw_cpu__icontains=filter_value) |
                             Q(hw_mb__icontains=filter_value) |
                             Q(hw_ram__icontains=filter_value) |
                             Q(hw_disk__icontains=filter_value) |
                             Q(hw_gpu__icontains=filter_value) |
                             Q(first_network__icontains=filter_value) |
                             Q(mem_use__icontains=filter_value) |
                             Q(disk_use__icontains=filter_value))
                user = user.filter(query)
    else:
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(chw_cpu__icontains=term) |
                                               Q(hw_mb__icontains=term) |
                                               Q(hw_ram__icontains=term) |
                                               Q(hw_disk__icontains=term) |
                                               Q(chw_gpu__icontains=term) |
                                               Q(first_network__icontains=term) |
                                               Q(mem_use__icontains=term) |
                                               Q(disk_use__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(chw_cpu__icontains=term) |
                                               Q(hw_mb__icontains=term) |
                                               Q(hw_ram__icontains=term) |
                                               Q(hw_disk__icontains=term) |
                                               Q(chw_gpu__icontains=term) |
                                               Q(first_network__icontains=term) |
                                               Q(mem_use__icontains=term) |
                                               Q(disk_use__icontains=term)
                                               for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(logged_name_id__deptName__icontains=filter_value) |
                         Q(logged_name_id__userName__icontains=filter_value) |
                         Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hw_cpu__icontains=filter_value) |
                         Q(hw_mb__icontains=filter_value) |
                         Q(hw_ram__icontains=filter_value) |
                         Q(hw_disk__icontains=filter_value) |
                         Q(hw_gpu__icontains=filter_value) |
                         Q(first_network__icontains=filter_value) |
                         Q(mem_use__icontains=filter_value) |
                         Q(disk_use__icontains=filter_value))
            user = user.filter(query)
    computer_id= list(user.values('computer_id'))
    computer_name= list(user.values('computer_name'))
    count = user.values('computer_id').count()
    data = {
        'message': 'Data received successfully.',
        'computer_id': computer_id,
        'computer_name': computer_name,
        'count': count,

    }

    # JsonResponse 객체로 응답 반환
    return JsonResponse(data)



@csrf_exempt
def sw_pur_asset_select_all(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='PUR_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='PUR_asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    start_of_today1 = now.strftime('%Y-%m-%d %H')
    start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
    start_of_today = timezone.make_aware(start_of_today2)
    start_of_day = start_of_today - timedelta(days=7)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    seven_days_ago = timezone.now() - timedelta(days=7)
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)

    if filter_text and filter_column:
        if filter_column == "user_date":
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(chw_cpu__icontains=term) |
                                                       Q(hw_mb__icontains=term) |
                                                       Q(hw_ram__icontains=term) |
                                                       Q(hw_disk__icontains=term) |
                                                       Q(chw_gpu__icontains=term) |
                                                       Q(first_network__icontains=term) |
                                                       Q(mem_use__icontains=term) |
                                                       Q(disk_use__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(chw_cpu__icontains=term) |
                                                      Q(hw_mb__icontains=term) |
                                                      Q(hw_ram__icontains=term) |
                                                      Q(hw_disk__icontains=term) |
                                                      Q(chw_gpu__icontains=term) |
                                                      Q(first_network__icontains=term) |
                                                      Q(mem_use__icontains=term) |
                                                      Q(disk_use__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hw_cpu__icontains=filter_value) |
                                 Q(hw_mb__icontains=filter_value) |
                                 Q(hw_ram__icontains=filter_value) |
                                 Q(hw_disk__icontains=filter_value) |
                                 Q(hw_gpu__icontains=filter_value) |
                                 Q(first_network__icontains=filter_value) |
                                 Q(mem_use__icontains=filter_value) |
                                 Q(disk_use__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            #filter_column = 'computer__' + filter_column
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            #print(user)
            # service = Xfactor_Service.objects.filter(computer=user.computer_id)
            # print(service.essential1)
            user = user.filter(query)
            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(sw_list__icontains=term) |
                                                   Q(sw_ver_list__icontains=term) |
                                                   Q(sw_install__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                  Q(computer_name__icontains=term) |
                                                  Q(ip_address__icontains=term) |
                                                  Q(sw_list__icontains=term) |
                                                  Q(sw_ver_list__icontains=term) |
                                                  Q(sw_install__icontains=term) |
                                                  Q(memo__icontains=term)
                                                  for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                             Q(logged_name_id__deptName__icontains=filter_value) |
                             Q(logged_name_id__userName__icontains=filter_value) |
                             Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(sw_list__icontains=filter_value) |
                             Q(sw_ver_list__icontains=filter_value) |
                             Q(sw_install__icontains=filter_value) |
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        #user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

        # print(user.values_list('computer_id', flat=True))
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(sw_ver_list__icontains=term) |
                                               Q(sw_install__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(sw_list__icontains=term) |
                                              Q(sw_ver_list__icontains=term) |
                                              Q(sw_install__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(logged_name_id__deptName__icontains=filter_value) |
                         Q(logged_name_id__userName__icontains=filter_value) |
                         Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(sw_list__icontains=filter_value) |
                         Q(sw_ver_list__icontains=filter_value) |
                         Q(sw_install__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)
    computer_id= list(user.values('computer_id'))
    computer_name= list(user.values('computer_name'))
    count = user.values('computer_id').count()
    data = {
        'message': 'Data received successfully.',
        'computer_id': computer_id,
        'computer_name': computer_name,
        'count': count,

    }

    # JsonResponse 객체로 응답 반환
    return JsonResponse(data)
