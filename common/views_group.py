from datetime import timedelta, datetime
import psycopg2
from django.shortcuts import render, redirect

from django.http import JsonResponse,HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Xfactor_Group, Xfactor_Log
import requests
import json
import math
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
apiUrl = SETTING['API']['apiUrl']
SessionKeyPath = SETTING['API']['PATH']['SessionKey']
APIUNM = SETTING['API']['username']
APIPWD = SETTING['API']['password']
DEFAULTGROUPID = SETTING['API']['defaultGroupID']
PACKAGEID = SETTING['API']['packageID']
DBHost = SETTING['DB']['DBHost']
DBPort = SETTING['DB']['DBPort']
DBName = SETTING['DB']['DBName']
DBUser = SETTING['DB']['DBUser']
DBPwd = SETTING['DB']['DBPwd']



@csrf_exempt
def create(request):
    group_name = request.POST['group_name']
    group_description = request.POST['group_description']
    computerIds = json.loads(request.POST['computerIds'])
    computerNames = json.loads(request.POST['computerNames'])

    # 세션키 받기
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SessionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    # Computer Group 만들기
    text = ""
    for index, computerid in enumerate(computerIds):
        if index == len(computerIds) - 1:
            text += f'Computer ID matches \\"{computerid}\\"'
        else:
            text += f'Computer ID matches \\"{computerid}\\" or '

    CCGH = {'session': SK, 'Content-Type': 'text/plain'}
    CCGURL = apiUrl + '/api/v2/groups'
    CCGB = '{"name" : "' + group_name + '","text" : "' + text + '"}'
    CCG = requests.post(CCGURL, headers=CCGH, data=CCGB, verify=False)
    if CCG.status_code== 400:
        message_code = "error"
        message = "Group Name이 이미 존재합니다. 다시 지정해 주세요."
    else :
        CGID = str(CCG.json()['data']['id'])

        #DB넣기
        group_insert = Xfactor_Group()
        group_insert.group_id = CGID
        group_insert.group_name = group_name
        group_insert.group_note = group_description
        group_insert.computer_id_list = computerIds
        group_insert.computer_name_list = computerNames
        group_insert.save()
        message_code = "success"
        message = "Group이 생성되었습니다. \n 그룹이름 : " +group_name+"\n 그룹번호 : " +CGID

        function = 'Group Create'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
        item = 'Create Group for the '+ group_name
        result = '성공'
        user = request.session.get('sessionid')
        date = timezone.now()
        Xfactor_log = Xfactor_Log(
            log_func=function,
            log_item=item,
            log_result=result,
            log_user=user,
            log_date=date
        )
        Xfactor_log.save()

    return JsonResponse({"success":message_code, "message": message})

