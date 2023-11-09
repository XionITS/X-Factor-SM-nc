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
def history(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='History', auth_use='false')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'],
                                                    xfactor_auth_id='History', auth_use='false')
    if user_auth and group_auth:
        return redirect('../home/')
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu_user = XuserAuthSerializer(xuser_auths, many=True)
    xgroup_auths = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'], auth_use='true')
    menu_group = XgroupAuthSerializer(xgroup_auths, many=True)
    all_menu = menu_user.data + menu_group.data
    unique_items = list({(item['xfactor_auth']['auth_id'], item['xfactor_auth']['auth_name'], item['xfactor_auth']['auth_url'], item['xfactor_auth']['auth_num'], item['auth_use']) for item in all_menu})
    context = {'menu_list': unique_items}
    return render(request, 'asset_history.html', context)


@csrf_exempt
def search_h(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='History', auth_use='false')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'],
                                                    xfactor_auth_id='History', auth_use='false')
    if user_auth and group_auth:
        return redirect('../../home/')
    if request.method == "POST":
        today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
        search_text = request.POST.get('searchText', None)
        datesource1 = request.POST.get('date1', None)
        datesource2 = request.POST.get('date2', None)
        if datesource1 == '' or datesource2 == '':
            return HttpResponse(None)
        date1 = datetime.strptime(datesource1, "%Y-%m-%d %H시")
        date2 = datetime.strptime(datesource2, "%Y-%m-%d %H시")
        start_h_1 = timezone.make_aware(datetime.combine(date1.date(), datetime.min.time())) + timedelta(hours=date1.hour)
        end_h_1 = start_h_1 + timedelta(hours=1)
        start_h_2 = timezone.make_aware(datetime.combine(date1.date(), datetime.min.time())) + timedelta(hours=date2.hour)
        end_h_2 = start_h_2 + timedelta(hours=1)
        if search_text == '':
            return HttpResponse(None)
        user1 = Xfactor_Common_Cache.objects.filter(user_date__range=(start_h_1, end_h_1)).filter(computer_name__icontains=search_text).order_by('-user_date').first()
        user2 = Xfactor_Common_Cache.objects.filter(user_date__range=(start_h_2, end_h_2)).filter(computer_name__icontains=search_text).order_by('-user_date').first()

        user_data1 = Cacheserializer(user1).data
        user_data2 = Cacheserializer(user2).data
        # response = {
        #     'data': user_data,  # Serialized data for the current page
        # }
        return JsonResponse({'data1': user_data1,
                             'data2': user_data2})


@csrf_exempt
def search_box_h(request):
    user_auth = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=request.session['sessionid'],
                                                  xfactor_auth_id='History', auth_use='false')
    group_auth = Xfactor_Xgroup_Auth.objects.filter(xfactor_xgroup=request.session['sessionid'],
                                                    xfactor_auth_id='History', auth_use='false')
    if user_auth and group_auth:
        return redirect('../../home/')
    if request.method == "POST":
        today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
        search_text = request.POST.get('searchText', None)
        user_data = Xfactor_Common.objects.filter(computer_name__icontains=search_text).values('computer_name')
        #print(user_data)
        # user_data = XfactorServiceserializer(user, many=True).data
        return JsonResponse({'data': list(user_data)})


# @csrf_exempt
# def select_date_l(request):
#     if request.method == "POST":
#         date = request.POST.get('date1')
#         user = Xfactor_Service.objects.select_related('computer').filter(user_date__date=date)
#         user_data = XfactorServiceserializer(user, many=True).data
#         return JsonResponse({'data': user_data})
#
#
# @csrf_exempt
# def select_date_r(request):
#     if request.method == "POST":
#         date = request.POST.get('date2')
#         user = Xfactor_Service.objects.select_related('computer').filter(user_date__date=date)
#         user_data = XfactorServiceserializer(user, many=True).data
#         return JsonResponse({'data': user_data})