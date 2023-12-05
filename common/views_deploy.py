from datetime import timedelta, datetime
import psycopg2
from django.shortcuts import render, redirect

from django.http import JsonResponse,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
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
def group(request):
    search = request.POST.get('search')
    # print(search)
    con_set = request.POST.get('id')
    if con_set is None:
        con_set = ''
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SessionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    #print("SessionKey 불러오기 성공")

    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    groupsList = []
    # print(data['data'][0]['content_set']['name'])
    GURL = apiUrl + '/api/v2/management_rights_groups'
    responseGroup = requests.get(GURL, headers=PSQ, verify=False)
    dataG = responseGroup.json()
    for i in range(len(dataG['data']) - 1):
        groupsList.append({'Name': dataG['data'][i]['name'], 'id': dataG['data'][i]['id']})
        # if con_set == 'all':
        #     if dataG['data'][i]['name'].startswith(search) or dataG['data'][i]['content_set']['name'].startswith(search) or dataG['data'][i]['text'].startswith(search):
        #         groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
        # elif dataG['data'][i]['content_set']['name'] == con_set and search is None:
        #     groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
        # elif dataG['data'][i]['content_set']['name'] == con_set:
        #     if dataG['data'][i]['name'].startswith(search) or dataG['data'][i]['content_set']['name'].startswith(search) or dataG['data'][i]['text'].startswith(search):
        #         groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
    Count = len(groupsList)
    RD = {'item': groupsList,
            'recordsTotal': Count,
            'recordsFiltered': Count,
            }
    return JsonResponse(RD)


@csrf_exempt
def package(request):
    search = request.POST.get('search')
    con_set = request.POST.get('id')
    if con_set is None:
        con_set = 'Default'
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SessionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    # print("SessionKey 불러오기 성공")

    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    PURL = apiUrl + '/api/v2/packages'
    responsePack = requests.get(PURL, headers=PSQ, verify=False)
    dataP = responsePack.json()
    packageList = []
    # print(con_set)
    for i in range(len(dataP['data']) - 1):
        packageList.append({'Name': dataP['data'][i]['name'], 'id': dataP['data'][i]['id']})
        # if con_set == 'all':
        #     if dataP['data'][i]['name'].startswith(search) or dataP['data'][i]['content_set']['name'].startswith(search) or dataP['data'][i]['command'].startswith(search):
        #         packageList.append({'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
        #                             'Command': dataP['data'][i]['command']})
        # elif dataP['data'][i]['content_set']['name'] == con_set and search is None:
        #     packageList.append({'id': dataP['data'][i]['id'], 'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
        #                         'Command': dataP['data'][i]['command'], 'Command_Timeout': dataP['data'][i]['command_timeout']})
        # elif dataP['data'][i]['content_set']['name'] == con_set:
        #     if dataP['data'][i]['name'].startswith(search) or dataP['data'][i]['content_set']['name'].startswith(search) or dataP['data'][i]['command'].startswith(search):
        #         packageList.append({'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
        #                             'Command': dataP['data'][i]['command']})
    Count = len(packageList)
    RD = {'item': sorted(packageList, key=lambda x: x['Name']),
            'recordsTotal': Count,
            'recordsFiltered': Count
            }
    return JsonResponse(RD)


@csrf_exempt
def deploy_action(request):
    comId = request.POST.get('selectedGroup')
    packID = request.POST.get('selectedPackage')
    groupName = request.POST.get('selectedGroupName')
    packName = request.POST.get('selectedPackageName')
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SessionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']
    PSQ = {'session': SK, 'Content-Type': 'application/json'}

    AURL = apiUrl + '/api/v2/actions'
    body = {
        "action_group": {
            "id": 4
        },
        "package_spec": {
            "id": packID
        },
        "name": "Sample Action",
        "expire_seconds": 3600,
        "target_group": {
            "id": comId
        }
    }
    CAQ = requests.post(AURL, headers=PSQ, json=body, verify=False)
    function = 'Deploy'  # 분류 정보를 원하시는 텍스트로 변경해주세요.
    item = 'Deploy '+ packName + ' for the ' + groupName + ' Group'
    result = '성공'
    user = request.session.get('sessionid')
    date = timezone.now().replace(microsecond=0)
    if CAQ.status_code == 200:
        Xfactor_log = Xfactor_Log(
            log_func=function,
            log_item=item,
            log_result=result,
            log_user=user,
            log_date=date
        )
        Xfactor_log.save()
        RD = {'result': 'success'}
    else:
        result = '실패'
        Xfactor_log = Xfactor_Log(
            log_func=function,
            log_item=item,
            log_result=result,
            log_user=user,
            log_date=date
        )
        Xfactor_log.save()
        RD = {'result': 'fail'}
    return JsonResponse(RD)


@csrf_exempt
def group_list(request):
    group_id = request.POST.get('id')
    try:
        group = Xfactor_Group.objects.get(group_id=group_id)
        group_data = {
            'group_id': group.group_id,
            'group_name': group.group_name,
            'group_note': group.group_note,
            'computer_id_list': group.computer_id_list,
            'computer_name_list': group.computer_name_list
        }
    except ObjectDoesNotExist:
        # 그룹 데이터가 존재하지 않을 경우, 값들을 공백 또는 빈 문자열로 처리
        group_data = {
            'group_id': group_id,
            'group_name': '',
            'group_note': '값이 없습니다. ',
            'computer_id_list': '',
            'computer_name_list': '-기존 Group입니다.-'
        }
    RD = {'group': group_data}
    # print(RD)
    return JsonResponse(RD)
