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
#today_collect_date = timezone.now() - timedelta(minutes=7)

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

@csrf_exempt
def ver_asset(request):
    #메뉴
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    #테이블아래 자산현황

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)

    asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='os_simple').values('item', 'item_count').order_by('-item_count')[:5]
    total_item_count = sum(asset.values_list('item_count', flat=True))

    context = {'menu_list': unique_items, 'asset': asset, 'total_item_count': total_item_count}
    return render(request, 'ver_asset.html', context)

@csrf_exempt
def ver_asset_paging(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    default_os = request.POST.get('filter[defaultColumn]')
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Daily.objects.filter(os_simple__icontains=default_os)

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)

    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = user.filter(user_date__gte=today_collect_date)
        user = user.filter(query)
        #user = Xfactor_Common.objects.filter(query)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer_name__icontains=term) |
                                               Q(os_total__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(os_build__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer_name__icontains=term) |
                                               Q(os_total__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(os_build__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(computer_name__icontains=filter_value) |
                         Q(os_total__icontains=filter_value) |
                         Q(os_version__icontains=filter_value) |
                         Q(os_build__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = user.filter(user_date__gte=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer_name__icontains=term) |
                                               Q(os_total__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(os_build__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer_name__icontains=term) |
                                               Q(os_total__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(os_build__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(computer_name__icontains=filter_value) |
                         Q(os_total__icontains=filter_value) |
                         Q(os_version__icontains=filter_value) |
                         Q(os_build__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chassistype',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address',
        5: 'os_total',
        6: 'os_version',
        7: 'os_build',
        8: 'memo'
        # Add mappings for other columns here
    }
    order_column = order_column_map.get(order_column_index, 'computer_name')
    if order_column_dir == 'asc':
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
    user_list = Dailyserializer(page, many=True).data
    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


def os_asset(request):
    # 메뉴
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)

    # 테이블아래 자산현황
    asset = Daily_Statistics.objects.filter(statistics_collection_date__gte=today_collect_date, classification='os_simple').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))

    context = {'menu_list': unique_items, 'asset': asset, 'total_item_count': total_item_count}
    return render(request, 'os_asset.html', context)


@csrf_exempt
def os_asset_paging(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    default_os = request.POST.get('filter[defaultColumn]')
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


    user = Xfactor_Common.objects.filter(os_simple__icontains=default_os)
    #user = Xfactor_Common.objects.filter(os_total__icontains=default_os).exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed')

    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = user.filter(user_date__gte=today_collect_date)
        user = user.filter(query)
        #user = Xfactor_Common.objects.filter(query)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer_name__icontains=term) |
                                               Q(os_simple__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer_name__icontains=term) |
                                               Q(os_simple__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(computer_name__icontains=filter_value) |
                         Q(os_simple__icontains=filter_value) |
                         Q(os_version__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(mac_address__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = user.filter(user_date__gte=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer_name__icontains=term) |
                                               Q(os_simple__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer_name__icontains=term) |
                                               Q(os_simple__icontains=term) |
                                               Q(os_version__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(computer_name__icontains=filter_value) |
                         Q(os_simple__icontains=filter_value) |
                         Q(os_version__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(mac_address__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'computer_name',
        3: 'ip_address',
        4: 'os_simple',
        5: 'os_version',
        6: 'mac_address',
        7: 'memo'
        # Add mappings for other columns here
    }
    order_column = order_column_map.get(order_column_index, 'computer_name')
    if order_column_dir == 'asc':
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

