from django.http import HttpResponse
import math
import json
import operator
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count, F , ExpressionWrapper, fields
from django.db.models.functions import Lower
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *
import pytz
from common.custom_sort_key import custom_sort_key as cus_sort

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
from .views_dashboard import Dashboard

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

@csrf_exempt
def dashboard(request):
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)

    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    selected_date = None
    if 'datetime' in request.GET:
        selected_date = request.GET['datetime']
    DCDL = Dashboard(unique_items, selected_date)


    monthly_asset_data_list = DCDL['monthly_asset_data_list']
    cpu_data_list = DCDL['cpu_data_list']
    os_asset_data_list = DCDL['os_asset_data_list']
    os_asset_data_count_list = DCDL['os_asset_data_count_list']
    os_up_data_list = DCDL['os_up_data_list']
    discover_data_list = DCDL['discover_data_list']
    location_data_list = DCDL['location_data_list']
    hotfix_data_list = DCDL['hotfix_data_list']
    asset_all_chart_list = DCDL['asset_all_chart_list']
    office_data_list = DCDL['office_data_list']

    desk_online_list = DCDL['desk_online_list']
    note_online_list = DCDL['note_online_list']
    other_online_list = DCDL['other_online_list']
    desk_total_list = DCDL['desk_total_list']
    note_total_list = DCDL['note_total_list']
    other_total_list = DCDL['other_total_list']
    setting_value_list = DCDL['setting_value_list']

    dataList = {
                'monthly_asset_data_list': monthly_asset_data_list,
                'cpu_data_list': cpu_data_list,
                'os_asset_data_list': os_asset_data_list,
                'os_asset_data_count_list': os_asset_data_count_list,
                'os_up_data_list': os_up_data_list,
                'discover_data_list': discover_data_list,
                'location_data_list': location_data_list,
                'hotfix_data_list': hotfix_data_list,
                'asset_all_chart_list': asset_all_chart_list,
                'office_data_list': office_data_list,
                'desk_online_list': desk_online_list,
                'note_online_list': note_online_list,
                'other_online_list': other_online_list,
                'desk_total_list': desk_total_list,
                'note_total_list': note_total_list,
                'other_total_list': other_total_list,
                'selected_date': selected_date if selected_date is not None else "select date...",
                #'setting_value_list': setting_value_list
    }

    context = {'menu_list' : unique_items, 'dataList': dataList}
    return render(request, 'dashboard1.html', context)

# def dashboard(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         selected_date = request.POST.get('selected_date')
#         DCDL = Dashboard(selected_date)
#         return JsonResponse(DCDL)
#
#
#
#     DCDL = Dashboard()
#     # print(Xfactor_Xuser_Auth.objects.all())
#     #session을 computer_id에 넣기
#     xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
#     #xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id='admin', auth_use='true')
#     menu = XuserAuthSerializer(xuser_auths, many=True)
#     monthly_asset_data_list = DCDL['monthly_asset_data_list']
#     cpu_data_list = DCDL['cpu_data_list']
#     os_asset_data_list = DCDL['os_asset_data_list']
#     os_asset_data_count_list = DCDL['os_asset_data_count_list']
#     os_up_data_list = DCDL['os_up_data_list']
#     discover_data_list = DCDL['discover_data_list']
#     location_data_list = DCDL['location_data_list']
#     hotfix_data_list = DCDL['hotfix_data_list']
#     asset_all_chart_list = DCDL['asset_all_chart_list']
#     office_data_list = DCDL['office_data_list']
#
#     desk_online_list = DCDL['desk_online_list']
#     note_online_list = DCDL['note_online_list']
#     other_online_list = DCDL['other_online_list']
#     desk_total_list = DCDL['desk_total_list']
#     note_total_list = DCDL['note_total_list']
#     other_total_list = DCDL['other_total_list']
#
#     dataList = {
#         'monthly_asset_data_list': monthly_asset_data_list,
#         'cpu_data_list': cpu_data_list,
#         'os_asset_data_list': os_asset_data_list,
#         'os_asset_data_count_list': os_asset_data_count_list,
#         'os_up_data_list': os_up_data_list,
#         'discover_data_list': discover_data_list,
#         'location_data_list': location_data_list,
#         'hotfix_data_list': hotfix_data_list,
#         'asset_all_chart_list': asset_all_chart_list,
#         'office_data_list': office_data_list,
#         'desk_online_list': desk_online_list,
#         'note_online_list': note_online_list,
#         'other_online_list': other_online_list,
#         'desk_total_list': desk_total_list,
#         'note_total_list': note_total_list,
#         'other_total_list': other_total_list,
#     }
#
#     context = {'menu_list' : menu.data, 'dataList': dataList}
#     return render(request, 'dashboard1.html', context)

