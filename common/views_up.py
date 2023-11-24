import json

import pytz
from django.http import HttpResponse
import math
import operator
from django.shortcuts import render,redirect
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
from common.custom_sort_key import custom_sort_key as cus_sort

#today_collect_date = timezone.now() - timedelta(minutes=7)
with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

@csrf_exempt
def up_asset(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                 xfactor_auth_id='UP_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='UP_asset', auth_use='true')
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
    context = {'menu_list': unique_items}
    #테이블아래 자산현황
    asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))
    return render(request, 'up_asset.html', context)

@csrf_exempt
def up_asset_paging(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='UP_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='UP_asset', auth_use='true')
    print(user_auth)
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
    user = Xfactor_Common_Cache.objects.filter(os_simple='Windows')
    # user = user.datetime.strptime(user.hotfix_date, '%m/%d/%Y %H:%M:%S')
    if filter_text and filter_column:
        if filter_column == "cache_date":
            user = user.filter(user_date__gte=start_of_today)
            if all(char in "online" for char in filter_text.lower()):
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
                                                       Q(mac_address__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(hotfix__icontains=term) |
                                                       Q(hotfix_date__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(mac_address__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(hotfix__icontains=term) |
                                                      Q(hotfix_date__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(mac_address__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hotfix__icontains=filter_value) |
                                 Q(hotfix_date__icontains=filter_value) |
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            elif all(char in "offline" for char in filter_text.lower()):
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
                                                       Q(mac_address__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(hotfix__icontains=term) |
                                                       Q(hotfix_date__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(mac_address__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(hotfix__icontains=term) |
                                                      Q(hotfix_date__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(mac_address__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hotfix__icontains=filter_value) |
                                 Q(hotfix_date__icontains=filter_value) |
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            user = user.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
            user = user.filter(query)
            #user = Xfactor_Common.objects.filter(query)
            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(mac_address__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(hotfix__icontains=term) |
                                                   Q(hotfix_date__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(mac_address__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(hotfix__icontains=term) |
                                                   Q(hotfix_date__icontains=term) |
                                                   Q(memo__icontains=term)
                                                  for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                            Q(logged_name_id__deptName__icontains=filter_value) |
                            Q(logged_name_id__userName__icontains=filter_value) |
                            Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(mac_address__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(hotfix__icontains=filter_value) |
                             Q(hotfix_date__icontains=filter_value) |
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        user = user.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hotfix__icontains=term) |
                                               Q(hotfix_date__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hotfix__icontains=term) |
                                               Q(hotfix_date__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                        Q(logged_name_id__deptName__icontains=filter_value) |
                        Q(logged_name_id__userName__icontains=filter_value) |
                        Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(mac_address__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hotfix__icontains=filter_value) |
                         Q(hotfix_date__icontains=filter_value) |
                         Q(memo__icontains=filter_value))
            user = user.filter(query)


    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'chassistype',
        2: 'logged_name_id__deptName',
        3: 'logged_name_id__userName',
        4: 'logged_name_id__userId',
        5: 'computer_name',
        6: 'ip_address',
        7: 'mac_address',
        9: 'cache_date',
        10: 'memo',
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
    user_list = Cacheserializer(page, many=True).data
    # Prepare the response

    #hotfix_list = user.values_list('hotfix', flat=True)
    #hotfix_date_list = user.values_list('hotfix_date', flat=True)
    # print(hotfix_date_list)

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


@csrf_exempt
def up_asset_select_all(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='UP_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='UP_asset', auth_use='true')
    print(user_auth)
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
    user = Xfactor_Common_Cache.objects.filter(os_simple='Windows')
    # user = user.datetime.strptime(user.hotfix_date, '%m/%d/%Y %H:%M:%S')
    if filter_text and filter_column:
        if filter_column == "cache_date":
            user = user.filter(user_date__gte=start_of_today)
            if all(char in "online" for char in filter_text.lower()):
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
                                                       Q(mac_address__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(hotfix__icontains=term) |
                                                       Q(hotfix_date__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(mac_address__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(hotfix__icontains=term) |
                                                      Q(hotfix_date__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(mac_address__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hotfix__icontains=filter_value) |
                                 Q(hotfix_date__icontains=filter_value) |
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            elif all(char in "offline" for char in filter_text.lower()):
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
                                                       Q(mac_address__icontains=term) |
                                                       Q(ip_address__icontains=term) |
                                                       Q(hotfix__icontains=term) |
                                                       Q(hotfix_date__icontains=term) |
                                                       Q(memo__icontains=term)
                                                       for term in search_terms])
                    elif ' or ' in filter_value:
                        search_terms = filter_value.split(' or ')
                        query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
                                                      Q(computer_name__icontains=term) |
                                                      Q(mac_address__icontains=term) |
                                                      Q(ip_address__icontains=term) |
                                                      Q(hotfix__icontains=term) |
                                                      Q(hotfix_date__icontains=term) |
                                                      Q(memo__icontains=term)
                                                      for term in search_terms])
                    else:
                        query = (Q(chassistype__icontains=filter_value) |
                                 Q(logged_name_id__deptName__icontains=filter_value) |
                                 Q(logged_name_id__userName__icontains=filter_value) |
                                 Q(logged_name_id__userId__icontains=filter_value) |
                                 Q(computer_name__icontains=filter_value) |
                                 Q(mac_address__icontains=filter_value) |
                                 Q(ip_address__icontains=filter_value) |
                                 Q(hotfix__icontains=filter_value) |
                                 Q(hotfix_date__icontains=filter_value) |
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            user = user.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
            user = user.filter(query)
            #user = Xfactor_Common.objects.filter(query)
            if filter_value:
                if ' and ' in filter_value:
                    search_terms = filter_value.split(' and ')
                    query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                                   Q(logged_name_id__deptName__icontains=term) |
                                                   Q(logged_name_id__userName__icontains=term) |
                                                   Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(mac_address__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(hotfix__icontains=term) |
                                                   Q(hotfix_date__icontains=term) |
                                                   Q(memo__icontains=term)
                                                   for term in search_terms])
                elif ' or ' in filter_value:
                    search_terms = filter_value.split(' or ')
                    query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
                                                   Q(computer_name__icontains=term) |
                                                   Q(mac_address__icontains=term) |
                                                   Q(ip_address__icontains=term) |
                                                   Q(hotfix__icontains=term) |
                                                   Q(hotfix_date__icontains=term) |
                                                   Q(memo__icontains=term)
                                                  for term in search_terms])
                else:
                    query = (Q(chassistype__icontains=filter_value) |
                            Q(logged_name_id__deptName__icontains=filter_value) |
                            Q(logged_name_id__userName__icontains=filter_value) |
                            Q(logged_name_id__userId__icontains=filter_value) |
                             Q(computer_name__icontains=filter_value) |
                             Q(mac_address__icontains=filter_value) |
                             Q(ip_address__icontains=filter_value) |
                             Q(hotfix__icontains=filter_value) |
                             Q(hotfix_date__icontains=filter_value) |
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        user = user.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hotfix__icontains=term) |
                                               Q(hotfix_date__icontains=term) |
                                               Q(memo__icontains=term)
                                               for term in search_terms])
            elif ' or ' in filter_value:
                search_terms = filter_value.split(' or ')
                query = reduce(operator.or_, [Q(chassistype__icontains=term) |
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
                                               Q(computer_name__icontains=term) |
                                               Q(mac_address__icontains=term) |
                                               Q(ip_address__icontains=term) |
                                               Q(hotfix__icontains=term) |
                                               Q(hotfix_date__icontains=term) |
                                               Q(memo__icontains=term)
                                              for term in search_terms])
            else:
                query = (Q(chassistype__icontains=filter_value) |
                        Q(logged_name_id__deptName__icontains=filter_value) |
                        Q(logged_name_id__userName__icontains=filter_value) |
                        Q(logged_name_id__userId__icontains=filter_value) |
                         Q(computer_name__icontains=filter_value) |
                         Q(mac_address__icontains=filter_value) |
                         Q(ip_address__icontains=filter_value) |
                         Q(hotfix__icontains=filter_value) |
                         Q(hotfix_date__icontains=filter_value) |
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
