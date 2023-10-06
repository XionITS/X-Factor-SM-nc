from urllib.parse import urlencode

from django.shortcuts import redirect
from django.test import TestCase
import requests
# Create your tests here.
from django.http import HttpResponseBadRequest, HttpResponse
from django.views import View

from common.models import Xfactor_Xuser


class CallbackView(View):
    def get(self, request):
        print("mmmmmmmmmmmmmmmmmmmmm")
        code = request.GET.get('code')
        print(code)

        # access_token = exchange_code_for_token(code)
        # print(access_token)
        userinfo_url = "https://sso.sandbox-nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/userinfo"

        # headers = {
        #     "Authorization": f"Bearer {access_token}"
        # }
        #
        # response = requests.get(userinfo_url, headers=headers)
        # userinfo_data = response.json()
        # sub = userinfo_data.get("sub")
        # email = userinfo_data.get("email")
        # print("User Sub:", sub)
        # xuser_instance = Xfactor_Xuser(
        #     x_id=sub,
        #     x_email=email,
        # )
        # xuser_instance.save()

        if not code:
            return HttpResponseBadRequest("No code provided.")

            # 여기서 인증 코드(code)를 토큰 요청 API 호출에 사용하여 access token과 ID token을 얻어야 합니다.
            # 그 후 access token과 ID token의 유효성 검사 등 필요한 과정을 거칩니다.

        return redirect("../dashboard")

def exchange_code_for_token(code):
    token_url = "https://sso.sandbox-nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/token"
    client_id = "stg-tanium-dashboard"
    client_secret = "whLXIZvLEZsAWfqbQIsiwSkhVpgKGJWP"  # 클라이언트 시크릿 키

    # 토큰 요청 파라미터 설정
    token_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://tanium.ncsoft.com:8000/",
        "client_id": client_id,
        "client_secret": client_secret
    }
    token_payload_encoded = urlencode(token_payload)
    # 토큰 요청 보내기
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"  # 헤더에 Content-Type 설정
    }
    response = requests.post(token_url, data=token_payload_encoded, headers=headers)

    # 토큰 요청의 응답을 확인합니다.
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        return access_token
    else:
        return None
