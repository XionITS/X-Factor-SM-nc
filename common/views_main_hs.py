from django.http import HttpResponse
import math
import operator
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#from django.utils import timezone
from django.db.models import Q
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
import pytz


# menu_list = Xfactor_Auth.objects.get(auth_id="OS_asset").auth_name
# menu_list = Xfactor_Auth.objects.all()
# menu_list = []
# auth_names = Xfactor_Auth.objects.values_list('auth_name', flat=True)
# for auth_name in auth_names:
#    menu_list.append(auth_name)

#  Daily_Statistics.objects.filter(classification='chassis_type').values('item','item_count')
#    asset = Daily_Statistics.objects.filter(classification='chassis_type').values('item','item_count').order_by('-item_count')


# auth_id = user_auth.auth_id
# auth_name = user_auth.xfactor_auth.auth_name
# auth_url = user_auth.xfactor_auth.auth_url
# print(menu_list)
#today_collect_date = timezone.now() - timedelta(minutes=7)


@csrf_exempt
def dashboard(request):
    print(Xfactor_Xuser_Auth.objects.all())
    #session을 computer_id에 넣기
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    # user_auths = Xfactor_CommonAuth.objects.filter(xfactor_user__computer_id='123', auth_use='true')  # 사용자의 권한 목록 가져오기
    # menu_list = []
    # for user_auth in user_auths:
    #     menu_list.append(user_auth.xfactor_auth)
    # menu_list = serialize('json', menu_list)
    # print(menu_list)
    #menu_list = list(Xfactor_CommonAuth.objects.values().filter(xfactor_user__computer_id='123', auth_use='true'))
    context = {'menu_list' : menu.data}
    return render(request, 'dashboard1.html', context)


def dashboard1(request):
    print(Xfactor_Xuser_Auth.objects.all())
    #session을 computer_id에 넣기
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    # user_auths = Xfactor_CommonAuth.objects.filter(xfactor_user__computer_id='123', auth_use='true')  # 사용자의 권한 목록 가져오기
    # menu_list = []
    # for user_auth in user_auths:
    #     menu_list.append(user_auth.xfactor_auth)
    # menu_list = serialize('json', menu_list)
    # print(menu_list)
    #menu_list = list(Xfactor_CommonAuth.objects.values().filter(xfactor_user__computer_id='123', auth_use='true'))
    context = {'menu_list' : menu.data}
    return render(request, 'dashboard1.html', context)


@csrf_exempt
def hs_asset(request):
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    #테이블아래 자산현황
    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    local_now = utc_now.astimezone(local_tz)
    # 24시간 30분 이전의 시간 계산
    today_collect_date = local_now - timedelta(minutes=7)
    asset = Daily_Statistics.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')[:5]
    total_asset = Daily_Statistics.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(total_asset.values_list('item_count', flat=True))

    context = {'menu_list' : menu.data, 'asset' : asset, 'total_item_count' : total_item_count}
    return render(request, 'hs_asset.html', context)

