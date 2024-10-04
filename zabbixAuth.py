import json
import requests

# Zabbix 서버 URL
def zabbix_login(url, username, password):
    """
    Zabbix 서버에 로그인하고 토큰을 반환하는 함수입니다.
    
    :param url: Zabbix 서버의 URL입니다.
    :param username: Zabbix 사용자 이름입니다.
    :param password: Zabbix 사용자 비밀번호입니다.
    :return: 성공 시 토큰을 반환하고, 실패 시 오류 메시지를 출력합니다.
    """
    headers = {'Content-Type': 'application/json-rpc'}
    login_data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password
        },
        "id": 1,
        "auth": None
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(login_data))
    response_data = response.json()
    
    if 'result' in response_data:
        return response_data['result']
    else:
        print("로그인 실패:", response_data.get('error'))
        return None

