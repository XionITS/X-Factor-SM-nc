from datetime import datetime, timedelta
import json
import logging

import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from django.db.models import Max, Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
# from datetime import datetime
from django.utils.timezone import now

from common.models import Xfactor_Common, Daily_Statistics, Daily_Statistics_log, Xfactor_Service
from django.core.serializers import serialize
from common.models import *

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

def Dashboard(selected_date=None):
    logger = logging.getLogger(__name__)
    monthly_asset = []
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    if selected_date:
        start_date_naive = datetime.strptime(selected_date, "%Y-%m-%d")
        end_date_naive = start_date_naive + timedelta(days=1) - timedelta(seconds=1)

        start_date = timezone.make_aware(start_date_naive)
        end_date = timezone.make_aware(end_date_naive)

        asset = Daily_Statistics.objects.filter(statistics_collection_date__gte=start_date, statistics_collection_date__lte=end_date)
        asset_log = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=start_date, statistics_collection_date__lte=end_date)
    else:
        asset = Daily_Statistics.objects.all()
        asset_log = Daily_Statistics_log.objects.all()
    service = Xfactor_Service.objects.all()
    common = Xfactor_Common.objects.all()


    #미관리 자산현황
    discover_min = asset.filter(classification='discover').filter(item='장기 미접속 자산').values('item', 'item_count')
    discover_min_list = [[data['item'], data['item_count']] for data in discover_min]
    discover_day = asset_log.filter(classification='discover').filter(item='150_day_ago').values('item', 'item_count')
    discover_day_list = [[data['item'], data['item_count']] for data in discover_day]
    discover_data_list = discover_min_list + discover_day_list

    #위치별 자산현황
    location_data = asset.filter(classification='subnet').order_by('item').values('item', 'item_count')
    location_items = [data['item'] for data in location_data]
    location_item_counts = [data['item_count'] for data in location_data]
    location_data_list = [location_items, location_item_counts]

    # 보안패치 자산현황
    hotfix_data = asset.filter(classification='hotfix').order_by('-item_count').values('item', 'item_count')
    hotfix_items = [data['item'] for data in hotfix_data]
    hotfix_item_counts = [data['item_count'] for data in hotfix_data]
    hotfix_data_list = [hotfix_items, hotfix_item_counts]

    # Office 버전
    # office_data = asset.filter(classification='office_ver').exclude(item='').order_by('-item_count').values('item', 'item_count')
    office_data_new = asset.filter(classification='office_ver', item__in=['Office 21', 'Office 19', 'Office 16']).aggregate(total=Sum('item_count'))
    if office_data_new['total'] == None:
        office_data_new['total'] = 0
    office_data_old = asset.filter(classification='office_ver', item__in=['Office 15']).aggregate(total=Sum('item_count'))
    if office_data_old['total'] == None:
        office_data_old['total'] = 0
    office_data_none = asset.filter(classification='office_ver', item__in=['unconfirmed', '오피스 없음', '']).aggregate(
        total=Sum('item_count'))
    # office_items = [data['item'] for data in office_data]
    # office_item_counts = [data['item_count'] for data in office_data]
    office_items = ['Office 16 이상', 'Office 16 미만', 'Office 설치 안됨']
    office_item_counts = [office_data_new['total'], office_data_old['total'], office_data_none['total']]
    office_data_list = [office_items, office_item_counts]

    ########################################################################################################################################
    # 전체자산수 Online, TOTAL, Chassis type
    #노트북
    notebook_data = asset.filter(classification='chassis_type').filter(item='Notebook').values('item','item_count')
    notebook_data_cache = asset.filter(classification='chassis_type_cache').filter(item='Notebook').values('item','item_count')
    notebook_data_list = [{'item': data['item'], 'count': data['item_count']} for data in notebook_data]
    notebook_data_cache_list = [{'item': data['item'], 'count': data['item_count']} for data in notebook_data_cache]
    notebook = [notebook_data_list, notebook_data_cache_list]
    #print(notebook)
    #데스크탑
    desktop_data = asset.filter(classification='chassis_type').filter(item='Desktop').values('item','item_count')
    desktop_data_cache = asset.filter(classification='chassis_type_cache').filter(item='Desktop').values('item','item_count')
    desktop_data_list = [{'item': data['item'], 'count': data['item_count']} for data in desktop_data]
    desktop_data_cache_list = [{'item': data['item'], 'count': data['item_count']} for data in desktop_data_cache]
    desktop = [desktop_data_list, desktop_data_cache_list]
    #print(desktop)
    #그외
    other_data = asset.filter(classification='chassis_type').exclude(item__in=['Notebook', 'Desktop']).values('item_count')
    other_data_cache  = asset.filter(classification='chassis_type_cache').exclude(item__in=['Notebook', 'Desktop']).values('item_count')
    other_data_sum = sum(data['item_count'] for data in other_data)
    other_data_cache_sum = sum(data['item_count'] for data in other_data_cache)
    other_data_list = {'item': 'Other', 'count': other_data_sum}
    other_data_cache_list = {'item': 'Other', 'count': other_data_cache_sum}
    others = [other_data_list, other_data_cache_list]

    asset_all_chart_list = [notebook, desktop, others]

    ########################################################################################################################################
    # 온라인 차트
    # desktop[other, mac, winodws]
    desk_online_other = asset.filter(classification='Desktop_chassis_online').exclude(item__in=['Windows', 'Mac']).values('item_count')
    desk_online_other_sum = sum(data['item_count'] for data in desk_online_other)
    desk_online_other_list = {'item': 'Other', 'count': desk_online_other_sum}

    desk_online_mac = asset.filter(classification='Desktop_chassis_online').filter(item='Mac').values('item_count')
    desk_online_mac_sum = sum(data['item_count'] for data in desk_online_mac)
    desk_online_mac_list = {'item': 'Mac', 'count': desk_online_mac_sum}

    desk_online_window = asset.filter(classification='Desktop_chassis_online').filter(item='Windows').values('item_count')
    desk_online_window_sum = sum(data['item_count'] for data in desk_online_window)
    desk_online_window_list = {'item': 'Windows', 'count': desk_online_window_sum}

    desk_online_list = [desk_online_other_list, desk_online_mac_list, desk_online_window_list]

    # notebook[other, mac, winodws]
    note_online_other = asset.filter(classification='Notebook_chassis_online').exclude(item__in=['Windows', 'Mac']).values('item_count')
    note_online_other_sum = sum(data['item_count'] for data in note_online_other)
    note_online_other_list = {'item': 'Other', 'count': note_online_other_sum}

    note_online_mac = asset.filter(classification='Notebook_chassis_online').filter(item='Mac').values('item_count')
    note_online_mac_sum = sum(data['item_count'] for data in note_online_mac)
    note_online_mac_list = {'item': 'Mac', 'count': note_online_mac_sum}

    note_online_window = asset.filter(classification='Notebook_chassis_online').filter(item='Windows').values('item_count')
    note_online_window_sum = sum(data['item_count'] for data in note_online_window)
    note_online_window_list = {'item': 'Windows', 'count': note_online_window_sum}

    note_online_list = [note_online_other_list, note_online_mac_list, note_online_window_list]

    # Other[other, mac, winodws]
    other_online_other = asset.filter(classification='Other_chassis_online').exclude(item__in=['Windows', 'Mac']).values('item_count')
    other_online_other_sum = sum(data['item_count'] for data in other_online_other)
    other_online_other_list = {'item': 'Other', 'count': other_online_other_sum}

    other_online_mac = asset.filter(classification='Other_chassis_online').filter(item='Mac').values('item_count')
    other_online_mac_sum = sum(data['item_count'] for data in other_online_mac)
    other_online_mac_list = {'item': 'Mac', 'count': other_online_mac_sum}

    other_online_window = asset.filter(classification='Other_chassis_online').filter(item='Windows').values('item_count')
    other_online_window_sum = sum(data['item_count'] for data in other_online_window)
    other_online_window_list = {'item': 'Windows', 'count': other_online_window_sum}

    other_online_list = [other_online_other_list, other_online_mac_list, other_online_window_list]


