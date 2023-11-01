import pytz
from django.db.models.expressions import RawSQL
from django.http import HttpResponse
import math
import operator
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from dateutil.relativedelta import relativedelta
from django.db.models import Max
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from calendar import monthrange
from .models import *
from .serializers import *
import logging
from common.models import *


with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

@csrf_exempt
def create(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='dash_report', auth_use='false')
    print(user_auth)
    if user_auth:
        return redirect('../home/')
    datetime = request.GET.get('datetime')
    #print(datetime)
    selected_date = datetime
    DCDL = report(selected_date)
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    days_150 = DCDL['150_day_ago']
    win_ver = DCDL['win_os_build']
    hotfix = DCDL['necessery']
    os_version_up = DCDL['old']
    Notebook_chassis_total = DCDL['Notebook_chassis_total']
    Desktop_chassis_total = DCDL['Desktop_chassis_total']
    dataList = {
        '150days': days_150,
        'win_ver': win_ver,
        'hotfix': hotfix,
        'os_version_up': os_version_up,
        'Notebook_chassis_total': Notebook_chassis_total,
        'Desktop_chassis_total': Desktop_chassis_total
    }
    context = {'menu_list': unique_items, 'dataList': dataList}
    #print(dataList)
    return render(request, 'report.html', context)

@csrf_exempt
def report(selected_date=None):
    # 장기 미접속 자산 증가율, 업데이트 대상 수 변화량, 보안 패치 대상 수 변화량
    def get_data_for_item(item_value):
        current_data = Daily_Statistics_log.objects.filter(
            statistics_collection_date__year=year,
            statistics_collection_date__month=month,
            statistics_collection_date__day=day,
            statistics_collection_date__hour=hour,
            item=item_value
        ).first()

        prev_month_date = datetime(year, month, day) - relativedelta(months=1)
        first_day_prev_month = datetime(prev_month_date.year, prev_month_date.month, 1)
        last_day_prev_month = datetime(prev_month_date.year, prev_month_date.month, monthrange(prev_month_date.year, prev_month_date.month)[1])

        last_data_in_prev_month = Daily_Statistics_log.objects.filter(
            statistics_collection_date__year=prev_month_date.year,
            statistics_collection_date__month=prev_month_date.month,
            statistics_collection_date__gte=first_day_prev_month,
            statistics_collection_date__lte=last_day_prev_month,
            item=item_value
        ).order_by('-statistics_collection_date').first()

        increase_rate = 0
        increase_amount = 0
        if current_data and last_data_in_prev_month:
            difference = current_data.item_count - last_data_in_prev_month.item_count
            increase_rate = round(((difference / last_data_in_prev_month.item_count) * 100) if last_data_in_prev_month.item_count != 0 else 0, 2)
            increase_amount = difference
        return {
            'current_value': current_data.item_count if current_data else 'null',
            'last_value_in_prev_month': last_data_in_prev_month.item_count if last_data_in_prev_month else 'null',
            'increase_rate': increase_rate,
            'increase_amount': increase_amount
        }

    # Windows 버전별 수 변화량
    def get_win_os_build_data():
        current_data = Daily_Statistics_log.objects.filter(
            statistics_collection_date__year=year,
            statistics_collection_date__month=month,
            statistics_collection_date__day=day,
            statistics_collection_date__hour=hour,
            classification='win_os_build'
        ).order_by('-item_count')[:6]
        prev_month_date = datetime(year, month, day) - relativedelta(months=1)
        last_data_in_prev_month = Daily_Statistics_log.objects.filter(
            statistics_collection_date__year=prev_month_date.year,
            statistics_collection_date__month=prev_month_date.month,
            classification='win_os_build'
        ).order_by('-statistics_collection_date', '-item_count')[:6]
        result_data = []
        for current in current_data:
            matched_data = next((data for data in last_data_in_prev_month if data.item == current.item), None)
            if matched_data:
                difference = current.item_count - matched_data.item_count
                increase_rate = round((difference / matched_data.item_count) * 100 if matched_data and matched_data.item_count != 0 else 100, 2)
            else:
                difference = current.item_count
                increase_rate = 100
            formatted_increase_amount = f"+{difference}" if difference > 0 else difference
            formatted_increase_rate = f"+{increase_rate}" if increase_rate > 0 else increase_rate

            result_data.append({
                'item': current.item,
                'current_value': current.item_count,
                'last_value_in_prev_month': matched_data.item_count if matched_data else 'null',
                'increase_rate': formatted_increase_rate,
                'increase_amount': formatted_increase_amount
            })
        return result_data

    # 월간 자산수 비교
    def get_specific_classification_data(classification_value, item_value):
        current_data = Daily_Statistics_log.objects.filter(
            statistics_collection_date__year=year,
            statistics_collection_date__month=month,
            statistics_collection_date__day=day,
            statistics_collection_date__hour=hour,
            classification=classification_value,
            item=item_value
        ).first()
        prev_month_date = datetime(year, month, day) - relativedelta(months=1)
        last_data_in_prev_month = Daily_Statistics_log.objects.filter(
            statistics_collection_date__year=prev_month_date.year,
            statistics_collection_date__month=prev_month_date.month,
            classification=classification_value,
            item=item_value
        ).order_by('-statistics_collection_date').first()
        increase_rate = 0
        increase_amount = 0
        if current_data and last_data_in_prev_month:
            difference = current_data.item_count - last_data_in_prev_month.item_count
            increase_rate = round(((difference / last_data_in_prev_month.item_count) * 100) if last_data_in_prev_month.item_count != 0 else 0, 2)
            increase_amount = difference
        return {
            'current_value': current_data.item_count if current_data else 'null',
            'last_value_in_prev_month': last_data_in_prev_month.item_count if last_data_in_prev_month else 'null',
            'increase_rate': increase_rate,
            'increase_amount': increase_amount
        }

    year, month, day, hour = map(int, selected_date.split('-'))
    items_to_query = ['150_day_ago', 'old', 'necessery']  # 원하는 item들을 이 리스트에 추가하세요.
    RD = {item: get_data_for_item(item) for item in items_to_query}
    RD['win_os_build'] = get_win_os_build_data()
    RD['Notebook_chassis_total'] = get_specific_classification_data('Notebook_chassis_total', 'Notebook')
    RD['Desktop_chassis_total'] = get_specific_classification_data('Desktop_chassis_total', 'Desktop')
    #print(RD)
    return RD