def dashboard1(request):
    # print(Xfactor_Xuser_Auth.objects.all())
    #session을 computer_id에 넣기
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    context = {'menu_list': unique_items}
    return render(request, 'dashboard1.html', context)


@csrf_exempt
def hs_asset(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],xfactor_auth_id='HS_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'],xfactor_auth_id='HS_asset', auth_use='true')
    #print(user_auth)
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

    # # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    # local_tz = pytz.timezone('Asia/Seoul')
    # # UTC 시간대를 사용하여 현재 시간을 얻음
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # # 현재 시간대로 시간 변환
    # local_now = utc_now.astimezone(local_tz)
    # # 24시간 30분 이전의 시간 계산
    # today_collect_date = local_now - timedelta(minutes=7)

    #온라인자산
    online_asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')[:5]
    online_total_asset = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='chassis_type').values('item', 'item_count').order_by('-item_count')
    online_total_item_count = sum(online_total_asset.values_list('item_count', flat=True))

    #토탈자산
    total_asset_Desk = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='Desktop_cache_total').values('item_count')
    total_asset_Note = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=today_collect_date, classification='Notebook_cache_total').values('item_count')

    context = {'menu_list' : unique_items, 'online_asset' : online_asset, 'online_total_item_count' : online_total_item_count,'total_asset_Desk' : total_asset_Desk, 'total_asset_Note': total_asset_Note}
    return render(request, 'hs_asset.html', context)

@csrf_exempt
def hs_asset_paginghw(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'], xfactor_auth_id='HS_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='HS_asset', auth_use='true')
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
        if filter_column == "cache_date":
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today)
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
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
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
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
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
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
            users = user.values('chassistype').annotate(count=Count('chassistype'))
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
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
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
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
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
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
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
                         Q(memo__icontains=filter_value))
            user = user.filter(query)



    # user = user.exclude(ip_address='unconfirmed')
    # user = user.exclude(hw_list='unconfirmed')
    # user = user.exclude(os_total='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'logged_name_id__userId',
        4: 'computer_name',
        5: 'ip_address',
        6: 'mac_address',
        8: 'cache_date',
        9: 'memo',
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
    #user=user.filter(logged_name__in=Xfactor_ncdb.objects.values('userId'))
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
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='HS_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='HS_asset', auth_use='true')
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
        if filter_column == "cache_date":
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today)
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
                                                       Q(ip_address__icontains=term) |
                                                       Q(sw_list__icontains=term) |
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
                                                       Q(ip_address__icontains=term) |
                                                       Q(sw_list__icontains=term) |
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
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
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
                    Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
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
                         Q(memo__icontains=filter_value))
            user = user.filter(query)

    # user = user.exclude(ip_address='unconfirmed')
    # user = user.exclude(os_total='unconfirmed')
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'logged_name_id__userId',
        4: 'computer_name',
        5: 'ip_address',
        6: 'mac_address',
        8: 'cache_date',
        9: 'memo',
        # Add mappings for other columns here
    }
    #from common.multiprocess import apply_multiprocessing_sort
    order_column = order_column_map.get(order_column_index, 'computer_name')
    if order_column_dir == 'asc':
        user = user.order_by(order_column, '-computer_id')
    else:
        user = user.order_by('-' + order_column, 'computer_id')
    #user = apply_multiprocessing_sort(user, order_column, order_column_dir)


    #멀티프로세싱 적용 x
    #order_column = order_column_map.get(order_column_index, 'computer_name')
    #if order_column_dir == 'asc':
    #    user = sorted(user, key=lambda x: cus_sort(x, order_column))
    #else:
    #    user = sorted(user, key=lambda x: cus_sort(x, order_column), reverse=True)


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

