from django.http import HttpResponse
import math
import json
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
import pytz


with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']

today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)


@csrf_exempt
def um(request):
    #메뉴
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser__x_id=request.session['sessionid'], auth_use='true')
    menu = XuserAuthSerializer(xuser_auths, many=True)
    context = {'menu_list': menu.data}
    return render(request, 'user_management.html', context)

@csrf_exempt
def um_user(request):
    user = Xfactor_Xuser.objects.all()
    #user = Xfactor_Common.objects.prefetch_related('purchase').filter(user_date__gte=today_collect_date)
    filter_columnmap = request.POST.get('filter[columnmap]')
    order_column_index = int(request.POST.get('order[0][column]', 0))
    order_column_dir = request.POST.get('order[0][dir]', 'asc')
    order_column_map = {
        2: 'x_id',
        3: 'x_name',
        4: 'x_email',
        5: 'x_auth',
        # Add mappings for other columns here
    }

    order_column = order_column_map.get(order_column_index, 'x_id')
    if order_column_dir == 'asc':
        user = user.order_by(order_column)
    else:
        user = user.order_by('-' + order_column)

    # Get start and length parameters from DataTables AJAX request
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))  # Default to 10 items per page

    # Paginate the queryset
    paginator = Paginator(user, length)
    page_number = (start // length) + 1

    try:
        page = paginator.page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Serialize the paginated data

    user_list = XuserSerializer(page, many=True).data
    # Prepare the response
    response = {
        'draw': int(request.POST.get('draw', 1)),  # Echo back the draw parameter from the request
        'recordsTotal': paginator.count,  # Total number of items without filtering
        'recordsFiltered': paginator.count,  # Total number of items after filtering (you can update this based on your filtering logic)
        'data': user_list,  # Serialized data for the current page
    }

    return JsonResponse(response)

@csrf_exempt
def user_auth(request):
    x_id = request.POST.get("x_id")
    xuser_auths = Xfactor_Xuser_Auth.objects.filter(xfactor_xuser_id=x_id)
    auth_list= XuserAuthSerializer(xuser_auths, many=True).data
    response = {'auth_list': auth_list}
    return JsonResponse(response)