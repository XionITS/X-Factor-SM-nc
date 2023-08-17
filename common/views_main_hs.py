from django.http import HttpResponse
import math
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



# menu_list = XFactor_Auth.objects.get(auth_id="OS_asset").auth_name
# menu_list = XFactor_Auth.objects.all()
# menu_list = []
# auth_names = XFactor_Auth.objects.values_list('auth_name', flat=True)
# for auth_name in auth_names:
#    menu_list.append(auth_name)

#  Daily_Statistics.objects.filter(classification='chassis_type').values('item','item_count')
#    asset = Daily_Statistics.objects.filter(classification='chassis_type').values('item','item_count').order_by('-item_count')


# auth_id = user_auth.auth_id
# auth_name = user_auth.xfactor_auth.auth_name
# auth_url = user_auth.xfactor_auth.auth_url
# print(menu_list)
today_collect_date = timezone.now() - timedelta(hours=24, minutes=30)


@csrf_exempt
def dashboard(request):
    #session을 computer_id에 넣기
    xuser_auths = XFactor_XUserAuth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = UserAuthSerializer(xuser_auths, many=True)
    # user_auths = XFactor_UserAuth.objects.filter(xfactor_user__computer_id='123', auth_use='true')  # 사용자의 권한 목록 가져오기
    # menu_list = []
    # for user_auth in user_auths:
    #     menu_list.append(user_auth.xfactor_auth)
    # menu_list = serialize('json', menu_list)
    # print(menu_list)
    #menu_list = list(XFactor_UserAuth.objects.values().filter(xfactor_user__computer_id='123', auth_use='true'))
    context = {'menu_list' : menu.data}
    return render(request, 'dashboard.html', context)


@csrf_exempt
def hs_asset(request):
    #메뉴
    xuser_auths = XFactor_XUserAuth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = UserAuthSerializer(xuser_auths, many=True)
    #테이블아래 자산현황
    asset = Daily_Statistics.objects.filter(statistics_collection_date__gt=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))

    context = {'menu_list' : menu.data, 'asset' : asset, 'total_item_count' : total_item_count}
    return render(request, 'hs_asset.html', context)
@csrf_exempt
def hs_asset_paginghw(request):
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')

    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = XFactor_User.objects.filter(user_date__gt=today_collect_date)
        user = user.objects.filter(query)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chasisstype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hw_list__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chasisstype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(hw_list__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chasisstype__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hw_list__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = XFactor_User.objects.filter(user_date__gt=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chasisstype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hw_list__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chasisstype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(hw_list__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chasisstype__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hw_list__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)



    user = user.exclude(ip_address='unconfirmed')
    user = user.exclude(hw_list='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chasisstype',
        2: 'computer_name',
        3: 'ip_address',
        4: 'hw_list',
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
    user_list = UserSerializer(page, many=True).data

    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


    # #메뉴
    # user_auths = XFactor_UserAuth.objects.filter(xfactor_user__computer_id='123', auth_use='true')
    # menu = UserAuthSerializer(user_auths, many=True)
    #검색
    # search_text = request.POST.get('search[value]')
    # print(search_text)
    # if search_text:
    #     user = XFactor_User.objects.filter(
    #         Q(chasisstype__icontains=search_text) |
    #         Q(computer_name__icontains=search_text) |
    #         Q(user_name__icontains=search_text) |
    #         Q(ip_address__icontains=search_text) |
    #         Q(hw_list__icontains=search_text) |
    #         Q(memo__icontains=search_text)
    #         # Add more fields as needed
    #     )
    # else:
    #     user= XFactor_User.objects.all()
    # #User
    # #user = XFactor_User.objects.all()
    # user_list = UserSerializer(user, many=True)
    # context = {'user_list': user_list.data}
    # return JsonResponse(context)
@csrf_exempt
def hs_asset_pagingsw(request):
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = XFactor_User.objects.filter(user_date__gt=today_collect_date)
        user = user.objects.filter(query)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chasisstype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chasisstype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(sw_list__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chasisstype__icontains=filter_value) |
                Q(computer_name__icontains=filter_value) |
                Q(ip_address__icontains=filter_value) |
                Q(sw_list__icontains=filter_value) |
                Q(memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = XFactor_User.objects.filter(user_date__gt=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chasisstype__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chasisstype__icontains=term) |
                                              Q(computer_name__icontains=term) |
                                              Q(ip_address__icontains=term) |
                                              Q(sw_list__icontains=term) |
                                              Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chasisstype__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(sw_list__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)

    user = user.exclude(ip_address='unconfirmed')
    user = user.exclude(sw_list='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chasisstype',
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
    #user_list = LimitedUserSerializer(page, many=True).data
    user_list = UserSerializer(page, many=True).data

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
    # user_list = XFactor_User
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
    group_list = XFactor_Group.objects.get(group_id=123)
    data = [{'group_id' : group_list.group_id,
            'group_name': group_list.group_name,
            'group_note': group_list.group_note,
            }]
    RD = {"item": data}
    #print(RD)
    return JsonResponse(RD)