# def custom_sort_key(item, order_column):
#     # item에서 order_column 값을 가져오기
#     if "__" in order_column:
#         parts = order_column.split("__")
#         fk_field = parts[0]
#         related_field = parts[1]
        
#         related_obj = getattr(item, fk_field)
#         if related_obj:
#             value = getattr(related_obj, related_field, "")
#         else:
#             value = ""
#     else:
#         value = getattr(item, order_column, "")
    
#     if not value:
#         return (3, )  # 정의되지 않은 값은 가장 마지막에 위치

#     value = value.lower()  # 대소문자 구분 없이 처리하기 위해 소문자로 변환
#     first_char = value[0] if value else ''
#     # 한글 처리
#     if '가' <= first_char <= '힣':
#         cho = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
#         jung = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        
#         cho_index = next((i for i, c in enumerate(cho) if first_char.startswith(c)), len(cho))
#         jung_index = next((i for i, c in enumerate(jung) if first_char.startswith(c)), len(jung))
        
#         return (0, cho_index, jung_index, value)
    
#     # 영어 처리
#     elif 'a' <= first_char <= 'z':
#         return (1, first_char)
    
#     # 숫자 처리
#     elif '0' <= first_char <= '9':
#         return (2, first_char)
    
#     # 그 외 처리
#     else:
#         return (3, first_char)

@csrf_exempt
def hw_asset_select_all(request):
    data = request
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='HS_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='HS_asset', auth_use='true')
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
        if filter_column == "cache_date":
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today)
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
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
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
                                                      Q(logged_name_id__deptName__icontains=term) |
                                                      Q(logged_name_id__userName__icontains=term) |
                                                      Q(logged_name_id__userId__icontains=term) |
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
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
            users = user.values('chassistype').annotate(count=Count('chassistype'))
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
                                                  Q(logged_name_id__deptName__icontains=term) |
                                                  Q(logged_name_id__userName__icontains=term) |
                                                  Q(logged_name_id__userId__icontains=term) |
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
                             Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
        if filter_value:
            if ' and ' in filter_value:
                search_terms = filter_value.split(' and ')
                query = reduce(operator.and_, [Q(chassistype__icontains=term) |
                                               Q(logged_name_id__deptName__icontains=term) |
                                               Q(logged_name_id__userName__icontains=term) |
                                               Q(logged_name_id__userId__icontains=term) |
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
                                              Q(logged_name_id__deptName__icontains=term) |
                                              Q(logged_name_id__userName__icontains=term) |
                                              Q(logged_name_id__userId__icontains=term) |
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


@csrf_exempt
def sw_asset_select_all(request):
    data = request
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='HS_asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], xfactor_auth_id='HS_asset', auth_use='true')
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
        if filter_column == "cache_date":
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today)
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
                                                       Q(ip_address__icontains=term) |
                                                       Q(sw_list__icontains=term) |
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
                                                       Q(ip_address__icontains=term) |
                                                       Q(sw_list__icontains=term) |
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
                                 Q(memo__icontains=filter_value))
                    user = user.filter(query)
            else:
                user = user
        else:
            query = Q(**{f'{filter_column}__icontains': filter_text})
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
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
                    Q(memo__icontains=filter_value))
                user = user.filter(query)
    else:
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date)
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today).filter(cache_date__gte=start_of_day)
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
