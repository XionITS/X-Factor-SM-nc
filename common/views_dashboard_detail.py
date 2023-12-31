import json

import pytz
from django.db.models.functions import Concat, Cast
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Value, Count, Max, BigIntegerField, DateTimeField, DateField
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

# start_of_today = now.replace(minute=0, second=0, microsecond=0)
# start_of_day = start_of_today - timedelta(days=7)
# end_of_today = start_of_today + timedelta(minutes=50)
#end_of_day = now.replace(minute=50, second=0, microsecond=0) +timedelta(days=7)



#전체 자산 수 차트
@csrf_exempt
def all_asset_paging1(request):
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    # date_150_days_ago = now - timedelta(days=150)
    # discover_user = Xfactor_Common.objects.values('mac_address').distinct().count()
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    current_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    filter_text = request.POST.get('search[value]')
    user = ''
    cache = ''
    # aa = Xfactor_Xuser.objects.values('x_id')
    # for a in aa:
    #     bb = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=a['x_id'], xfactor_auth_id='deploy')
    #     if bb:
    #         pass
    #     else:
    #         av = Xfactor_Xuser_Auth(xfactor_xuser_id=a['x_id'], xfactor_auth_id='deploy', auth_use='false')
    #         av.save()
    #
    # aaa = Xfactor_Xuser_Group.objects.values('pk')
    # for a in aaa:
    #     b = Xfactor_Xgroup_Auth.objects.filter(xgroup_id=a['pk'], xfactor_auth_id='deploy')
    #     if b:
    #         pass
    #     else:
    #         cc = Xfactor_Xgroup_Auth.objects.filter(xgroup_id=a['pk']).values('xfactor_xgroup').distinct()
    #         for c in cc:
    #             ca = Xfactor_Xgroup_Auth(xfactor_xgroup=c['xfactor_xgroup'], xfactor_auth_id='deploy', auth_use='false', xgroup_id=a['pk'])
    #             ca.save()
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':
        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=59)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=59)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        # 출력 형식을 설정합니다.
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=59)
        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if request.POST.get('categoryName') == 'Online':
        if request.POST.get('seriesName') == 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop'])
            user = user.exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            #print(user)
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop'])
                user = user.exclude(chassistype='Notebook').exclude(chassistype='Desktop')
        if request.POST.get('seriesName') != 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))
            user  = user.filter(chassistype=request.POST.get('seriesName'))
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))
                user = user.filter(chassistype=request.POST.get('seriesName'))

    if request.POST.get('categoryName') == 'Total':
        if request.POST.get('seriesName') == 'Other':
            user = cache.exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = cache.exclude(chassistype='Notebook').exclude(chassistype='Desktop')
        if request.POST.get('seriesName') != 'Other':
            user = cache.filter(chassistype=request.POST.get('seriesName'))
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = cache.filter(chassistype=request.POST.get('seriesName'))

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'os_simple'
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
    if request.POST.get('categoryName') == 'Total':
        user_list = CommonSerializer(page, many=True).data
    elif request.POST.get('categoryName') == 'Online':
        user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

