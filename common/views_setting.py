import datetime

import requests
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
import hashlib
import psycopg2
import json
import ast
from django.http import JsonResponse, HttpResponse
from urllib.parse import urlencode
from common.models import Xfactor_Log, Xfactor_Xuser, Xfactor_Xuser_Auth, Xfactor_Xgroup_Auth, Xfactor_Xuser_Group, Xfactor_Common, Daily_Statistics_log

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBHost = SETTING['DB']['DBHost']
DBPort = SETTING['DB']['DBPort']
DBName = SETTING['DB']['DBName']
DBUser = SETTING['DB']['DBUser']
DBPwd = SETTING['DB']['DBPwd']

@csrf_exempt
def ver_list(request):
    try:
        ver = Xfactor_Common.objects.filter(os_simple='Windows').exclude(os_build__in=['', 'unconfirmed']).values_list('os_build', flat=True).distinct()
        ver_list = sorted(map(int, ver), reverse=True)

        #현재 Web 값 가져오기
        ver_current = Daily_Statistics_log.objects.filter(item='ver_web').order_by('-statistics_collection_date').values_list('item_count', flat=True).first()

        data = {
            'ver_list': ver_list,
            'current_value': ver_current
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        print('Windows Ver_list 실패')


@csrf_exempt
def update_ver_module(request):
    try:
        value = request.POST.get('value')
        Conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        query = "UPDATE common_daily_statistics_log SET item_count = %s WHERE item = 'ver_module' AND statistics_collection_date = (SELECT MAX(statistics_collection_date) FROM common_daily_statistics_log WHERE item = 'ver_module')"
        Cur.execute(query, (value,))
        Conn.commit()
        Cur.close()
        Conn.close()

        return JsonResponse({'result': 'success'}, status=200)  # 성공적으로 삭제되었을 때 응답
    except Exception as e:
        print(str(e))  # 에러 메시지 출력 (디버깅 용)
        return JsonResponse({'result': 'failure'}, status=400)  # 삭제 중 오류가 발생했을 때 응답


@csrf_exempt
def hot_list(request):
    try:
        hot_list = [1,2,3,4,5,6]
        #현재 Web 값 가져오기
        hot_current = Daily_Statistics_log.objects.filter(item='hot_web').order_by('-statistics_collection_date').values_list('item_count', flat=True).first()

        data = {
            'hot_list': hot_list,
            'current_value': hot_current/30
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        print('Windows Hot_list 실패')


@csrf_exempt
def update_hot_module(request):
    try:
        value = request.POST.get('value')
        Conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        query = "UPDATE common_daily_statistics_log SET item_count = %s *30 WHERE item = 'hot_module' AND statistics_collection_date = (SELECT MAX(statistics_collection_date) FROM common_daily_statistics_log WHERE item = 'hot_module')"
        Cur.execute(query, (value,))
        Conn.commit()
        Cur.close()
        Conn.close()

        return JsonResponse({'result': 'success'}, status=200)  # 성공적으로 삭제되었을 때 응답
    except Exception as e:
        print(str(e))  # 에러 메시지 출력 (디버깅 용)
        return JsonResponse({'result': 'failure'}, status=400)  # 삭제 중 오류가 발생했을 때 응답


@csrf_exempt
def discover_list(request):
    try:
        discover_list = [120,130,140,150,160,170]
        #현재 Web 값 가져오기
        discover_current = Daily_Statistics_log.objects.filter(item='discover_web').order_by('-statistics_collection_date').values_list('item_count', flat=True).first()

        data = {
            'discover_list': discover_list,
            'current_value': discover_current
        }
        return HttpResponse(json.dumps(data), content_type='application/json')
    except:
        print('discover_list 실패')


@csrf_exempt
def update_discover_module(request):
    try:
        value = request.POST.get('value')
        Conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()
        query = "UPDATE common_daily_statistics_log SET item_count = %s WHERE item = 'discover_module' AND statistics_collection_date = (SELECT MAX(statistics_collection_date) FROM common_daily_statistics_log WHERE item = 'discover_module')"
        Cur.execute(query, (value,))
        Conn.commit()
        Cur.close()
        Conn.close()

        return JsonResponse({'result': 'success'}, status=200)  # 성공적으로 삭제되었을 때 응답
    except Exception as e:
        print(str(e))  # 에러 메시지 출력 (디버깅 용)
        return JsonResponse({'result': 'failure'}, status=400)  # 삭제 중 오류가 발생했을 때 응답

