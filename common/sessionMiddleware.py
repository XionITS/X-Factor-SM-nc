from django.shortcuts import redirect


class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('sessionid') and not request.path.startswith('/login/'):
            # 세션 아이디가 없으면 로그인 페이지로 리다이렉트
            return redirect('login')  # 'login'은 실제 로그인 페이지의 URL 이름으로 변경해야 합니다.

        response = self.get_response(request)
        return response