########################################################################################################################################
    # 토탈 차트
    # desktop[other, mac, winodws]
    desk_total_other = asset.filter(classification='Desktop_chassis_total').exclude(item__in=['Windows', 'Mac']).values('item_count')
    desk_total_other_sum = sum(data['item_count'] for data in desk_total_other)
    desk_total_other_list = {'item': 'Other', 'count': desk_total_other_sum}

    desk_total_mac = asset.filter(classification='Desktop_chassis_total').filter(item='Mac').values('item_count')
    desk_total_mac_sum = sum(data['item_count'] for data in desk_total_mac)
    desk_total_mac_list = {'item': 'Mac', 'count': desk_total_mac_sum}

    desk_total_window = asset.filter(classification='Desktop_chassis_total').filter(item='Windows').values('item_count')
    desk_total_window_sum = sum(data['item_count'] for data in desk_total_window)
    desk_total_window_list = {'item': 'Windows', 'count': desk_total_window_sum}

    desk_total_list = [desk_total_other_list, desk_total_mac_list, desk_total_window_list]

    # notebook[other, mac, winodws]
    note_total_other = asset.filter(classification='Notebook_chassis_total').exclude(item__in=['Windows', 'Mac']).values('item_count')
    note_total_other_sum = sum(data['item_count'] for data in note_total_other)
    note_total_other_list = {'item': 'Other', 'count': note_total_other_sum}

    note_total_mac = asset.filter(classification='Notebook_chassis_total').filter(item='Mac').values('item_count')
    note_total_mac_sum = sum(data['item_count'] for data in note_total_mac)
    note_total_mac_list = {'item': 'Mac', 'count': note_total_mac_sum}

    note_total_window = asset.filter(classification='Notebook_chassis_total').filter(item='Windows').values('item_count')
    note_total_window_sum = sum(data['item_count'] for data in note_total_window)
    note_total_window_list = {'item': 'Windows', 'count': note_total_window_sum}

    note_total_list = [note_total_other_list, note_total_mac_list, note_total_window_list]
    #print(note_total_list)
    # Other[other, mac, winodws]
    other_total_other = asset.filter(classification='Other_chassis_total').exclude(item__in=['Windows', 'Mac']).values('item_count')
    other_total_other_sum = sum(data['item_count'] for data in other_total_other)
    other_total_other_list = {'item': 'Other', 'count': other_total_other_sum}

    other_total_mac = asset.filter(classification='Other_chassis_total').filter(item='Mac').values('item_count')
    other_total_mac_sum = sum(data['item_count'] for data in other_total_mac)
    other_total_mac_list = {'item': 'Mac', 'count': other_total_mac_sum}

    other_total_window = asset.filter(classification='Other_chassis_total').filter(item='Windows').values('item_count')
    other_total_window_sum = sum(data['item_count'] for data in other_total_window)
    other_total_window_list = {'item': 'Windows', 'count': other_total_window_sum}

    other_total_list = [other_total_other_list, other_total_mac_list, other_total_window_list]
    #print(other_total_list)
    ########################################################################################################################################


    # 월별 자산 변화 수 차트
    lastDay = (now() - relativedelta(months=5)).strftime("%Y-%m-%d")
    lastMonth = pd.date_range(lastDay, periods=5, freq='M').strftime("%Y-%m-%d")
    LM = tuple(lastMonth)
    # print(LM)
    daily_asset_desktop = asset_log.filter(classification='chassis_type').filter(item='Desktop').values('item_count', 'statistics_collection_date')
    daily_asset_laptop = asset_log.filter(classification='chassis_type').filter(item='Notebook').values('item_count', 'statistics_collection_date')
    minutely_asset_desktop = asset.filter(classification='chassis_type').filter(item='Desktop').values('item_count', 'statistics_collection_date')
    minutely_asset_laptop = asset.filter(classification='chassis_type').filter(item='Notebook').values('item_count', 'statistics_collection_date')
    monthly_asset_ditem_count = [entry['item_count'] for entry in daily_asset_desktop]
    monthly_asset_litem_count = [entry['item_count'] for entry in daily_asset_laptop]
    minutely_asset_ditem_count = [entry['item_count'] for entry in minutely_asset_desktop]
    minutely_asset_litem_count = [entry['item_count'] for entry in minutely_asset_laptop]

    monthly_asset_date = [entry['statistics_collection_date'].strftime('%m') + "월" for entry in daily_asset_desktop]
    minutely_asset_date = [entry['statistics_collection_date'].strftime('%m') + "월" for entry in minutely_asset_desktop]
    # monthly_asset_data_list = [monthly_asset_ditem_count + minutely_asset_ditem_count, monthly_asset_litem_count + minutely_asset_litem_count, monthly_asset_date + minutely_asset_date]
    monthly_asset_data_list = [minutely_asset_ditem_count, minutely_asset_litem_count, minutely_asset_date]
    # CPU 사용량 차트
    try:
        used_tcpu = asset.filter(classification='t_cpu').filter(item='True').values('item_count')
        notused_tcpu = asset.filter(classification='t_cpu').filter(item='False').values('item_count')
        cpu_data_list = [used_tcpu[0]['item_count'], notused_tcpu[0]['item_count']]
    except:
        cpu_data_list = [0, 0]

    # os버전별 자산 현황
    try:
        os_asset = asset.filter(classification='win_os_build').values('item', 'item_count')
        # print(os_asset)
        half_index = len(os_asset) // 2
        first_half = os_asset[:half_index]
        second_half = os_asset[half_index:]
        os_asset_data_list = {'first_half': first_half, 'second_half': second_half}
    except:
        os_asset_data_list = {'first_half': '-', 'second_half': '-'}

    # os버전별 자산 통계 차트
    try:
        os_up = asset.filter(classification='os_version_up').values('item', 'item_count')
        os_up_data_list = [entry['item_count'] for entry in os_up]
    except:
        os_up_data_list = ['-', '-']

    RD = {
        'monthly_asset_data_list': monthly_asset_data_list,
        'cpu_data_list': cpu_data_list,
        'os_asset_data_list': os_asset_data_list,
        'os_up_data_list': os_up_data_list,
        'discover_data_list': discover_data_list,
        'location_data_list': location_data_list,
        'hotfix_data_list': hotfix_data_list,
        'asset_all_chart_list': asset_all_chart_list,
        'office_data_list': office_data_list,
        'desk_online_list' : desk_online_list,
        'note_online_list' : note_online_list,
        'other_online_list' : other_online_list,
        'desk_total_list' : desk_total_list,
        'note_total_list' : note_total_list,
        'other_total_list' : other_total_list,



    }
    # 예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시예시
    # try:
    #     wire_pieData = inputDb('wire_pieData')
    #     logger.info('dashboardFunction.py - wire_pieData - Success')
    # except:
    #     logger.warning('dashboardFunction.py - Error Occurred')
    #     logger.warning('Error - wire_pieData')
    #     # -----------------------------상단 물리/가상 파이차트 ------------------------------------
    # try:
    #     virtual_pieData = inputDb('virtual_pieData')
    #     logger.info('dashboardFunction.py - virtual_pieData - Success')
    # except:
    #     logger.warning('dashboardFunction.py - Error Occurred')
    #     logger.warning('Error - virtual_pieData')
    return RD