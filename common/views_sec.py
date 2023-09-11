import json

from django.http import HttpResponse
import math
import operator
from django.shortcuts import render, redirect
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

today_collect_date = timezone.now() - timedelta(minutes=7)
with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

def sec_asset(request):
    #메뉴

    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    #테이블아래 자산현황
    asset = Daily_Statistics.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))
    context = {'menu_list': menu.data}
    return render(request, 'sec_asset.html', context)

@csrf_exempt
def sec_asset_paging(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    default_os = request.POST.get('filter[defaultColumn]')
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Security.objects.select_related('computer').filter(user_date__gte=today_collect_date)

    cososys_count = user.filter(security1='True ').count()
    symantec_count = user.filter(security2='True ').count()
    cbr_count = user.filter(security3='True ').count()
    cbc_count = user.filter(security4='True ').count()
    mcafee_count = user.filter(security5='True ').count()

    count_list = cososys_count, symantec_count, cbr_count, cbc_count, mcafee_count

    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = user.filter(query)

        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(security1__icontains=term) |
                                               Q(security2__icontains=term) |
                                               Q(security3__icontains=term) |
                                               Q(security4__icontains=term) |
                                               Q(security5__icontains=term) |
                                               Q(computer__memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(security1__icontains=term) |
                                               Q(security2__icontains=term) |
                                               Q(security3__icontains=term) |
                                               Q(security4__icontains=term) |
                                               Q(security5__icontains=term) |
                                               Q(computer__memo__icontains=term)
                                               for term in search_terms])
            else:
                query = (Q(computer__os_simple__icontains=filter_value) |
                         Q(computer__computer_name__icontains=filter_value) |
                         Q(security1__icontains=filter_value) |
                         Q(security2__icontains=filter_value) |
                         Q(security3__icontains=filter_value) |
                         Q(security4__icontains=filter_value) |
                         Q(security5__icontains=filter_value) |
                         Q(computer__memo__icontains=filter_value))
            user = user.filter(query)
    else:
        user = Xfactor_Security.objects.select_related('computer').filter(user_date__gte=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(security1__icontains=term) |
                                               Q(security2__icontains=term) |
                                               Q(security3__icontains=term) |
                                               Q(security4__icontains=term) |
                                               Q(security5__icontains=term) |
                                               Q(computer__memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(security1__icontains=term) |
                                               Q(security2__icontains=term) |
                                               Q(security3__icontains=term) |
                                               Q(security4__icontains=term) |
                                               Q(security5__icontains=term) |
                                               Q(computer__memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(computer__os_simple__icontains=filter_value) |
                         Q(computer__computer_name__icontains=filter_value) |
                         Q(security1__icontains=filter_value) |
                         Q(security2__icontains=filter_value) |
                         Q(security3__icontains=filter_value) |
                         Q(security4__icontains=filter_value) |
                         Q(security5__icontains=filter_value) |
                         Q(computer__memo__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'computer__os_simple',
        3: 'computer__computer_name',
        4: 'security1',
        5: 'security2',
        6: 'security3',
        7: 'security4',
        8: 'security5',
        9: 'computer__memo'
        # Add mappings for other columns here
    }
    order_column = order_column_map.get(order_column_index, 'computer__computer_name')
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
    user_list = XfactorSecuritySerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
        'count_list': count_list
    }

    return JsonResponse(response)


def sec_asset_list(request):
    # 메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    # 테이블아래 자산현황
    asset = Daily_Statistics.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))

    context = {'menu_list': menu.data}
    return render(request, 'sec_asset_list.html', context)


