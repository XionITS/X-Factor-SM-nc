import json

from django.db.models.functions import Concat
from django.http import HttpResponse
import math
import operator
from django.shortcuts import render, redirect
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

#전체 자산 수 차트
@csrf_exempt
def all_asset_paging1(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')

    if request.POST.get('categoryName') == 'Online':
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop'])
        if request.POST.get('seriesName') != 'Other':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                            Q(ip_address__icontains=filter_text) |
                            Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'))

    if request.POST.get('categoryName') == 'Total':
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.all().exclude(chassistype__in=['Notebook', 'Desktop'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                            Q(ip_address__icontains=filter_text) |
                            Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = Xfactor_Common.objects.all().exclude(chassistype__in=['Notebook', 'Desktop'])
        if request.POST.get('seriesName') != 'Other':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName'))
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
            else:
                user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName'))

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'deptName',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address.',
        5: 'mac_address',
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

#전체 자산 수 os별 차트1
@csrf_exempt
def asset_os_paging1(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    print(request.POST.get('categoryName'))
    print(request.POST.get('seriesName'))
    if request.POST.get('categoryName') == 'Other':
        if request.POST.get('seriesName') == 'Desktop':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop']).exclude( os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Mac':
        if request.POST.get('seriesName') == 'Desktop':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop']).exclude( os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Windows':
        if request.POST.get('seriesName') == 'Desktop':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, os_simple='Windows').exclude(chassistype__in=['Notebook', 'Desktop'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'deptName',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address.',
        5: 'mac_address',
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

#전체 자산 수 os별 차트1
@csrf_exempt
def asset_os_paging2(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    print(request.POST.get('categoryName'))
    print(request.POST.get('seriesName'))
    filter_text = request.POST.get('search[value]')
    if request.POST.get('categoryName') == 'Other':
        if request.POST.get('seriesName') == 'Desktop':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.exclude(chassistype__in=['Notebook', 'Desktop']).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Mac':
        if request.POST.get('seriesName') == 'Desktop':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.exclude(chassistype__in=['Notebook', 'Desktop']).exclude( os_simple__in=['Windows', 'Mac'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    if request.POST.get('categoryName') == 'Windows':
        if request.POST.get('seriesName') == 'Desktop':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Notebook':
            user = Xfactor_Common.objects.filter(chassistype=request.POST.get('seriesName'), os_simple='Windows')
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)
        if request.POST.get('seriesName') == 'Other':
            user = Xfactor_Common.objects.filter(os_simple='Windows').exclude(chassistype__in=['Notebook', 'Desktop'])
            if filter_text:
                query = (Q(computer_name__icontains=filter_text) |
                         Q(ip_address__icontains=filter_text) |
                         Q(mac_address__icontains=filter_text))
                user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'deptName',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address.',
        5: 'mac_address',
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


#windows 버전별 자산 목록
@csrf_exempt
def oslistPieChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).annotate(windows_build=Concat('os_total', Value(' '), 'os_build')).filter(windows_build__contains=request.POST.get('categoryName'))
    if filter_text:
        query = (Q(computer_name__icontains=filter_text) |
                 Q(ip_address__icontains=filter_text) |
                 Q(mac_address__icontains=filter_text))
        user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'deptName',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address.',
        5: 'mac_address',
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

#Windows 버전별 자산 현황 차트
@csrf_exempt
def osVerPieChart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    if request.POST.get('categoryName') == '업데이트 완료':
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, os_simple='Windows', os_build__gte='19044')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == '업데이트 필요':
        user = Xfactor_Common.objects.filter(os_simple='Windows', os_build__lt='19044', user_date__gte=today_collect_date)
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'deptName',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address.',
        5: 'mac_address',
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

#Office 버전별 자산 형황 차트
@csrf_exempt
def office_chart(request):
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    filter_text = request.POST.get('search[value]')
    if request.POST.get('categoryName') == 'Office 16 이상':
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, essential5__in=['Office 21', 'Office 19', 'Office 16'])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Office 16 미만':
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, essential5__in='Office 15')
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)
    if request.POST.get('categoryName') == 'Office 설치 안됨':
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date, essential5__in=['unconfirmed', '오피스 없음', ''])
        if filter_text:
            query = (Q(computer_name__icontains=filter_text) |
                     Q(ip_address__icontains=filter_text) |
                     Q(mac_address__icontains=filter_text))
            user = user.filter(query)

    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        1: 'deptName',
        2: 'computer_name',
        3: 'logged_name',
        4: 'ip_address.',
        5: 'mac_address',
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