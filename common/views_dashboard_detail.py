import json

import pytz
from django.db.models.functions import Concat
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Value, Count
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
local_tz = pytz.timezone('Asia/Seoul')
utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
now = utc_now.astimezone(local_tz)
start_of_today = now.replace(minute=0, second=0, microsecond=0)
start_of_day = start_of_today - timedelta(days=7)
end_of_today = start_of_today + timedelta(minutes=50)
#end_of_day = now.replace(minute=50, second=0, microsecond=0) +timedelta(days=7)



#전체 자산 수 차트
@csrf_exempt
def all_asset_paging1(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    current_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    filter_text = request.POST.get('search[value]')
    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

        print(len(user))
    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)



    if request.POST.get('categoryName') == 'Online':
        if request.POST.get('seriesName') == 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop'])
            user = user.exclude(chassistype__in=['Notebook', 'Desktop'])
            print(user)
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop'])
                user = user.exclude(chassistype__in=['Notebook', 'Desktop'])
        if request.POST.get('seriesName') != 'Other':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))
            user  = user.filter(chassistype=request.POST.get('seriesName'))
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
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
            user = cache.exclude(chassistype__in=['Notebook', 'Desktop'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = cache.exclude(chassistype__in=['Notebook', 'Desktop'])
        if request.POST.get('seriesName') != 'Other':
            user = cache.filter(chassistype=request.POST.get('seriesName'))
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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
        user_list = Cacheserializer(page, many=True).data
    elif request.POST.get('categoryName') == 'Online':
        user_list = Cacheserializer(page, many=True).data
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
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    print(request.POST.get('categoryName'))
    print(request.POST.get('seriesName'))
    if request.POST.get('categoryName') == 'Other':
        if request.POST.get('seriesName') == 'Desktop':
            #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            user = user.filter( chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = user.filter( chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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

#전체 자산 수 os별 차트1
@csrf_exempt
def asset_os_paging2(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    print(request.POST.get('categoryName'))
    print(request.POST.get('seriesName'))

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    filter_text = request.POST.get('search[value]')

    if request.POST.get('categoryName') == 'Other':
        if request.POST.get('seriesName') == 'Desktop':
            user = cache.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user =cache.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = cache.exclude(chassistype__in=['Notebook', 'Desktop']).exclude(os_simple='Windows').exclude(os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = cache.filter(chassistype=request.POST.get('seriesName'), os_simple='Mac')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = cache.filter( os_simple='Mac').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
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
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = cache.filter(chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
                         Q(logged_name_id__userName__icontains=filter_text) |
                         Q(logged_name_id__userId__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = cache.filter(os_simple='Windows').exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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


#windows 버전별 자산 목록
@csrf_exempt
def oslistPieChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, os_total__contains='Windows').annotate(windows_build=Concat('os_total', Value(' '), 'os_build')).filter(windows_build=request.POST.get('categoryName'))
    user = user.filter( os_total__contains='Windows').annotate(windows_build=Concat('os_total', Value(' '), 'os_build')).filter(windows_build=request.POST.get('categoryName'))
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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

#Windows 버전별 자산 현황 차트
@csrf_exempt
def osVerPieChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    if request.POST.get('categoryName') == '업데이트 완료':
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, os_simple='Windows', os_build__gte='19044').exclude(os_total='unconfirmed')
        user = user.filter( os_simple='Windows', os_build__gte='19044').exclude(os_total='unconfirmed')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '업데이트 필요':
        #user = Xfactor_Daily.objects.filter(os_simple='Windows', os_build__lt='19044', user_date__gte=today_collect_date).exclude(os_total='unconfirmed')
        user = user.filter(os_simple='Windows', os_build__lt='19044').exclude(os_total='unconfirmed')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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

#Office 버전별 자산 형황 차트
@csrf_exempt
def office_chart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    if request.POST.get('categoryName') == 'Office 16 이상':
        #user = Xfactor_Daily.objects.filter(user_date__gte=today_collect_date, essential5__in=['Office 21', 'Office 19', 'Office 16'])
        user = user.filter( essential5__in=['Office 21', 'Office 19', 'Office 16'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Office 16 미만':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, essential5='Office 15')
        user = user.filter(essential5='Office 15')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Office 설치 안됨':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today,essential5='오피스 없음')
        user = user.filter(essential5='오피스 없음')
        print(start_of_today)
        print(start_of_today)
        print(start_of_today)
        print(start_of_today)
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
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
                     Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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


#위치별 차트
@csrf_exempt
def subnet_chart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    if request.POST.get('categoryName') == 'VPN':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, subnet__in=['172.21.224.0/20', '192.168.0.0/20'])
        user = user.filter(subnet__in=['172.21.224.0/20', '192.168.0.0/20'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '사내망':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, subnet__in=['172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
        user = user.filter(subnet__in=['172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
                    , '172.18.88.0/21', '172.18.96.0/21', '172.18.104.0/22', '172.20.16.0/21', '172.20.40.0/22', '172.20.48.0/21', '172.20.56.0/21', '172.20.64.0/22', '172.20.68.0/22', '172.20.78.0/23', '172.20.8.0/21'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '미확인':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, subnet='unconfirmed')
        user = user.filter(subnet='unconfirmed')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
                     Q(logged_name_id__userName__icontains=filter_text) |
                     Q(logged_name_id__userId__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '외부망':
        #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today).exclude(subnet__in=['unconfirmed', '172.21.224.0/20', '192.168.0.0/20', '172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
        user = user.exclude(subnet__in=['unconfirmed', '172.21.224.0/20', '192.168.0.0/20', '172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
                    , '172.18.88.0/21', '172.18.96.0/21', '172.18.104.0/22', '172.20.16.0/21', '172.20.40.0/22', '172.20.48.0/21', '172.20.56.0/21', '172.20.64.0/22', '172.20.68.0/22', '172.20.78.0/23', '172.20.8.0/21'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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
def hotfixChart(request):
    three_months_ago = datetime.now() - timedelta(days=90)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    filtered_user_objects = []  # 조건을 만족하는 사용자들을 저장할 리스트
    #user_objects = Xfactor_Daily.objects.filter(user_date__gte=start_of_today)
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
            if latest_date < three_months_ago and request.POST.get('categoryName') == '보안패치 필요':
                filtered_user_objects.append(user['computer_id'])
            elif latest_date >= three_months_ago and request.POST.get('categoryName') == '보안패치 불필요':
                filtered_user_objects.append(user['computer_id'])
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(logged_name_id__deptName=filter_text) |
                 Q(logged_name_id__userName__icontains=filter_text) |
                 Q(logged_name_id__userId__icontains=filter_text) |
                 Q(ip_address__icontains=filter_text) |
                 Q(mac_address__icontains=filter_text))
        filtered_user_objects = user.filter(query)

    user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date, computer_id__in=filtered_user_objects)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'logged_name_id__deptName',
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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
def tcpuChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    user = ''
    cache = ''
    print(request.POST.get('selectedDate'))
    if request.POST.get('selectedDate') != '':

        start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        if start_of_today.date() < datetime(start_of_today.year, 10, 30).date():
            start_date_naive = datetime.strptime(request.POST.get('selectedDate'), "%Y-%m-%d-%H")
            start_of_today2 = timezone.make_aware(start_date_naive) - timedelta(minutes=120)
            end_of_today2 = start_of_today + timedelta(minutes=110)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today2)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today)
        else:
            end_of_today = start_of_today + timedelta(minutes=50)
            # 현재
            user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
            # 토탈
            cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.POST.get('selectedDate') == '':
        start_of_today = now.replace(minute=0, second=0, microsecond=0)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)

        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    #user = Xfactor_Daily.objects.filter(user_date__gte=start_of_today, t_cpu='True')
    user = user.filter(t_cpu='True')
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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
def discoverChart(request):
    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    date_150_days_ago = now - timedelta(days=150)
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    user = Xfactor_Common.objects.filter(user_date__gte=date_150_days_ago)
    filter_text = request.POST.get('search[value]')
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(logged_name_id__deptName=filter_text) |
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
        2: 'computer_name',
        3: 'logged_name_id__userId',
        4: 'ip_address.',
        5: 'mac_address',
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