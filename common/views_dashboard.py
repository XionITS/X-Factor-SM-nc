import datetime
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

def Dashboard():
    logger = logging.getLogger(__name__)
    monthly_asset = []
    today_collect_date = timezone.now() - datetime.timedelta(minutes=DBSettingTime)

    asset = Daily_Statistics.objects.all()
    asset_log = Daily_Statistics_log.objects.all()

    #미관리 자산현황
    discover_data = asset.filter(classification='discover').filter(item='장기 미접속 자산').values('item', 'item_count')
    discover_items = [data['item'] for data in discover_data]
    discover_item_counts = [data['item_count'] for data in discover_data]
    discover_data_list = [discover_items, discover_item_counts]

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
    office_data_old = asset.filter(classification='office_ver', item__in=['Office 15']).aggregate(total=Sum('item_count'))
    if office_data_old['total'] == None:
        office_data_old['total'] = 0
    office_data_none = asset.filter(classification='office_ver', item__in=['unconfiremd', '오피스 없음', '']).aggregate(
        total=Sum('item_count'))
    # office_items = [data['item'] for data in office_data]
    # office_item_counts = [data['item_count'] for data in office_data]
    office_items = ['Office 16 이상', 'Office 16 미만', 'Office 설치 안됨']
    office_item_counts = [office_data_new['total'], office_data_old['total'], office_data_none['total']]
    office_data_list = [office_items, office_item_counts]

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
    #print(others)
    # 온라인 토탈
    # [c1 , c1]
    # [c2 , c2]
    # [c3 , c3]
    asset_all_chart_list = [notebook, desktop, others]    #

    #[1,2]
    #[1.2]
    #[1.2]
    #....

    # win- desk

               #    온라인           토탈

    # win-desk =[on-win-desk,  to-win-desk] win group
    # mac -desk =[on-mac-desk,  to-mac-desk] mac group
    # other -desk[on-other-desk,  to-other-desk] other group

    # win - note[[on-win-note,  to-win-note] win group
    # mac - note[on-mac-note,  to-mac-note]mac group
    # other -note[on-other-note,  to-other-note]other group

    # win - other[on-win-other,  to-win-other] win group
    # mac - other[on-mac-other,  to-mac-other]mac group
    # other -other[on-other-other,  to-other-other]other group




    # local_tz = pytz.timezone('Asia/Seoul')
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # now = utc_now.astimezone(local_tz)
    # time = now - datetime.timedelta(minutes=7)
    asset_log = Daily_Statistics_log.objects.all()
    asset = Daily_Statistics.objects.all()
    service = Xfactor_Service.objects.all()
    common = Xfactor_Common.objects.all()
    daily = Daily_Statistics.objects.all()

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
        used_tcpu = daily.filter(classification='t_cpu').filter(item='True').values('item_count')
        notused_tcpu = daily.filter(classification='t_cpu').filter(item='False').values('item_count')
        cpu_data_list = [used_tcpu[0]['item_count'], notused_tcpu[0]['item_count']]
    except:
        cpu_data_list = [0, notused_tcpu[0]['item_count']]

    # os버전별 자산 현황
    try:
        os_asset = daily.filter(classification='win_os_build').values('item', 'item_count')
        # print(os_asset)
        half_index = len(os_asset) // 2
        first_half = os_asset[:half_index]
        second_half = os_asset[half_index:]
        os_asset_data_list = {'first_half': first_half, 'second_half': second_half}
    except:
        os_asset_data_list = {'first_half': '-', 'second_half': '-'}

    # os버전별 자산 통계 차트
    try:
        os_up = daily.filter(classification='os_version_up').values('item', 'item_count')
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