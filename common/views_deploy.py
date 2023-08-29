from datetime import timedelta, datetime
import psycopg2
from django.shortcuts import render, redirect

from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Xfactor_Group
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

    print("SessionKey 불러오기 성공")

    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    groupsList = []
    # print(data['data'][0]['content_set']['name'])
    GURL = apiUrl + '/api/v2/management_rights_groups'
    responseGroup = requests.get(GURL, headers=PSQ, verify=False)
    dataG = responseGroup.json()
    ik = []
    for i in range(len(dataG['data']) - 1):
        groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
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
        packageList.append({'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                            'Command': dataP['data'][i]['command']})
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
    comName = request.POST.get('selectedGroup')
    packName = request.POST.get('selectedPackage')
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SessionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']
    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    CURL = apiUrl + '/api/v2/groups/by-name/' + comName
    PURL = apiUrl + '/api/v2/packages/by-name/' + packName

    CSR = requests.get(CURL, headers=PSQ, verify=False)
    PSR = requests.get(PURL, headers=PSQ, verify=False)

    PSRT = PSR.content.decode('utf-8', errors='ignore')
    CSRT = CSR.content.decode('utf-8', errors='ignore')
    PSRJ = json.loads(PSRT)
    CSRJ = json.loads(CSRT)

    AURL = apiUrl + '/api/v2/actions'
    body = {
        "action_group": {
            "id": 4
        },
        "package_spec": {
            "id": PSRJ['data']['id']
        },
        "name": "Sample Action",
        "expire_seconds": 3600,
        "target_group": {
            "id": CSRJ['data']['id']
        }
    }
    CAQ = requests.post(AURL, headers=PSQ, json=body, verify=False)
    print(CAQ.status_code)
    RD = {}
    return JsonResponse(RD)


@csrf_exempt
def computer_group_sel(request):

    return JsonResponse()
