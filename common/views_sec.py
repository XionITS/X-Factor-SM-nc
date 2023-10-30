import json

from django.http import HttpResponse
import math
import operator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, F , ExpressionWrapper, fields
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
from common.custom_sort_key import custom_sort_key as cus_sort
#today_collect_date = timezone.now() - timedelta(minutes=7)
with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

def sec_asset(request):
    #메뉴
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    #테이블아래 자산현황
    asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))
    context = {'menu_list': unique_items}
    return render(request, 'sec_asset.html', context)

@csrf_exempt
def sec_asset_paging(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    seven_days_ago = timezone.now() - timedelta(days=7)
    default_os = request.POST.get('filter[defaultColumn]')
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)

    cososys_count = user.filter(security1='True ').count()
    symantec_count = user.filter(security2='True ').count()
    cbr_count = user.filter(security3='True ').count()
    cbc_count = user.filter(security4='True ').count()
    mcafee_count = user.filter(security5='True ').count()

    count_list = cososys_count, symantec_count, cbr_count, cbc_count, mcafee_count

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
                        query = reduce(operator.and_, [Q(os_simple__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(security1__icontains=term) |
                                                       Q(security2__icontains=term) |
                                                       Q(security3__icontains=term) |
                                                       Q(security4__icontains=term) |
                                                       Q(security5__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(os_simple__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(security1__icontains=term) |
                                                      Q(security2__icontains=term) |
                                                      Q(security3__icontains=term) |
                                                      Q(security4__icontains=term) |
                                                      Q(security5__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(os_simple__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(security1__icontains=filter_value) |
                                 Q(security2__icontains=filter_value) |
                                 Q(security3__icontains=filter_value) |
                                 Q(security4__icontains=filter_value) |
                                 Q(security5__icontains=filter_value) |
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            elif filter_text == "offline":
                user = user.annotate(time_difference=ExpressionWrapper(
                    F('user_date') - F('cache_date'),
                    output_field=fields.DurationField()
                )).filter(time_difference__gt=timedelta(hours=1))
                if filter_value:
                    if ' and ' in filter_value:
                        search_terms = filter_value.split(' and ')
                        query = reduce(operator.and_, [Q(os_simple__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(security1__icontains=term) |
                                                       Q(security2__icontains=term) |
                                                       Q(security3__icontains=term) |
                                                       Q(security4__icontains=term) |
                                                       Q(security5__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(os_simple__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(security1__icontains=term) |
                                                      Q(security2__icontains=term) |
                                                      Q(security3__icontains=term) |
                                                      Q(security4__icontains=term) |
                                                      Q(security5__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(os_simple__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(security1__icontains=filter_value) |
                                 Q(security2__icontains=filter_value) |
                                 Q(security3__icontains=filter_value) |
                                 Q(security4__icontains=filter_value) |
                                 Q(security5__icontains=filter_value) |
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            user = user.filter(query)

            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(os_simple__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(security1__icontains=term) |
                                                   Q(security2__icontains=term) |
                                                   Q(security3__icontains=term) |
                                                   Q(security4__icontains=term) |
                                                   Q(security5__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(os_simple__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(security1__icontains=term) |
                                                   Q(security2__icontains=term) |
                                                   Q(security3__icontains=term) |
                                                   Q(security4__icontains=term) |
                                                   Q(security5__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                else:
                    query = (Q(os_simple__icontains=filter_value) |
                             Q(logged_name_id__deptName__icontains=filter_value) |
                             Q(logged_name_id__userName__icontains=filter_value) |
                             Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(security1__icontains=filter_value) |
                             Q(security2__icontains=filter_value) |
                             Q(security3__icontains=filter_value) |
                             Q(security4__icontains=filter_value) |
                             Q(security5__icontains=filter_value) |
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(os_simple__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(security1__icontains=term) |
                                               Q(security2__icontains=term) |
                                               Q(security3__icontains=term) |
                                               Q(security4__icontains=term) |
                                               Q(security5__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(os_simple__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(security1__icontains=term) |
                                               Q(security2__icontains=term) |
                                               Q(security3__icontains=term) |
                                               Q(security4__icontains=term) |
                                               Q(security5__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(os_simple__icontains=filter_value) |
                         Q(logged_name_id__deptName__icontains=filter_value) |
                         Q(logged_name_id__userName__icontains=filter_value) |
                         Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(security1__icontains=filter_value) |
                         Q(security2__icontains=filter_value) |
                         Q(security3__icontains=filter_value) |
                         Q(security4__icontains=filter_value) |
                         Q(security5__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chassistype',
        2: 'os_simple',
        3: 'logged_name_id__deptName',
        4: 'logged_name_id__userName',
        5: 'logged_name_id__userId',
        6: 'computer_name',
        7: 'security1',
        8: 'security2',
        9: 'security3',
        10: 'security4',
        11: 'security5',
        13: 'cache_date',
        14: 'memo'
        # Add mappings for other columns here
    }
    order_column = order_column_map.get(order_column_index, 'computer_name')
    if order_column_dir == 'asc':
        user = sorted(user, key=lambda x: cus_sort(x, order_column))
        #user = user.order_by(order_column, '-computer_id')
    else:
        user = sorted(user, key=lambda x: cus_sort(x, order_column), reverse=True)

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
        'count_list': count_list
    }

    return JsonResponse(response)


def sec_asset_list(request):
    # 메뉴
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    # 테이블아래 자산현황
    asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))

    context = {'menu_list': unique_items}
    return render(request, 'sec_asset_list.html', context)


@csrf_exempt
def sec_asset_list_paging(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    seven_days_ago = timezone.now() - timedelta(days=7)
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)

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
                                                       Q(os_simple__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(mac_address__icontains=term) |
                                                       Q(ext_chr__icontains=term) |
                                                       Q(ext_edg__icontains=term) |
                                                       Q(ext_fir__icontains=term) |
                                                       Q(sw_list__icontains=term) |
                                                       Q(sw_ver_list__icontains=term) |
                                                       Q(hotfix__icontains=term) |
                                                       Q(hotfix_date__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(os_simple__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(mac_address__icontains=term) |
                                                      Q(ext_chr__icontains=term) |
                                                      Q(ext_edg__icontains=term) |
                                                      Q(ext_fir__icontains=term) |
                                                      Q(sw_list__icontains=term) |
                                                      Q(sw_ver_list__icontains=term) |
                                                      Q(hotfix__icontains=term) |
                                                      Q(hotfix_date__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(os_simple__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(mac_address__icontains=filter_value) |
                                 Q(ext_chr__icontains=filter_value) |
                                 Q(ext_edg__icontains=filter_value) |
                                 Q(ext_fir__icontains=filter_value) |
                                 Q(sw_list__icontains=filter_value) |
                                 Q(sw_ver_list__icontains=filter_value) |
                                 Q(hotfix__icontains=filter_value) |
                                 Q(hotfix_date__icontains=filter_value) |
                                 Q(memo__icontains=filter_value)
                                 )
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
                                                       Q(os_simple__icontains=term) |
                                                       Q(logged_name_id__deptName__icontains=term) |
                                                       Q(logged_name_id__userName__icontains=term) |
                                                       Q(logged_name_id__userId__icontains=term) |
                                                       Q(computer_name__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(mac_address__icontains=term) |
                                                       Q(ext_chr__icontains=term) |
                                                       Q(ext_edg__icontains=term) |
                                                       Q(ext_fir__icontains=term) |
                                                       Q(sw_list__icontains=term) |
                                                       Q(sw_ver_list__icontains=term) |
                                                       Q(hotfix__icontains=term) |
                                                       Q(hotfix_date__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(os_simple__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(mac_address__icontains=term) |
                                                      Q(ext_chr__icontains=term) |
                                                      Q(ext_edg__icontains=term) |
                                                      Q(ext_fir__icontains=term) |
                                                      Q(sw_list__icontains=term) |
                                                      Q(sw_ver_list__icontains=term) |
                                                      Q(hotfix__icontains=term) |
                                                      Q(hotfix_date__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(os_simple__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(mac_address__icontains=filter_value) |
                                 Q(ext_chr__icontains=filter_value) |
                                 Q(ext_edg__icontains=filter_value) |
                                 Q(ext_fir__icontains=filter_value) |
                                 Q(sw_list__icontains=filter_value) |
                                 Q(sw_ver_list__icontains=filter_value) |
                                 Q(hotfix__icontains=filter_value) |
                                 Q(hotfix_date__icontains=filter_value) |
                                 Q(memo__icontains=filter_value)
                                 )
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            user = user.filter(query)

            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(os_simple__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(mac_address__icontains=term) |
                                                   Q(ext_chr__icontains=term) |
                                                   Q(ext_edg__icontains=term) |
                                                   Q(ext_fir__icontains=term) |
                                                   Q(sw_list__icontains=term) |
                                                   Q(sw_ver_list__icontains=term) |
                                                   Q(hotfix__icontains=term) |
                                                   Q(hotfix_date__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                   Q(os_simple__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(mac_address__icontains=term) |
                                                   Q(ext_chr__icontains=term) |
                                                   Q(ext_edg__icontains=term) |
                                                   Q(ext_fir__icontains=term) |
                                                   Q(sw_list__icontains=term) |
                                                   Q(sw_ver_list__icontains=term) |
                                                   Q(hotfix__icontains=term) |
                                                   Q(hotfix_date__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                             Q(os_simple__icontains=filter_value) |
                             Q(logged_name_id__deptName__icontains=filter_value) |
                             Q(logged_name_id__userName__icontains=filter_value) |
                             Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(mac_address__icontains=filter_value) |
                             Q(ext_chr__icontains=filter_value) |
                             Q(ext_edg__icontains=filter_value) |
                             Q(ext_fir__icontains=filter_value) |
                             Q(sw_list__icontains=filter_value) |
                             Q(sw_ver_list__icontains=filter_value) |
                             Q(hotfix__icontains=filter_value) |
                             Q(hotfix_date__icontains=filter_value) |
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).filter(cache_date__gte=seven_days_ago)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(os_simple__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(ext_chr__icontains=term) |
                                               Q(ext_edg__icontains=term) |
                                               Q(ext_fir__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(sw_ver_list__icontains=term) |
                                               Q(hotfix__icontains=term) |
                                               Q(hotfix_date__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                               Q(os_simple__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(ext_chr__icontains=term) |
                                               Q(ext_edg__icontains=term) |
                                               Q(ext_fir__icontains=term) |
                                               Q(sw_list__icontains=term) |
                                               Q(sw_ver_list__icontains=term) |
                                               Q(hotfix__icontains=term) |
                                               Q(hotfix_date__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                         Q(os_simple__icontains=filter_value) |
                         Q(logged_name_id__deptName__icontains=filter_value) |
                         Q(logged_name_id__userName__icontains=filter_value) |
                         Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(mac_address__icontains=filter_value) |
                         Q(ext_chr__icontains=filter_value) |
                         Q(ext_edg__icontains=filter_value) |
                         Q(ext_fir__icontains=filter_value) |
                         Q(sw_list__icontains=filter_value) |
                         Q(sw_ver_list__icontains=filter_value) |
                         Q(hotfix__icontains=filter_value) |
                         Q(hotfix_date__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'chassistype',
        3: 'os_simple',
        4: 'logged_name_id__deptName',
        5: 'logged_name_id__userName',
        6: 'logged_name_id__userId',
        7: 'computer_name',
        8: 'ip_address',
        9: 'mac_address',
        10: 'ext_chr',
        11: 'sw_list',
        12: 'hotfix',
        13: 'cache_date',
        14: 'memo',
    }
    order_column = order_column_map.get(order_column_index, 'chassistype')
    if order_column_dir == 'desc':
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
        'data': user_list  # Serialized data for the current page
    }

    return JsonResponse(response)

