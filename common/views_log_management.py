import pytz
from django.db.models.expressions import RawSQL
from django.http import HttpResponse
import math
import operator
import json
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from functools import reduce
from datetime import datetime, timedelta
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage
from .models import *
from .serializers import *

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)

@csrf_exempt
def log(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                 xfactor_auth_id='settings', auth_use='false')
    print(user_auth)
    if user_auth:
        return redirect('../home/')
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    context = {'menu_list': unique_items}
    return render(request, 'log_management.html', context)


@csrf_exempt
def log_paging(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                 xfactor_auth_id='settings', auth_use='false')
    print(user_auth)
    if user_auth:
        return redirect('../../home/')
    korean_tz = pytz.timezone('Asia/Seoul')
    logs = Xfactor_Log.objects.order_by('-log_date')
    formatted_logs = [
        {
            'log_func': log.log_func,
            'log_item': log.log_item,
            'log_result': log.log_result,
            'log_user': log.log_user,
            'log_date': log.log_date.astimezone(korean_tz).strftime("%Y-%m-%d %H:%M:%S")
        }
        for log in logs
    ]
    # Get start and length parameters from DataTables AJAX request
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))  # Default to 10 items per page

    # Paginate the queryset
    paginator = Paginator(formatted_logs, length)
    page_number = (start // length) + 1

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Serialize the paginated data
    #user_list = LimitedCommonSerializer(page, many=True).data
    user_list = XfactorLogserializer(page, many=True).data
    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)