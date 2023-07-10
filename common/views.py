from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from .models import XFactor_User
from .models import XFactor_Group
from .models import XFactor_Auth
from .models import XFactor_UserAuth


# menu_list = XFactor_Auth.objects.get(auth_id="OS_asset").auth_name
# menu_list = XFactor_Auth.objects.all()
# menu_list = []
# auth_names = XFactor_Auth.objects.values_list('auth_name', flat=True)
# for auth_name in auth_names:
#    menu_list.append(auth_name)


# auth_id = user_auth.auth_id
# auth_name = user_auth.xfactor_auth.auth_name
# auth_url = user_auth.xfactor_auth.auth_url
# print(menu_list)


def dashboard(request):
    #session을 computer_id에 넣기
    user_auths = XFactor_UserAuth.objects.filter(xfactor_user__computer_id='123', auth_use='true')  # 사용자의 권한 목록 가져오기
    menu_list = []
    for user_auth in user_auths:
        menu_list.append(user_auth.xfactor_auth)
    context = {'menu_list' : menu_list}
    return render(request, 'dashboard.html', context)


def index(request):
    # user_list = XFactor_User
    # context = {'user_list' : user_list}
    # return render(request, 'user_list.html', context)
    return render(request, '1.html')
@csrf_exempt
def index_paging (request):
    #print(request)
    #return render(request, '1.html')
    # draw = int(request.POST.get('draw'))
    # start = int(request.POST.get('start'))
    # length = int(request.POST.get('length'))
    # search = request.POST.get('search[value]')
    # page = math.ceil(start / length) + 1
    # data = [ str(length), str(page), str(search)]
    # SMD = PDPI('statistics', 'osMore', data)
    # SMC = PDPI('statistics', 'osCount', data)
    RD = {
           }
    #eturnData = {'computer_id':'123','computer_name':'djlee'}
    group_list = XFactor_Group.objects.get(group_id=123)
    data = [{'group_id' : group_list.group_id,
            'group_name': group_list.group_name,
            'group_note': group_list.group_note,
            }]
    RD = {"item": data}
    #print(RD)
    return JsonResponse(RD)