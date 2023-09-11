import datetime
import json
import logging

import pytz
from django.utils import timezone

from common.models import Xfactor_Common, Daily_Statistics, Daily_Statistics_log

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
    asset = Daily_Statistics_log.objects.all()
    asset.filter(item='Desktop').values('item', 'item_count', 'statistics_collection_date')
    print(asset.filter(item='Desktop').values('item', 'item_count', 'statistics_collection_date'))