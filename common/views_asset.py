from django.http import HttpResponse
import math
import operator
import json
from django.shortcuts import render
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
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)

    context = {'menu_list': menu.data}
    return render(request, 'asset.html', context)



@csrf_exempt
def search(request):
    if request.method == "POST":
        today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)
        search_text = request.POST.get('searchText', None)
        user = Xfactor_Common.objects.filter(user_date__gte=today_collect_date).filter(computer_name__icontains=search_text)
        #print(user)
        #print("11")
        user_data = CommonSerializer(user, many=True).data
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