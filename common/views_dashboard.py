from datetime import datetime, timedelta
import json
import logging

import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta
from django.db.models import Max, Sum, Count, Q, Subquery, OuterRef
from django.db.models.functions import TruncMonth
from django.utils import timezone
# from datetime import datetime
from django.utils.timezone import now

from common.models import Xfactor_Common, Daily_Statistics, Daily_Statistics_log
from django.core.serializers import serialize
from common.models import *

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

def Dashboard(selected_date=None):
    logger = logging.getLogger(__name__)
    monthly_asset = []
    today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
    yesterday_collect_date = timezone.now() - timedelta(days=1)
    asset = Daily_Statistics.objects.all()
    if selected_date:
        start_date_naive = datetime.strptime(selected_date, "%Y-%m-%d-%H")
        start_date = timezone.make_aware(start_date_naive)
        end_date = start_date + timedelta(hours=1)
        asset_log = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=start_date, statistics_collection_date__lt=end_date)
        asset_log_prev = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=start_date - timedelta(days=1), statistics_collection_date__lt=end_date - timedelta(days=1))
        #print("selected_Date있음")
    else:
        latest_date = Daily_Statistics_log.objects.latest('statistics_collection_date').statistics_collection_date
        previous_date = latest_date - timedelta(days=1)
        start_time = timezone.datetime(latest_date.year, latest_date.month, latest_date.day, latest_date.hour, tzinfo=timezone.utc)
        end_time = start_time + timedelta(hours=1)
        asset_log = Daily_Statistics_log.objects.filter(statistics_collection_date__gte=start_time, statistics_collection_date__lt=end_time)
        asset_log_prev = Daily_Statistics_log.objects.filter(statistics_collection_date__date=previous_date)
        #print("selected_Date없음")

    discover_min = asset_log.filter(item='150_day_ago').first()
    discover_min_list = []
    if discover_min:
        discover_min_datetime = timezone.localtime(discover_min.statistics_collection_date)
        target_datetime = discover_min_datetime - timedelta(days=1)
        target_date = target_datetime.date()
        target_hour = target_datetime.hour
        discover_min_list = [[discover_min.item + '_min', discover_min.item_count]]
    else:
        target_datetime = timezone.localtime() - timedelta(days=1)
        target_date = target_datetime.date()
        target_hour = target_datetime.hour

    discover_day = asset_log_prev.filter(statistics_collection_date__date=target_date, statistics_collection_date__hour=target_hour, item='150_day_ago').first()
    discover_day_list = []
    if discover_day:
        discover_day_list = [[discover_day.item + '_day', discover_day.item_count]]

    discover_data_list = discover_min_list + discover_day_list
    #print(discover_data_list)
    #위치별 자산현황
    location_data = asset_log.filter(classification='subnet').order_by('item').values('item', 'item_count')
    location_items = [data['item'] for data in location_data]
    location_item_counts = [data['item_count'] for data in location_data]
    location_data_list = [location_items, location_item_counts]

    # 보안패치 자산현황
    hotfix_rename = {
        'unnecessery': '보안패치 불필요',
        'necessery': '보안패치 필요'
    }
    hotfix_data = asset_log.filter(classification='hotfix').order_by('-item_count').values('item', 'item_count')
    hotfix_items = [hotfix_rename.get(data['item'], data['item']) for data in hotfix_data]
    hotfix_item_counts = [data['item_count'] for data in hotfix_data]
    hotfix_data_list = [hotfix_items, hotfix_item_counts]

    # Office 버전
    # office_data = asset.filter(classification='office_ver').exclude(item='').order_by('-item_count').values('item', 'item_count')
    office_data_new = asset_log.filter(classification='office_ver', item__in=['Office 21', 'Office 19', 'Office 16']).aggregate(total=Sum('item_count'))
    if office_data_new['total'] == None:
        office_data_new['total'] = 0
    office_data_old = asset_log.filter(classification='office_ver', item='Office 15').aggregate(total=Sum('item_count'))
    if office_data_old['total'] == None:
        office_data_old['total'] = 0
    office_data_none = asset_log.filter(classification='office_ver', item__in=['unconfirmed', '오피스 없음', '']).aggregate(
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
    if len(notebook_data_list) == 0:
        notebook_data_list = [{'item': 'Notebook', 'count': 0}]
    if len(notebook_data_cache_list) == 0:
        notebook_data_cache_list = [{'item': 'Notebook', 'count': 0}]
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
    #asset_log = Daily_Statistics_log.objects.all()
    lastDay = (now() - relativedelta(months=5)).strftime("%Y-%m-%d")
    lastMonth = pd.date_range(lastDay, periods=5, freq='M').strftime("%Y-%m-%d")
    LM = tuple(lastMonth)
    latest_dates_desktop1 = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date__date=LM[0]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_desktop2 = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date__date=LM[1]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_desktop3 = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date__date=LM[2]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_desktop4 = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date__date=LM[3]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_desktop5 = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date__date=LM[4]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_laptop1 = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date__date=LM[0]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_laptop2 = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date__date=LM[1]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_laptop3 = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date__date=LM[2]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_laptop4 = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date__date=LM[3]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')
    latest_dates_laptop5 = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date__date=LM[4]).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('max_date')

    if latest_dates_desktop1 and 'max_date' in latest_dates_desktop1[0]:
        max_date = latest_dates_desktop1[0]['max_date']
        latest_dates_desktop1C = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_desktop1C = 0
    if latest_dates_desktop2 and 'max_date' in latest_dates_desktop2[0]:
        max_date = latest_dates_desktop2[0]['max_date']
        latest_dates_desktop2C = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_desktop2C = 0
    if latest_dates_desktop3 and 'max_date' in latest_dates_desktop3[0]:
        max_date = latest_dates_desktop3[0]['max_date']
        latest_dates_desktop3C = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_desktop3C = 0
    if latest_dates_desktop4 and 'max_date' in latest_dates_desktop4[0]:
        max_date = latest_dates_desktop4[0]['max_date']
        latest_dates_desktop4C = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_desktop4C = 0
    if latest_dates_desktop5 and 'max_date' in latest_dates_desktop5[0]:
        max_date = latest_dates_desktop5[0]['max_date']
        latest_dates_desktop5C = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_desktop5C = 0

    if latest_dates_laptop1 and 'max_date' in latest_dates_laptop1[0]:
        max_date = latest_dates_laptop1[0]['max_date']
        latest_dates_laptop1C = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_laptop1C = 0
    if latest_dates_laptop2 and 'max_date' in latest_dates_laptop2[0]:
        max_date = latest_dates_laptop2[0]['max_date']
        latest_dates_laptop2C = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_laptop2C = 0
    if latest_dates_laptop3 and 'max_date' in latest_dates_laptop3[0]:
        max_date = latest_dates_laptop3[0]['max_date']
        latest_dates_laptop3C = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_laptop3C = 0
    if latest_dates_laptop4 and 'max_date' in latest_dates_laptop4[0]:
        max_date = latest_dates_laptop4[0]['max_date']
        latest_dates_laptop4C = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_laptop4C = 0
    if latest_dates_laptop5 and 'max_date' in latest_dates_laptop5[0]:
        max_date = latest_dates_laptop5[0]['max_date']
        latest_dates_laptop5C = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date=max_date).values('item_count')[0]['item_count']
    else:
        latest_dates_laptop5C = 0

    # latest_dates_desktop1 = asset_log.filter(classification='Desktop_chassis_total', item='Desktop').filter(statistics_collection_date__date__in=LM).values('statistics_collection_date', 'item_count')
    latest_dates_laptop = asset_log.filter(classification='Notebook_chassis_total', item='Notebook').filter(statistics_collection_date__date__in=LM).annotate(month=TruncMonth('statistics_collection_date')).values('month').annotate(max_date=Max('statistics_collection_date')).values('item_count')
    latest_dates_desktop = latest_dates_desktop1 | latest_dates_desktop2 | latest_dates_desktop3 | latest_dates_desktop4| latest_dates_desktop5
    monthly_asset_ditem_count = [latest_dates_desktop1C, latest_dates_desktop2C, latest_dates_desktop3C, latest_dates_desktop4C, latest_dates_desktop5C]
    monthly_asset_litem_count = [latest_dates_laptop1C, latest_dates_laptop2C, latest_dates_laptop3C, latest_dates_laptop4C, latest_dates_laptop5C]
    minutely_asset_desktop = asset.filter(classification='Desktop_chassis_total').aggregate(total_item_count=Sum('item_count'))
    minutely_asset_laptop = asset.filter(classification='Notebook_chassis_total').aggregate(total_item_count=Sum('item_count'))
    if minutely_asset_laptop['total_item_count'] == None:
        minutely_asset_laptop['total_item_count'] = 0
    minutely_asset_date = asset.filter(classification='Desktop_chassis_total').values('statistics_collection_date').first()
    date1 = datetime.strptime(LM[0], '%Y-%m-%d').strftime('%m')+'월'
    date2 = datetime.strptime(LM[1], '%Y-%m-%d').strftime('%m')+'월'
    date3 = datetime.strptime(LM[2], '%Y-%m-%d').strftime('%m')+'월'
    date4 = datetime.strptime(LM[3], '%Y-%m-%d').strftime('%m')+'월'
    date5 = datetime.strptime(LM[4], '%Y-%m-%d').strftime('%m')+'월'
    monthly_asset_date = [date1, date2, date3, date4, date5]
    # monthly_asset_date = [entry['max_date'].strftime('%m') + "월" for entry in latest_dates_desktop]
    minutely_asset_date = minutely_asset_date['statistics_collection_date'].strftime('%m') + "월"
    monthly_asset_data_list = [monthly_asset_ditem_count+[minutely_asset_desktop['total_item_count']], monthly_asset_litem_count+[minutely_asset_laptop['total_item_count']], monthly_asset_date+[minutely_asset_date]]
    # CPU 사용량 차트
    try:
        used_tcpu = asset.filter(classification='t_cpu').filter(item='True').values('item_count')
        notused_tcpu = asset.filter(classification='t_cpu').filter(item='False').values('item_count')
        cpu_data_list = [used_tcpu[0]['item_count'], notused_tcpu[0]['item_count']]
    except:
        cpu_data_list = [0, 0]

    # os버전별 자산 현황
    try:
        os_asset_data_list = asset.filter(classification='win_os_build').values('item', 'item_count')
        os_asset_data_name_list = [entry['item'] for entry in os_asset_data_list]
        os_asset_data_count_list = [[entry['item_count'] for entry in os_asset_data_list]] + [os_asset_data_name_list]
        # print(os_asset_data_count_list)
    except:
        os_asset_data_list = {'item': '-', 'item_count': '-'}

    # os버전별 자산 통계 차트
    try:
        os_up = asset.filter(classification='os_version_up').values('item', 'item_count')
        os_up_data_list = [entry['item_count'] for entry in os_up]
    except:
        os_up_data_list = ['-', '-']

    RD = {
        'monthly_asset_data_list': monthly_asset_data_list,
        'cpu_data_list': cpu_data_list,
        'os_asset_data_list': list(os_asset_data_list),
        'os_asset_data_count_list': os_asset_data_count_list,
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