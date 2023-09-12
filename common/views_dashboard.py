import datetime
import json
import logging

import pytz
from django.utils import timezone
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
    discover_data = asset.filter(classification='discover').order_by('-item').values('item', 'item_count')
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
    office_data = asset.filter(classification='office_ver').order_by('-item_count').values('item', 'item_count')
    office_items = [data['item'] for data in office_data]
    office_item_counts = [data['item_count'] for data in office_data]
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
    asset_all_chart_list = [notebook, desktop, others]




    RD = {
        'discover_data_list' : discover_data_list,
        'location_data_list' : location_data_list,
        'hotfix_data_list' : hotfix_data_list,
        'asset_all_chart_list' : asset_all_chart_list,
        'office_data_list' : office_data_list,

    }

    return RD




    #
    # discover_Data = Daily_Statistics.objects.filter(classification='discover')
    # print(discover_Data)
    # discover_data_json = serialize('json', discover_Data)
    # print(type(discover_data_json))
    #
    # update_Data = Daily_Statistics.objects.filter(classification='update')
    # update_Data_json = serialize('json', update_Data)
    # #print(update_Data_json)
    #
    # location_Data = Daily_Statistics.objects.filter(classification='subnet')
    # location_Data_json = serialize('json', location_Data)
    # #print(location_Data_json)




    # local_tz = pytz.timezone('Asia/Seoul')
    # utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    # now = utc_now.astimezone(local_tz)
    # time = now - datetime.timedelta(minutes=7)
    # asset = Daily_Statistics_log.objects.all()
    # asset.filter(item='Desktop').values('item', 'item_count', 'statistics_collection_date')
    # print(asset.filter(item='Desktop').values('item', 'item_count', 'statistics_collection_date'))

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