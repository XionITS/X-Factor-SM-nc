from django.apps import apps
from django.conf import settings
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook
import os
import json
from datetime import datetime, timedelta
from django.utils import timezone


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
        model_class = apps.get_model('common', model)
        columns = ['computer_name','chassistype','ip_address','mac_address','hw_cpu','hw_mb','hw_ram','hw_disk','hw_gpu','sw_list','memo','user_date']
        data = model_class.objects.filter(user_date__gte=today_collect_date).values(*columns)
    elif parameter_value == 'ver_asset':
        model_class = apps.get_model('common', model)
        columns = ['computer_name','chassistyt7ype','ip_address','mac_address','os_simple','os_total','os_version','os_build','memo','user_date']
        data = model_class.objects.filter(user_date__gte=today_collect_date).values(*columns)
    elif parameter_value == 'up_asset':
        model_class = apps.get_model('common', model)
        columns = ['computer_name','chassistype','ip_address','mac_address','hotfix','hotfix_date','memo','user_date']
        data = model_class.objects.filter(user_date__gte=today_collect_date).filter(os_simple='Windows').values(*columns)
    elif parameter_value == 'pur_asset':
        model_class = apps.get_model('common', model)
        columns = ['computer__computer_name','computer__chassistype','computer__ip_address','computer__mac_address','computer__first_network','mem_use','disk_use','computer__hw_cpu'
            ,'computer__hw_mb','computer__hw_ram','computer__hw_disk','computer__hw_gpu','computer__sw_list','computer__sw_ver_list','computer__sw_install','computer__memo','user_date']
        data = model_class.objects.filter(user_date__gte=today_collect_date).values(*columns)
    elif parameter_value == 'sec_asset':
        print(model)
        model_class = apps.get_model('common', model)
        print(model_class)
        columns = ['computer__computer_name','computer__chassistype','computer__ip_address','computer__mac_address','security1','security1_ver'
            ,'security2','security2_ver','security3','security3_ver','security4','security4_ver','security5','security5_ver','uuid','user_date']
        data = model_class.objects.filter(user_date__gte=today_collect_date).values(*columns)
    elif parameter_value == 'sec_asset2':
        print(model)
        model_class = apps.get_model('common', model)
        print(model_class)
        columns = ['computer__computer_name','computer__chassistype','computer__ip_address','computer__mac_address'
            ,'ext_chr','ext_chr_ver','ext_edg','ext_edg_ver','ext_fir','ext_fir_ver','uuid','user_date']
        data = model_class.objects.filter(user_date__gte=today_collect_date).values(*columns)
    elif parameter_value == 'all_asset1':
        print(model)
        model_class = apps.get_model('common', model)
        print(model_class)
        columns = ['computer_name', 'chassistype', 'ip_address', 'mac_address', 'user_date']
        if request.GET.get('categoryName') == 'Online':
            if request.GET.get('seriesName') == 'Other':
                data = model_class.objects.filter(user_date__gte=today_collect_date).exclude(chassistype__in=['Notebook', 'Desktop']).values(*columns)
            else:
                data = model_class.objects.filter(user_date__gte=today_collect_date, chassistype=request.GET.get('seriesName')).values(*columns)
        if request.GET.get('categoryName') == 'Total':
            if request.GET.get('seriesName') == 'Other':
                data = model_class.objects.exclude(chassistype__in=['Notebook', 'Desktop']).values(*columns)
            else:
                data = model_class.objects.filter(chassistype=request.GET.get('seriesName')).values(*columns)

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
        # Modify the date format before appending it to the worksheet
        for column in columns:
            if isinstance(item[column], datetime):
                item[column] = item[column].strftime('%Y-%m-%d %H:%M:%S')  # Modify the date format as desired
        row_data = [item[column] for column in columns]
        ws.append(row_data)

    # 파일 저장
    wb.save(file_path)

    # 파일 다운로드 응답 생성
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{model}_{parameter_value}.xlsx.xlsx"'

    # Close the file manually after generating the response
    wb.close()

    return response