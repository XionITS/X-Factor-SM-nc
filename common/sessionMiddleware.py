import json

from django.shortcuts import redirect

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
    Login_Method = SETTING['PROJECT']['LOGIN']

class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.path)
        if not request.session.get('sessionid') and not request.path.startswith('/login/') and not request.path.startswith('/signup/'):
            # 세션 아이디가 없으면 로그인 페이지로 리다이렉트
            # if Login_Method == 'NANO':
            #     auth_url = "https://sso.nano.ncsoft.com/realms/ncsoft/protocol/openid-connect/auth"
            #     client_id = "tanium-dashboard"
            #     redirect_uri = "https://tanium.ncsoft.com/dashboard/"
            #     # 사용자를 인증 페이지로 리디렉션합니다.
            #     return redirect(f"{auth_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid")

            # return redirect(f"{auth_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=openid")
            return redirect('login')  # 'login'은 실제 로그인 페이지의 URL 이름으로 변경해야 합니다.

        response = self.get_response(request)
        return response