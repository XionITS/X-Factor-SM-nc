from django.apps import apps
from django.conf import settings
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook
import os
import datetime


csrf_exempt
def export(request, model):

    # 동적으로 모델에서 컬럼명 추출
    model_class = apps.get_model('common', model)  # 앱 이름과 모델명을 지정하여 모델 클래스를 가져옵니다
    columns = [field.name for field in model_class._meta.get_fields() if not field.many_to_many and not field.one_to_many]  # 모델의 모든 필드 이름을 가져옵니다
    # 데이터 추출
    data = model_class.objects.values(*columns)


    # 파일 업로드 처리
    file_path = os.path.join(settings.MEDIA_ROOT, f'{model}_data.xlsx')  # 저장될 파일 경로

    # 엑셀 파일 생성
    wb = Workbook()
    ws = wb.active

    # 헤더 추가
    ws.append(columns)

    # 데이터 추가
    for item in data:
        # Modify the date format before appending it to the worksheet
        for column in columns:
            if isinstance(item[column], datetime.date):
                item[column] = item[column].strftime('%Y-%m-%d %H:%M:%S')  # Modify the date format as desired
        row_data = [item[column] for column in columns]
        ws.append(row_data)

    # 파일 저장
    wb.save(file_path)

    # 파일 다운로드 응답 생성
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{model}_data.xlsx"'

    # Close the file manually after generating the response
    wb.close()

    return response