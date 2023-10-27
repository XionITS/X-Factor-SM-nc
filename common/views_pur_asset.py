from django.http import HttpResponse
import math
import json
import operator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q , F , ExpressionWrapper, fields
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
import pytz

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']


@csrf_exempt
def pur_asset(request):
    #메뉴
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})

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
    user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)
    if filter_text and filter_column:
        if filter_column == "cache_date":
            user = user.filter(user_date__gte=today_collect_date)
            if filter_text == "online":
                user = user.annotate(time_difference=ExpressionWrapper(
                    F('user_date') - F('cache_date'),
                    output_field=fields.DurationField()
                )).filter(time_difference__lte=timedelta(hours=1))
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
            elif filter_text == "offline":
                user = user.annotate(time_difference=ExpressionWrapper(
                    F('user_date') - F('cache_date'),
                    output_field=fields.DurationField()
                )).filter(time_difference__gt=timedelta(hours=1))
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
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)
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
        12: 'cache_date',
        13: 'memo',
        # Add mappings for other columns here
    }

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

    user_list = Cacheserializer(page, many=True).data


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
        if filter_column == "cache_date":
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)
            if filter_text == "online":
                user = user.annotate(time_difference=ExpressionWrapper(
                    F('user_date') - F('cache_date'),
                    output_field=fields.DurationField()
                )).filter(time_difference__lte=timedelta(hours=1))
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
            elif filter_text == "offline":
                user = user.annotate(time_difference=ExpressionWrapper(
                    F('user_date') - F('cache_date'),
                    output_field=fields.DurationField()
                )).filter(time_difference__gt=timedelta(hours=1))
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
            #filter_column = 'computer__' + filter_column
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)
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
        Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)

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
        12: 'cache_date',
        13: 'memo',
        # Add mappings for other columns here
    }
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
    user_list = Cacheserializer(page, many=True).data

    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

