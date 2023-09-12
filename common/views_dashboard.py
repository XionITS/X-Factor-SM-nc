import datetime
import json
import logging

import pytz
from django.db.models import Max, Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone

from common.models import Xfactor_Common, Daily_Statistics, Daily_Statistics_log, Xfactor_Service

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

def Dashboard():
    logger = logging.getLogger(__name__)
    monthly_asset = []
    today_collect_date = timezone.now() - datetime.timedelta(minutes=DBSettingTime)
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
    daily_asset_desktop = asset_log.filter(item='Desktop').values('item_count', 'statistics_collection_date')
    daily_asset_laptop = asset_log.filter(item='Notebook').values('item_count', 'statistics_collection_date')
    minutely_asset_desktop = asset.filter(item='Desktop').values('item_count', 'statistics_collection_date')
    minutely_asset_laptop = asset.filter(item='Notebook').values('item_count', 'statistics_collection_date')
    monthly_asset_ditem_count = [entry['item_count'] for entry in daily_asset_desktop]
    monthly_asset_litem_count = [entry['item_count'] for entry in daily_asset_laptop]
    minutely_asset_ditem_count = [entry['item_count'] for entry in minutely_asset_desktop]
    minutely_asset_litem_count = [entry['item_count'] for entry in minutely_asset_laptop]

    monthly_asset_date = [entry['statistics_collection_date'].strftime('%m') + "월" for entry in daily_asset_desktop]
    minutely_asset_date = [entry['statistics_collection_date'].strftime('%m') + "월" for entry in minutely_asset_desktop]
    monthly_asset_data_list = [monthly_asset_ditem_count + minutely_asset_ditem_count, monthly_asset_litem_count + minutely_asset_litem_count, monthly_asset_date + minutely_asset_date]

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
        print(os_up_data_list)
    except:
        os_up_data_list = ['-', '-']

    RD = {
        'monthly_asset_data_list': monthly_asset_data_list,
        'cpu_data_list': cpu_data_list,
        'os_asset_data_list': os_asset_data_list,
        'os_up_data_list': os_up_data_list
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