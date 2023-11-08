import pytz
from django.apps import apps
from django.conf import settings
from django.db.models import Value
from django.db.models.functions import Concat
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook
import os
import json
from datetime import datetime, timedelta
from django.utils import timezone

from common.models import Xfactor_Common_Cache
from common.serializers import CommonSerializer,Dailyserializer,Cacheserializer

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DBSettingTime = SETTING['DB']['DBSelectTime']
today_collect_date = timezone.now() - timedelta(minutes=DBSettingTime)

@csrf_exempt
def export(request, model):

    columns =[]
    parameter_value = request.GET.get('parameter_name')
    parameter_value2 = request.GET.get('parameter_value')
    # 파라미터 값에 따라 조건 처리

    if parameter_value == 'hs_asset':
        columns = ["ncdb_data__deptName", "ncdb_data__userName", "ncdb_data__userId", "computer_name", "ip_address", "mac_address",'hw_cpu','hw_mb','hw_ram','hw_disk','hw_gpu','sw_list','sw_ver_list','memo',"user_date"]
        model_class = apps.get_model('common', model)
        data_list = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date)
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'ver_asset':
        model_class = apps.get_model('common', model)
        columns = ["ncdb_data__deptName", "ncdb_data__userName", "ncdb_data__userId", "computer_name", "ip_address", "mac_address",'os_simple','os_total','os_version','os_build','memo','user_date']
        data_list = model_class.objects.filter(user_date__gte=today_collect_date)
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'up_asset':
        model_class = apps.get_model('common', model)
        columns = ["ncdb_data__deptName", "ncdb_data__userName", "ncdb_data__userId", "computer_name", "ip_address", "mac_address",'hotfix','hotfix_date','memo','user_date']
        data_list = model_class.objects.filter(user_date__gte=today_collect_date).filter(os_simple='Windows')
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'pur_asset':
        model_class = apps.get_model('common', model)
        columns = ["chassistype","ncdb_data__deptName", "ncdb_data__userName", "ncdb_data__userId", "computer_name", "ip_address", "mac_address",'first_network','mem_use','disk_use','hw_cpu'
            ,'hw_mb','hw_ram','hw_disk','hw_gpu','sw_list','sw_ver_list','sw_install','memo','user_date']
        data_list = model_class.objects.filter(user_date__gte=today_collect_date)
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'sec_asset':
        model_class = apps.get_model('common', model)
        columns = ["chassistype","ncdb_data__deptName", "ncdb_data__userName", "ncdb_data__userId", "computer_name", "ip_address", "mac_address",'security1','security1_ver'
            ,'security2','security2_ver','security3','security3_ver','security4','security4_ver','security5','security5_ver','uuid','user_date']
        data_list = model_class.objects.filter(user_date__gte=today_collect_date)
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'sec_asset2':
        model_class = apps.get_model('common', model)
        columns = ["chassistype","ncdb_data__deptName", "ncdb_data__userName", "ncdb_data__userId", "computer_name", "ip_address", "mac_address"
            ,'ext_chr','ext_chr_ver','ext_edg','ext_edg_ver','ext_fir','ext_fir_ver','uuid','user_date']
        data_list = model_class.objects.filter(user_date__gte=today_collect_date)
        data = Cacheserializer(data_list, many=True).data

    local_tz = pytz.timezone('Asia/Seoul')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    now = utc_now.astimezone(local_tz)
    user = ''
    cache = ''
    if request.GET.get('selectedDate') == None:
        pass
    elif request.GET.get('selectedDate') != '':
        start_date_naive = datetime.strptime(request.GET.get('selectedDate'), "%Y-%m-%d-%H")
        start_of_today = timezone.make_aware(start_date_naive)
        end_of_today = start_of_today + timedelta(minutes=50)
        start_of_day = start_of_today - timedelta(days=7)
        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    elif request.GET.get('selectedDate') == '':
        start_of_today1 = now.strftime('%Y-%m-%d %H')
        start_of_today2 = datetime.strptime(start_of_today1, '%Y-%m-%d %H')
        start_of_today = timezone.make_aware(start_of_today2)
        start_of_day = start_of_today - timedelta(days=7)
        end_of_today = start_of_today + timedelta(minutes=50)
        # 현재
        user = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_today, cache_date__lt=end_of_today)
        # 토탈
        cache = Xfactor_Common_Cache.objects.filter(user_date__gte=start_of_today, user_date__lt=end_of_today).filter(cache_date__gte=start_of_day, cache_date__lt=end_of_today)

    if parameter_value == 'all_asset1':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        if request.GET.get('categoryName') == 'Online':
            if request.GET.get('seriesName') == 'Other':
                data_list = user.exclude(chassistype__in=['Notebook', 'Desktop'])
            else:
                data_list = user.filter(chassistype=request.GET.get('seriesName'))
        if request.GET.get('categoryName') == 'Total':
            if request.GET.get('seriesName') == 'Other':
                data_list = cache.exclude(chassistype='Notebook').exclude(chassistype='Desktop')
            else:
                data_list = cache.filter(chassistype=request.GET.get('seriesName'))
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'asset_os_detail1':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        if request.GET.get('categoryName') == 'Other':
            if request.GET.get('seriesName') == 'Other':
                print("asd")
                data_list = user.exclude(os_simple__in=['Windows', 'Mac']).exclude(chassistype__in=['Desktop, Notebook'])
            else:
                data_list = user.filter(chassistype=request.GET.get('categoryName')).exclude(os_simple__in=['Windows', 'Mac'])
        else:
            if request.GET.get('seriesName') == 'Other':
                data_list = user.filter(os_simple=request.GET.get('categoryName')).exclude(chassistype__in=['Desktop, Notebook'])
            else:
                data_list = user.filter(os_simple=request.GET.get('categoryName'), chassistype=request.GET.get('seriesName'))
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'asset_os_detail2':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        if request.GET.get('categoryName') == 'Other':
            if request.GET.get('seriesName') == 'Other':
                data_list = cache.exclude(os_simple__in=['Windows', 'Mac']).exclude(chassistype__in=['Desktop, Notebook'])
                print(data_list)
            else:
                data_list = cache.filter(chassistype=request.GET.get('seriesName')).exclude(os_simple__in=['Windows', 'Mac'])
        else:
            if request.GET.get('seriesName') == 'Other':
                data_list = cache.filter(os_simple=request.GET.get('categoryName')).exclude(chassistype__in=['Desktop, Notebook'])
            else:
                data_list = cache.filter(os_simple=request.GET.get('categoryName'), chassistype=request.GET.get('seriesName'))
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'office_chart':
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        data_list = []
        if request.GET.get('categoryName') == 'Office 16 이상':
            data_list = user.filter(essential5__in=['Office 21', 'Office 19', 'Office 16'])
        if request.GET.get('categoryName') == 'Office 16 미만':
            data_list = user.filter(essential5='Office 15')
        if request.GET.get('categoryName') == 'Office 설치 안됨':
            data_list = user.filter(essential5='오피스 없음')
        if request.GET.get('categoryName') == '미확인':
            data_list = user.filter(essential5__in=['unconfirmed', ''])
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'oslistPieChart':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        data_list = user.annotate(windows_build=Concat('os_total', Value(' '), 'os_build')).filter(windows_build__contains=request.GET.get('categoryName'), os_simple='Windows')
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'osVerPieChart':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        if request.GET.get('categoryName') == '업데이트 완료':
            data_list = user.filter(os_simple='Windows', os_build__gte='19044').exclude(os_total='unconfirmed')
        if request.GET.get('categoryName') == '업데이트 필요':
            data_list = user.filter(os_simple='Windows', os_build__lt='19044').exclude(os_total='unconfirmed')
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'subnet_chart':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        if request.GET.get('categoryName') == 'VPN':
            data_list = user.filter(subnet__in=['172.21.224.0/20', '192.168.0.0/20'])
        if request.GET.get('categoryName') == '사내망':
            data_list = user.filter(subnet__in=['172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
                    , '172.18.88.0/21', '172.18.96.0/21', '172.18.104.0/22', '172.20.16.0/21', '172.20.40.0/22', '172.20.48.0/21', '172.20.56.0/21', '172.20.64.0/22', '172.20.68.0/22', '172.20.78.0/23', '172.20.8.0/21'])
        if request.GET.get('categoryName') == '미확인':
            data_list = user.filter(subnet='unconfirmed')
        if request.GET.get('categoryName') == '외부망':
            data_list = user.exclude(subnet__in=['unconfirmed', '172.21.224.0/20', '192.168.0.0/20', '172.18.16.0/21', '172.18.24.0/21', '172.18.32.0/22', '172.18.40.0/22', '172.18.48.0/21', '172.18.56.0/22', '172.18.64.0/21', '172.18.72.0/22' \
                    , '172.18.88.0/21', '172.18.96.0/21', '172.18.104.0/22', '172.20.16.0/21', '172.20.40.0/22', '172.20.48.0/21', '172.20.56.0/21', '172.20.64.0/22', '172.20.68.0/22', '172.20.78.0/23', '172.20.8.0/21'])
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'tcpuChart':
        data_list = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        data_list = user.filter(t_cpu='True')
        data = Cacheserializer(data_list, many=True).data

    elif parameter_value == 'hotfix_chart':
        three_months_ago = datetime.now() - timedelta(days=90)
        data_list = []
        filtered_user_objects = []
        columns = ["ncdb_data__deptName", "computer_name", "ncdb_data__userId", "chassistype", "ip_address", "mac_address", "user_date"]
        user_objects = user
        users_values = user_objects.values('hotfix_date', 'computer_id')

        for i, user in enumerate(users_values):
            date_strings = user['hotfix_date'].split('<br> ')
            date_objects = []
            for date_str in date_strings:
                try:
                    date_obj = datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
                    date_objects.append(date_obj)
                except ValueError:
                    continue
            if date_objects:
                latest_date = max(date_objects)
                if latest_date < three_months_ago and request.GET.get('categoryName') == '보안패치 필요':
                    filtered_user_objects.append(user['computer_id'])
                elif latest_date > three_months_ago and request.GET.get('categoryName') == '보안패치 불필요':
                    filtered_user_objects.append(user['computer_id'])
        data_list = Xfactor_Common_Cache.objects.filter(user_date__gte=today_collect_date, computer_id__in=filtered_user_objects)
        data = Cacheserializer(data_list, many=True).data

    # 전체컬럼 조회
    # 동적으로 모델에서 컬럼명 추출
    # model_class = apps.get_model('common', model)  # 앱 이름과 모델명을 지정하여 모델 클래스를 가져옵니다
    # columns = [field.name for field in model_class._meta.get_fields() if not field.many_to_many and not field.one_to_many]  # 모델의 모든 필드 이름을 가져옵니다

    # 데이터 추출
    #data = model_class.objects.filter(user_date__gte=today_collect_date).values(*columns)
    #data = model_class.objects.values(*columns)



    # 파일 업로드 처리
    file_path = os.path.join(settings.MEDIA_ROOT, f'{model}_{parameter_value}.xlsx')  # 저장될 파일 경로

    # 엑셀 파일 생성
    wb = Workbook()
    ws = wb.active

    # 헤더 추가
    ws.append(columns)

    # 데이터 추가
    for item in data:
        row_data = []
        for column in columns:
            if "__" in column:  # Check if the column name contains "__"
                field_name, sub_field_name = column.split("__")
                # If the field is 'ncdb_data', extract 'userId' or 'deptName'
                if field_name == 'ncdb_data' and isinstance(item[field_name], dict):
                    sub_field_value = item[field_name].get(sub_field_name, None)  # Default to None if not found
                    row_data.append(sub_field_value)
            elif column in item:  # Check if the column exists in the item
                # Modify the date format before appending it to the worksheet
                if isinstance(item[column], datetime):
                    row_data.append(item[column].strftime('%Y-%m-%d %H:%M:%S'))  # Modify the date format as desired
                else:
                    row_data.append(item[column])
            else:
                row_data.append(None)  # Or any other default value you want to use for missing data

        ws.append(row_data)

    # 파일 저장
    wb.save(file_path)

    # 파일 다운로드 응답 생성
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{model}_{parameter_value}.xlsx.xlsx"'

    # Close the file manually after generating the response
    wb.close()

    return response