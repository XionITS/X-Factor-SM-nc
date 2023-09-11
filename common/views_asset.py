from django.http import HttpResponse
import math
import operator
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

today_collect_date = timezone.now() - timedelta(minutes=7)

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
        today_collect_date = timezone.now() - timedelta(minutes=7)
        search_text = request.POST.get('searchText', None)
        #print(search_text)
        user = Xfactor_Service.objects.select_related('computer').filter(user_date__gte=today_collect_date).filter(computer__computer_name=search_text)
        user_data = XfactorServiceerializer(user, many=True).data
        print(user_data)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaa")
        #print(user_data.data)
        # response = {
        #     'data': user_data,  # Serialized data for the current page
        # }
        return JsonResponse({'data': user_data})