@csrf_exempt
def sec_asset_list_paging(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Security.objects.select_related('computer').filter(user_date__gte=today_collect_date)

    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = user.filter(query)

        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer__chassistype__icontains=term) |
                                               Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(computer__ip_address__icontains=term) |
                                               Q(computer__mac_address__icontains=term) |
                                               Q(ext_chr__icontains=term) |
                                               Q(ext_edg__icontains=term) |
                                               Q(ext_fir__icontains=term) |
                                               Q(computer__sw_list__icontains=term) |
                                               Q(computer__sw_ver_list__icontains=term) |
                                               Q(computer__hotfix__icontains=term) |
                                               Q(computer__hotfix_date__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer__chassistype__icontains=term) |
                                               Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(computer__ip_address__icontains=term) |
                                               Q(computer__mac_address__icontains=term) |
                                               Q(ext_chr__icontains=term) |
                                               Q(ext_edg__icontains=term) |
                                               Q(ext_fir__icontains=term) |
                                               Q(computer__sw_list__icontains=term) |
                                               Q(computer__sw_ver_list__icontains=term) |
                                               Q(computer__hotfix__icontains=term) |
                                               Q(computer__hotfix_date__icontains=term)
                                               for term in search_terms])
            else:
                query = (Q(computer__chassistype__icontains=filter_value) |
                         Q(computer__os_simple__icontains=filter_value) |
                         Q(computer__computer_name__icontains=filter_value) |
                         Q(computer__ip_address__icontains=filter_value) |
                         Q(computer__mac_address__icontains=filter_value) |
                         Q(ext_chr__icontains=filter_value) |
                         Q(ext_edg__icontains=filter_value) |
                         Q(ext_fir__icontains=filter_value) |
                         Q(computer__sw_list__icontains=filter_value) |
                         Q(computer__sw_ver_list__icontains=filter_value) |
                         Q(computer__hotfix__icontains=filter_value) |
                         Q(computer__hotfix_date__icontains=filter_value)
                         )
            user = user.filter(query)
    else:
        user = Xfactor_Security.objects.select_related('computer').filter(user_date__gte=today_collect_date)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(computer__chassistype__icontains=term) |
                                               Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(computer__ip_address__icontains=term) |
                                               Q(computer__mac_address__icontains=term) |
                                               Q(ext_chr__icontains=term) |
                                               Q(ext_edg__icontains=term) |
                                               Q(ext_fir__icontains=term) |
                                               Q(computer__sw_list__icontains=term) |
                                               Q(computer__sw_ver_list__icontains=term) |
                                               Q(computer__hotfix__icontains=term) |
                                               Q(computer__hotfix_date__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(computer__chassistype__icontains=term) |
                                               Q(computer__os_simple__icontains=term) |
                                               Q(computer__computer_name__icontains=term) |
                                               Q(computer__ip_address__icontains=term) |
                                               Q(computer__mac_address__icontains=term) |
                                               Q(ext_chr__icontains=term) |
                                               Q(ext_edg__icontains=term) |
                                               Q(ext_fir__icontains=term) |
                                               Q(computer__sw_list__icontains=term) |
                                               Q(computer__sw_ver_list__icontains=term) |
                                               Q(computer__hotfix__icontains=term) |
                                               Q(computer__hotfix_date__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(computer__chassistype__icontains=filter_value) |
                         Q(computer__os_simple__icontains=filter_value) |
                         Q(computer__computer_name__icontains=filter_value) |
                         Q(computer__ip_address__icontains=filter_value) |
                         Q(computer__mac_address__icontains=filter_value) |
                         Q(ext_chr__icontains=filter_value) |
                         Q(ext_edg__icontains=filter_value) |
                         Q(ext_fir__icontains=filter_value) |
                         Q(computer__sw_list__icontains=filter_value) |
                         Q(computer__sw_ver_list__icontains=filter_value) |
                         Q(computer__hotfix__icontains=filter_value) |
                         Q(computer__hotfix_date__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'computer__chassistype',
        3: 'computer__os_simple',
        4: 'computer__computer_name',
        5: 'computer__ip_address',
        6: 'computer__mac_address',
        7: 'ext_chr',
        8: 'computer__sw_list',
        9: 'computer__hotfix'
    }
    order_column = order_column_map.get(order_column_index, 'computer__chassistype')
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
    user_list = XfactorSecuritySerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list  # Serialized data for the current page
    }

    return JsonResponse(response)

