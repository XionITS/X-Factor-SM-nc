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
def asset(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='Asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'],
                                                    xfactor_auth_id='Asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../home/')
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    context = {'menu_list': unique_items}
    return render(request, 'asset.html', context)



@csrf_exempt
def search(request):
    if request.method == "POST":
        today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
        search_text = request.POST.get('searchText', None)
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date, cache_date__gte=today_collect_date).filter(computer_name=search_text)
        #print(user)
        #print("11")
        user_data = Cacheserializer(user, many=True).data
        #print(user_data.data)
        # response = {
        #     'data': user_data,  # Serialized data for the current page
        # }
        return JsonResponse({'data': user_data})


@csrf_exempt
def search_box(request):
    if request.method == "POST":
        today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
        search_text = request.POST.get('searchText', None)
        user_data = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).filter(computer_name__icontains=search_text).values('computer_name')
        # user_data = XfactorServiceserializer(user, many=True).data
        return JsonResponse({'data': list(user_data)})


@csrf_exempt
def save_memo(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='Asset', auth_use='true')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'],
                                                    xfactor_auth_id='Asset', auth_use='true')
    if not user_auth and not group_auth:
        return redirect('../../home/')
    if request.method =='POST':
        memo = request.POST.get('memo')
        today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
        largest_time = timezone.make_aware(datetime.max, timezone.utc)
        computername = request.POST.get('computername')
        macaddress = request.POST.get('macaddress')
        try:
            # X-Factor_Common 오브젝트 가져오기
            xfactor_common = Xfactor_Common.objects.get(computer_name=computername, mac_address=macaddress)

            # memo 필드 값 설정 및 저장
            xfactor_common.memo = memo
            xfactor_common.save()
            computer_name = xfactor_common.computer_name

            # X-Factor_Common 오브젝트 가져오기
            xfactor_common_cache = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date).get(computer_name=computername, mac_address=macaddress)

            # memo 필드 값 설정 및 저장
            xfactor_common_cache.memo = memo
            xfactor_common_cache.save()
            computer_name = xfactor_common_cache.computer_name
            return JsonResponse({'success': computer_name})


        except Xfactor_Daily.DoesNotExist:
            return JsonResponse({'error': 'X-Xfactor_Daily 오브젝트가 존재하지 않습니다.'})

