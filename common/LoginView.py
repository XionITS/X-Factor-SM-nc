# import urllib
#
# from django.test import TestCase
#
# # Create your tests here.
# from django.http import HttpResponseRedirect
# from django.views import View
#
#
# class LoginView(View):
#     def get(self, request):
#         # NCSoft의 OpenID Provider 주소
#         auth_url = "https://sso.sandbox-nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/auth"
#
#         # 필요한 쿼리 파라미터들
#         params = {
#             'client_id': 'stg-tanium-dashboard',
#             'response_type': 'code',
#             'redirect_uri': 'localhost:8000',
#             'scope': 'openid'
#         }
#
#         # 쿼리 파라미터들을 URL에 추가합니다.
#         url = f"{auth_url}?{urllib.parse.urlencode(params)}"
#         return HttpResponseRedirect(url)
