# from django.shortcuts import render
#
# class ExceptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         try:
#             response = self.get_response(request)
#         except Exception as e:
#             if isinstance(e, Exception):  # 여기서 SomeException은 실제 예외 클래스로 대체해야 합니다.
#                 return render(request, 'common/error_400.html', status=400)
#             elif isinstance(e, Exception):  # 여기서 SomeOtherException은 실제 예외 클래스로 대체해야 합니다.
#                 return render(request, 'common/error_404.html', status=404)
#             else:
#                 return render(request, 'common/error_500.html', status=500)
#         return response