@csrf_exempt
def hs_asset_paginghw(request):
    filter_column = request.POST.get('filter[column]')
    print(filter_column)
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    local_now = utc_now.astimezone(local_tz)
    # 24시간 30분 이전의 시간 계산
    today_collect_date = local_now - timedelta(minutes=7)
    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
        user = user.filter(query)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hw_cpu__icontains=term) |
                                               Q(hw_mb__icontains=term) |
                                               Q(hw_ram__icontains=term) |
                                               Q(hw_disk__icontains=term) |
                                               Q(hw_gpu__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(hw_cpu__icontains=term) |
                                              Q(hw_mb__icontains=term) |
                                              Q(hw_ram__icontains=term) |
                                              Q(hw_disk__icontains=term) |
                                              Q(hw_gpu__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hw_cpu__icontains=filter_value) |
                         Q(hw_mb__icontains=filter_value) |
                         Q(hw_ram__icontains=filter_value) |
                         Q(hw_disk__icontains=filter_value) |
                         Q(hw_gpu__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hw_cpu__icontains=term) |
                                               Q(hw_mb__icontains=term) |
                                               Q(hw_ram__icontains=term) |
                                               Q(hw_disk__icontains=term) |
                                               Q(hw_gpu__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(hw_cpu__icontains=term) |
                                              Q(hw_mb__icontains=term) |
                                              Q(hw_ram__icontains=term) |
                                              Q(hw_disk__icontains=term) |
                                              Q(hw_gpu__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hw_cpu__icontains=filter_value) |
                         Q(hw_mb__icontains=filter_value) |
                         Q(hw_ram__icontains=filter_value) |
                         Q(hw_disk__icontains=filter_value) |
                         Q(hw_gpu__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)



    # user = user.exclude(ip_address='unconfirmed')
    # user = user.exclude(hw_list='unconfirmed')
    # user = user.exclude(os_total='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chassistype',
        2: 'computer_name',
        3: 'ip_address',
        4: 'hw_cpu',
        5: 'hw_mb',
        6: 'hw_ram',
        7: 'hw_disk',
        8: 'hw_gpu',
        9: 'memo'
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


    # #메뉴
    # user_auths = Xfactor_CommonAuth.objects.filter(xfactor_user__computer_id='123', auth_use='true')
    # menu = XuserAuthSerializer(user_auths, many=True)
    #검색
    # search_text = request.POST.get('search[value]')
    # print(search_text)
    # if search_text:
    #     user = Xfactor_Common.objects.filter(
    #         Q(chassistype__icontains=search_text) |
    #         Q(computer_name__icontains=search_text) |
    #         Q(user_name__icontains=search_text) |
    #         Q(ip_address__icontains=search_text) |
    #         Q(hw_list__icontains=search_text) |
    #         Q(memo__icontains=search_text)
    #         # Add more fields as needed
    #     )
    # else:
    #     user= Xfactor_Common.objects.all()
    # #User
    # #user = Xfactor_Common.objects.all()
    # user_list = CommonSerializer(user, many=True)
    # context = {'user_list': user_list.data}
    # return JsonResponse(context)
@csrf_exempt
def hs_asset_pagingsw(request):
    filter_column = request.POST.get('filter[column]')
    print(filter_column)
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    local_now = utc_now.astimezone(local_tz)
    # 24시간 30분 이전의 시간 계산
    today_collect_date = local_now - timedelta(minutes=7)
    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
        # service = Xfactor_Service.objects.filter(computer=user.computer_id)
        # print(service.essential1)
        user = user.filter(query)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(sw_list__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                Q(computer_name__icontains=filter_value) |
                Q(ip_address__icontains=filter_value) |
                Q(sw_list__icontains=filter_value) |
                Q(memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date)
        # print(user.values_list('computer_id', flat=True))
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(sw_list__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(sw_list__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)

    # user = user.exclude(ip_address='unconfirmed')
    # user = user.exclude(os_total='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chassistype',
        2: 'computer_name',
        3: 'ip_address',
        4: 'sw_list',
        5: 'memo'
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
    #user_list = LimitedCommonSerializer(page, many=True).data
    user_list = CommonSerializer(page, many=True).data

    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)



@csrf_exempt
def index(request):
    # user_list = Xfactor_Common
    # context = {'user_list' : user_list}
    # return render(request, 'user_list.html')
    return render(request, '1.html')
@csrf_exempt
def index_paging (request):
    #print(request)
    #return render(request, '1.html')
    # draw = int(request.POST.get('draw'))
    # start = int(request.POST.get('start'))
    # length = int(request.POST.get('length'))
    # search = request.POST.get('search[value]')
    # page = math.ceil(start / length) + 1
    # data = [ str(length), str(page), str(search)]
    # SMD = PDPI('statistics', 'osMore', data)
    # SMC = PDPI('statistics', 'osCount', data)
    RD = {
           }
    #eturnData = {'computer_id':'123','computer_name':'djlee'}
    group_list = Xfactor_Group.objects.get(group_id=123)
    data = [{'group_id' : group_list.group_id,
            'group_name': group_list.group_name,
            'group_note': group_list.group_note,
            }]
    RD = {"item": data}
    #print(RD)
    return JsonResponse(RD)