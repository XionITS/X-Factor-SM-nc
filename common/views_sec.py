import json

import pytz
from django.http import HttpResponse
import math
import operator
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, F , ExpressionWrapper, fields
from django.db.models.functions import Lower
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
#today_collect_date = timezone.now() - timedelta(minutes=7)
with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

def sec_asset(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='SEC_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='SEC_asset', auth_use='true')
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
    #테이블아래 자산현황
    asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    total_item_count = sum(asset.values_list('item_count', flat=True))
    context = {'menu_list': unique_items}
    return render(request, 'sec_asset.html', context)

@csrf_exempt
def sec_asset_paging(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='SEC_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='SEC_asset', auth_use='true')
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
    default_os = request.POST.get('filter[defaultColumn]')
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
    count_list = []
    # cososys_count = user.filter(security1='True ').count()
    # symantec_count = user.filter(security2='True ').count()
    # cbr_count = user.filter(security3='True ').count()
    # cbc_count = user.filter(security4='True ').count()
    # mcafee_count = user.filter(security5='True ').count()

    cososys_count = Daily_Statistics_log.objects.filter(item='cososys', statistics_collection_date__gte=start_of_today).values_list('item_count', flat=True).first()
    symantec_count = Daily_Statistics_log.objects.filter(item='symantec', statistics_collection_date__gte=start_of_today).values_list('item_count', flat=True).first()
    cbr_count = Daily_Statistics_log.objects.filter(item='cbr', statistics_collection_date__gte=start_of_today).values_list('item_count', flat=True).first()
    cbc_count = Daily_Statistics_log.objects.filter(item='cbc', statistics_collection_date__gte=start_of_today).values_list('item_count', flat=True).first()
    mcafee_count = Daily_Statistics_log.objects.filter(item='mcafee', statistics_collection_date__gte=start_of_today).values_list('item_count', flat=True).first()
    # if not cososys_count and not symantec_count and not cbr_count and not cbc_count and not mcafee_count:
    #     cososys_count = Daily_Statistics_log.objects.filter(item='cososys').values_list('item_count', flat=True).first()
    #     symantec_count = Daily_Statistics_log.objects.filter(item='symantec').values_list('item_count', flat=True).first()
    #     cbr_count = Daily_Statistics_log.objects.filter(item='cbr').values_list('item_count', flat=True).first()
    #     cbc_count = Daily_Statistics_log.objects.filter(item='cbc').values_list('item_count', flat=True).first()
    #     mcafee_count = Daily_Statistics_log.objects.filter(item='mcafee').values_list('item_count', flat=True).first()
    # else:
    count_list = cososys_count, symantec_count, cbr_count, cbc_count, mcafee_count
    print(count_list)
    # count_list = cososys_count, symantec_count, cbr_count, cbc_count, mcafee_count

    if filter_text and filter_column:
        if filter_column == "user_date":
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
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
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
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
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
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
        13: 'user_date',
        14: 'memo'
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
    user_list = Commonserializer2(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
        'count_list': count_list
    }

    return JsonResponse(response)


@csrf_exempt
def sec_asset_select_all(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='SEC_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='SEC_asset', auth_use='true')
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
    default_os = request.POST.get('filter[defaultColumn]')
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if filter_text and filter_column:
        if filter_column == "user_date":
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
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
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
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
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
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
    computer_id = list(user.values('computer_id'))
    computer_name = list(user.values('computer_name'))
    count = user.values('computer_id').count()
    data = {
        'message': 'Data received successfully.',
        'computer_id': computer_id,
        'computer_name': computer_name,
        'count': count,

    }

    # JsonResponse 객체로 응답 반환
    return JsonResponse(data)


def sec_asset_list(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='SEC_asset_list', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='SEC_asset_list', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../home/')
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
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                 xfactor_auth_id='SEC_asset_list', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='SEC_asset_list', auth_use='true')
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
    user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if filter_text and filter_column:
        if filter_column == "user_date":
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
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
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
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
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
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
        13: 'user_date',
        14: 'memo',
    }
    #order_column = order_column_map.get(order_column_index, 'chassistype')
    #if order_column_dir == 'desc':
    #    user = user.order_by(order_column, '-computer_id')
    #else:
    #    user = user.order_by('-' + order_column, 'computer_id')
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
    user_list = Commonserializer2(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list  # Serialized data for the current page
    }

    return JsonResponse(response)



@csrf_exempt
def sec_list_asset_select_all(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                 xfactor_auth_id='SEC_asset_list', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='SEC_asset_list', auth_use='true')
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
    user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if filter_text and filter_column:
        if filter_column == "user_date":
            user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
            if all(char in "online" for char in filter_text.lower()):
                user = user.filter(user_date__gte=start_of_today)
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
            elif all(char in "offline" for char in filter_text.lower()):
                user = user.filter(user_date__lt=start_of_today)
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
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_day)
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