#전체 자산 수 os별 차트1
@csrf_exempt
def asset_os_paging1(request):
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)

        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    #print(request.POST.get('categoryName'))
    #print(request.POST.get('seriesName'))
    if request.POST.get('categoryName') == 'Other':
        if request.POST.get('seriesName') == 'Desktop':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            user = user.filter( chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = user.filter( chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop']).exclude(os_simple='Windows').exclude(os_simple='Mac')
            user = user.exclude(chassistype__in=['Notebook', 'Desktop']).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Mac':
        if request.POST.get('seriesName') == 'Desktop':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'), os_simple='Mac')
            user = user.filter( chassistype=request.POST.get('seriesName'), os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'), os_simple='Mac')
            user =user.filter(chassistype=request.POST.get('seriesName'), os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, os_simple='Mac').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            user = user.filter(os_simple='Mac').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Windows':
        if request.POST.get('seriesName') == 'Desktop':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'), os_simple='Windows')
            user = user.filter( chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'), os_simple='Windows')
            user = user.filter(chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, os_simple='Windows').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            user = user.filter( os_simple='Windows').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'os_simple'
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

#전체 자산 수 os별 차트1
@csrf_exempt
def asset_os_paging2(request):
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)

    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    #print(request.POST.get('categoryName'))
    #print(request.POST.get('seriesName'))

    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)

        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    filter_text = request.POST.get('search[value]')

    if request.POST.get('categoryName') == 'Other':
        if request.POST.get('seriesName') == 'Desktop':
            user = cache.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user =cache.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = cache.exclude(chassistype__in=['Notebook', 'Desktop']).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Mac':
        if request.POST.get('seriesName') == 'Desktop':
            user = cache.filter( chassistype=request.POST.get('seriesName'), os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = cache.filter(chassistype=request.POST.get('seriesName'), os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = cache.filter( os_simple='Mac').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Windows':
        if request.POST.get('seriesName') == 'Desktop':
            user = cache.filter(chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = cache.filter(chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = cache.filter(os_simple='Windows').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(os_simple__icontains=filter_text) |
                         Q(logged_name_id__deptName__icontains=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'os_simple',
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


#windows 버전별 자산 목록
@csrf_exempt
def oslistPieChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':
        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, os_total__contains='Windows').annotate(windows_build=Concat('os_total', Value(' '), 'os_build')).filter(windows_build=request.POST.get('categoryName'))
    user = user.filter(os_simple='Windows', os_total__contains='Windows').annotate(windows_build=Concat('os_total', Value(' '), 'os_build')).filter(windows_build=request.POST.get('categoryName'))
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(os_build__icontains=filter_text) |
                 Q(logged_name_id__deptName__icontains=filter_text) |
                 Q(logged_name_id__userName__icontains=filter_text) |
                 Q(logged_name_id__userId__icontains=filter_text) |
                 Q(ip_address__icontains=filter_text) |
                 Q(mac_address__icontains=filter_text))
        user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'os_build'
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

#Windows 버전별 자산 현황 차트
@csrf_exempt
def osVerPieChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')

        # 세팅값 변수처리 부분
        ver_current = Daily_Statistics_log.objects.filter(item='ver_web').filter(statistics_collection_date__gte=start_of_today, statistics_collection_date__lt=end_of_today).order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if ver_current == None:
            ver_current = 19044


        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today).exclude(os_build='')
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 세팅값 변수처리 부분
        ver_current = Daily_Statistics_log.objects.filter(item='ver_web').order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if ver_current == None:
            ver_current = 19044
        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).exclude(os_build='')
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if request.POST.get('categoryName') == '업데이트 완료':
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, os_simple='Windows', os_build__gte='19044').exclude(os_total='unconfirmed')


        #user = user.filter( os_simple='Windows', os_build__gt=ver_current).exclude(os_total='unconfirmed')
        user = user.annotate(os_build_cast=Cast('os_build', BigIntegerField())).filter( os_simple='Windows', os_build_cast__gte=ver_current).exclude(os_total='unconfirmed')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(os_build__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '업데이트 필요':
        #user = Xfactor_Daily.objects.filter(os_simple='Windows', os_build__lt='19044', user_date__gte=today_collect_date).exclude(os_total='unconfirmed')
        user = user.annotate(os_build_cast=Cast('os_build', BigIntegerField())).filter( os_simple='Windows', os_build_cast__lt=ver_current).exclude(os_total='unconfirmed')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(os_build__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'os_build_cast'
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

#Office 버전별 자산 형황 차트
@csrf_exempt
def office_chart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if request.POST.get('categoryName') == 'Office 365':
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, essential5__in=['Office 21', 'Office 19', 'Office 16'])
        user = user.filter(essential5__startswith='Office 365')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(essential5__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Office 365 외':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, essential5='Office 15')
        user = user.filter(essential5__in=['Office 21', 'Office 19', 'Office 16','Office 15','Office 2021', 'Office 2019', 'Office 2016', 'Office 2013', 'Office 2010', 'Office 2007', 'Office 2003'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(essential5__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Mac Office':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, essential5__in=['unconfirmed', ''])
        user =user.exclude(essential5__startswith="Office 365").exclude(essential5__in=['Office 365','Office 21', 'Office 19', 'Office 16','Office 15','Office 2021', 'Office 2019', 'Office 2016', 'Office 2013', 'Office 2010', 'Office 2007', 'Office 2003','오피스 없음','unconfirmed', ''])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(essential5__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Office 설치 안됨':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today,essential5='오피스 없음')
        user = user.filter(essential5='오피스 없음')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(essential5__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '미확인':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, essential5__in=['unconfirmed', ''])
        user =user.filter(essential5__in=['unconfirmed', ''])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(essential5__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)



    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'essential5'
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


#위치별 차트
@csrf_exempt
def subnet_chart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common.objects.filter(user_date__gte=start_of_day)

    if request.POST.get('categoryName') == 'VPN':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, subnet__in=['172.21.224.0/20', '192.168.0.0/20'])
        user = user.filter(subnet__in=['172.21.224.0/20','VPN','192.168.0.0/20'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(subnet__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '사내망':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, subnet__in=['172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
        user = user.filter(subnet__in=['172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
                    , '172.18.88.0/21', '172.18.96.0/21', '172.18.104.0/22', '172.20.16.0/21', '172.20.40.0/22', '172.20.48.0/21', '172.20.56.0/21', '172.20.64.0/22', '172.20.68.0/22', '172.20.78.0/23', '172.20.8.0/21','사내망'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(subnet__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '미확인':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, subnet='unconfirmed')
        user = user.filter(subnet__in=['unconfirmed','','Other'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(subnet__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '외부망':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today).exclude(subnet__in=['unconfirmed', '172.21.224.0/20', '192.168.0.0/20', '172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
        user = user.exclude(subnet__in=['사내망','VPN','unconfirmed', '', 'Other', '172.21.224.0/20','192.168.0.0/20', '172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
                    , '172.18.88.0/21', '172.18.96.0/21', '172.18.104.0/22', '172.20.16.0/21', '172.20.40.0/22', '172.20.48.0/21', '172.20.56.0/21', '172.20.64.0/22', '172.20.68.0/22', '172.20.78.0/23', '172.20.8.0/21'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(subnet__icontains=filter_text) |
                     Q(logged_name_id__deptName__icontains=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'subnet'
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
def hotfixChart(request):
    user = ''
    cache = ''
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    filtered_user_objects = []  # 조건을 만족하는 사용자들을 저장할 리스트
    if request.POST.get('selectedDate') != '':
        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)

        index_time = start_date_naive.strftime('%Y-%m-%d-%H')

        # 세팅값 변수처리 부분
        hot_current = Daily_Statistics_log.objects.filter(item='hot_web').filter(statistics_collection_date__gte=start_of_today, statistics_collection_date__lt=end_of_today).order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if hot_current == None:
            hot_current = 90
        three_months_ago = datetime.now() - timedelta(days=hot_current)
        three_months_ago = three_months_ago.strftime('%Y-%m-%d')
        # 현재
        user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today).exclude(hotfix_date='unconfirmed')

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 세팅값 변수처리 부분
        hot_current = Daily_Statistics_log.objects.filter(item='hot_web').order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if hot_current == None:
            hot_current = 90
        three_months_ago = datetime.now() - timedelta(days=hot_current)
        three_months_ago = three_months_ago.strftime('%Y-%m-%d')
        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today).exclude(hotfix_date='unconfirmed')
    # user_objects = Xfactor_Daily.objects.filter(user_date__gte=start_of_today)
    user_objects = user
    users_values = user_objects.values('hotfix_date', 'computer_id')
    for i, user in enumerate(users_values):
        date_strings = user['hotfix_date'].split('<br> ')
        date_objects = []
        for date_str in date_strings:
            try:
                date_obj = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
                date_objects.append(date_obj)
            except ValueError:
                continue
        if date_objects:
            latest_date = max(date_objects)
            latest_date = latest_date.strftime('%Y-%m-%d')
            # print(three_months_ago)
            # print(type(three_months_ago))
            #
            # print("aaaaa")
            # print(latest_date)
            # print(type(latest_date))
            if latest_date <= three_months_ago and request.POST.get('categoryName') == '보안패치 필요':
                filtered_user_objects.append(user['computer_id'])
            elif latest_date > three_months_ago and request.POST.get('categoryName') == '보안패치 불필요':
                filtered_user_objects.append(user['computer_id'])
    user = user_objects.filter(computer_id__in=filtered_user_objects)
    # if request.POST.get('selectedDate') != '':
    #     start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
    #     start_of_today = timezone.make_aware(start_date_naive)
    #     end_of_today = start_of_today + timedelta(minutes=50)
    #
    #     # 현재
    #     user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today, computer_id__in=filtered_user_objects)
    #
    # elif request.POST.get('selectedDate') == '':
    #     start_of_today1 = now.strftime('%Y-%m-%d %H')
    #     start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
    #     start_of_today = timezone.make_aware(start_of_today2)
    #     start_of_day = start_of_today - timedelta(days=7)
    #     end_of_today = start_of_today + timedelta(minutes=50)
    #     # 현재
    #     user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today, computer_id__in=filtered_user_objects)

    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(hotfix_date__icontains=filter_text) |
                 Q(logged_name_id__deptName__icontains=filter_text) |
                 Q(logged_name_id__userName__icontains=filter_text) |
                 Q(ip_address__icontains=filter_text) |
                 Q(mac_address__icontains=filter_text))
        user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'hotfix_date'
        # Add mappings for other columns here
    }
    order_column = order_column_map.get(order_column_index, 'computer_name')

    if order_column == 'hotfix_date':
        print("----------------")
        for a in user:
            date_strings = a.hotfix_date.split('<br>')
            date_strings = [date.strip() for date in date_strings if date.strip()]
            date_objects = [datetime.strptime(date.split(' ')[0], '%m/%d/%Y') for date in date_strings]
            latest_date = max(date_objects)
            latest_date_formatted = latest_date.strftime('%Y-%m-%d')
            a.latest_hotfix_date = latest_date_formatted  # 새로운 필드 생성


        # user를 latest_hotfix_date 필드를 기준으로 정렬
        if order_column_dir == 'asc':
            user = sorted(user, key=lambda x: x.latest_hotfix_date or '0000-00-00')
        else:
            user = sorted(user, key=lambda x: x.latest_hotfix_date or '9999-99-99', reverse=True)


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
    user_list = Cacheserializer3(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)


@csrf_exempt
def tcpuChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    #print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        index_time = start_date_naive.strftime('%Y-%m-%d-%H')
        if start_of_today.date() < datetime(2023, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            index_time = start_date_naive.strftime('%Y-%m-%d-%H')
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(essential2=index_time).filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        # 토탈
        #cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, t_cpu='True')
    user = user.filter(t_cpu='True')
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(logged_name_id__deptName__icontains=filter_text) |
                 Q(logged_name_id__userName__icontains=filter_text) |
                 Q(ip_address__icontains=filter_text) |
                 Q(mac_address__icontains=filter_text))
        user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 't_cpu'
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

#장기 미접속 차트
@csrf_exempt
def discoverChart(request):
    #print(request.POST.get('selectedDate'))
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    filter_text = request.POST.get('search[value]')
    start_of_today1 = now.strftime('%Y-%m-%d %H')
    start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
    start_of_today = timezone.make_aware(start_of_today2)  # 현재 시간대
    end_of_today = start_of_today + timedelta(minutes=50)  # 현재 시간대 + 50분
    if request.POST.get('selectedDate') != '':
        select_now = datetime.strptime(request.POST.get('selectedDate'), '%Y-%m-%d-%H')
        start_of_today1_sel = select_now.strftime('%Y-%m-%d %H')
        start_of_today2_sel = datetime.strptime(start_of_today1_sel, '%Y-%m-%d %H')
        start_of_today_sel = timezone.make_aware(start_of_today2_sel) #선택한 시간대
        end_of_today_sel = start_of_today_sel + timedelta(minutes=50) #선택한 시간대 + 50분

        # 세팅값 변수처리 부분
        discover_current = Daily_Statistics_log.objects.filter(item='discover_web').filter(statistics_collection_date__gte=start_of_today_sel, statistics_collection_date__lt=end_of_today_sel).order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if discover_current == None:
            discover_current = 150
        date_150_days_ago = start_of_today_sel - timedelta(days=discover_current) #선택한 시간대로부터 150일 전 시간대
        date_180_days_ago = date_150_days_ago - timedelta(days=30) #선택한 시간대로부터 150일 전 시간대

        discover_current_1day = Daily_Statistics_log.objects.filter(item='discover_web').filter(statistics_collection_date__gte=start_of_today_sel - timedelta(days=1) , statistics_collection_date__lt=end_of_today_sel - timedelta(days=1)).order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if discover_current_1day == None:
            discover_current_1day = 150
        date_150_days_ago_1day = start_of_today_sel - timedelta(days=discover_current_1day)
        date_180_days_ago_1day = date_150_days_ago_1day - timedelta(days=30)
    elif request.POST.get('selectedDate') == '':
        # 세팅값 변수처리 부분
        discover_current = Daily_Statistics_log.objects.filter(item='discover_web').order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if discover_current == None:
            discover_current = 150
        date_150_days_ago = start_of_today - timedelta(days=discover_current) #현재로부터 150일 전 시간대
        date_180_days_ago = date_150_days_ago - timedelta(days=30)

        discover_current_1day = Daily_Statistics_log.objects.filter(item='discover_web').filter(statistics_collection_date__gte=start_of_today - timedelta(days=1) , statistics_collection_date__lt=end_of_today - timedelta(days=1)).order_by('-statistics_collection_date').values_list('item_count', flat=True).first()
        if discover_current_1day == None:
            discover_current_1day = 150
        date_150_days_ago_1day = start_of_today - timedelta(days=discover_current_1day)
        date_180_days_ago_1day = date_150_days_ago_1day - timedelta(days=30)

    if request.POST.get('categoryName') == '1일 전':

        date_150_yesterday_ago = date_150_days_ago_1day - timedelta(days=1)
        date_180_yesterday_ago = date_180_days_ago_1day - timedelta(days=1)
        #user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__lt=date_150_yesterday_ago)
        #print('1일 전', date_150_yesterday_ago)
        filtered_records = (
            Xfactor_Common.objects
            .filter(user_date__gte=date_180_yesterday_ago, user_date__lt=date_150_yesterday_ago)
        )
        base = Xfactor_Common.objects.exclude(user_date__lt=date_150_yesterday_ago)
        user = filtered_records.exclude(mac_address__in=base.values('mac_address'))
    if request.POST.get('categoryName') == '현재':
        #print('현재', date_150_days_ago)
        #print(date_150_days_ago)
        #user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__lt=date_150_days_ago)
        filtered_records = (
            Xfactor_Common.objects
            .filter(user_date__gte=date_180_days_ago, user_date__lt=date_150_days_ago)
        )
        base = Xfactor_Common.objects.exclude(user_date__lt=date_150_days_ago)
        user = filtered_records.exclude(mac_address__in=base.values('mac_address'))
        #print(user.count())

    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(cache_date__icontains=filter_text) |
                 Q(logged_name_id__deptName__icontains=filter_text) |
                 Q(logged_name_id__userName__icontains=filter_text) |
                 Q(ip_address__icontains=filter_text) |
                 Q(mac_address__icontains=filter_text))
        user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'logged_name_id__userName',
        3: 'computer_name',
        4: 'ip_address',
        5: 'mac_address',
        6: 'user_date'
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
    user_list = CommonSerializer(page, many=True).data
    # Prepare the response

    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)
