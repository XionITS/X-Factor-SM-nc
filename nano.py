
#1. nano 통합인증서버에 애플리케이션을 등록 (통합인증서버에 등록하여 client_id, client_secret 받기)
#2. https를 get방식으로 client_id, scope, uri(로그인페이지)를 보내)
#3. 그럼 로그인페이지로 리다이렉트 되면서 아이디/비번을 입력받는다 (아이디 비번은 nano통합인증서버의 계정)
#4. 검증 후 인증성공하면 가져온 authrization_code, client_id, client_secret, uri를 보내서 access_token을 가져온다
#5. 유저정보등의 scope값을 보기위해 access_token을 저장하고 값을 API호출시 보내서 json형태의 값을 가져온다.
import requests


def nano_auth_code():
    #클라이언트 아이디받기
    client_id = 'your_client_id'

    #보낼 URI주소 입력
    redirect_uri = 'your_redirect_uri'

    #받고 싶은 권한범위 또는 scope=profile
    scope = 'openid'

    # 사용자를 인증 및 인가하는 URL
    authorization_url = 'https://{host}/realms/ncsoft/protocol/openidconnect/auth'

    # 파라미터 설정
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope
    }

    # 사용자를 인증 및 인가하는 페이지로 리디렉션
    response = requests.get(authorization_url, params=params)

    # 인증 코드를 추출
    # authorization_code = extract_authorization_code(response.url)
    # return authorization_code

def nano_access_token(authorization_code) :
    #클라이언트 아이디받기
    client_id = 'your_client_id'

    #보낼 URI주소 입력
    redirect_uri = 'your_redirect_uri'

    #클라이언트 비밀번호받기
    client_secret = 'your_client_secret'


    # 토큰 엔드포인트 URL
    token_url = 'https://{host}/realms/ncsoft/protocol/openidconnect/token'

    # 요청 페이로드 설정
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': authorization_code
    }
    # 액세스 토큰 요청
    response = requests.post(token_url, data=data)

    # 응답에서 액세스 토큰 추출
    access_token = response.json().get('access_token')

    return access_token


# 사용 예시
authorization_code = nano_auth_code()
access_token = nano_access_token(authorization_code)
print(access_token)