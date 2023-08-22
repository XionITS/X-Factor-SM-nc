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
#today_collect_date = timezone.now() - timedelta(hours=24, minutes=30)

@csrf_exempt
def ver_asset(request):
    #메뉴
    xuser_auths = XFactor_XUserAuth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = UserAuthSerializer(xuser_auths, many=True)
    #테이블아래 자산현황

    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    local_now = utc_now.astimezone(local_tz)
    # 24시간 30분 이전의 시간 계산
    today_collect_date = local_now - timedelta(hours=24, minutes=30)

    asset = Daily_Statistics.objects.filter(statistics_collection_date__gt=today_collect_date, classification='os_simple').values('item', 'item_count').order_by('-item_count')[:5]
    total_item_count = sum(asset.values_list('item_count', flat=True))

    context = {'menu_list': menu.data, 'asset': asset, 'total_item_count': total_item_count}
    return render(request, 'ver_asset.html', context)

@csrf_exempt
def ver_asset_paging(request):
    default_os = request.POST.get('filter[defaultColumn]')
    filter_column = request.POST.get('filter[column]')
    filter_text = request.POST.get('filter[value]')
    filter_value = request.POST.get('filter[value2]')
    user = XFactor_User.objects.filter(os_total__icontains=default_os).exclude(os_total='unconfirmed').exclude(ip_address='unconfirmed')
    # 현재 시간대 객체 생성, 예시: "Asia/Seoul"
    local_tz = pytz.timezone('Asia/Seoul')
    # UTC 시간대를 사용하여 현재 시간을 얻음
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # 현재 시간대로 시간 변환
    local_now = utc_now.astimezone(local_tz)
    # 24시간 30분 이전의 시간 계산
    today_collect_date = local_now - timedelta(hours=24, minutes=30)

    if filter_text and filter_column:
        query = Q(**{f'{filter_column}__icontains': filter_text})
        user = user.filter(user_date__gt=today_collect_date)
        user = user.filter(query)
        #user = XFactor_User.objects.filter(query)
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
        user = user.filter(user_date__gt=today_collect_date)
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
        1: 'computer_name',
        2: 'ip_address',
        3: 'os_total',
        4: 'os_version',
        5: 'os_build',
        6: 'memo'
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




