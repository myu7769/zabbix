from zabbixAuth import *
import requests
import json
from datetime import datetime
from config import Config

# 사용 예시
zabbix_url = Config.zabbix_COMMON
username = Config.zabbix_ID
password = Config.zabbix_PW

# hostname [] 형식으로 전달

def zabbix_host_get(url, token, hostnames):
    # HTTP 헤더
    headers = {'Content-Type': 'application/json-rpc'}

    if not hostnames:
        print(f"zabbix_host_get host none!!")
        return [];

    # 호스트 정보와 인터페이스, 그룹 ID와 이름, 템플릿 ID와 이름을 조회하는 API 요청 데이터 구성
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host"],
            "selectInterfaces": ["ip"],
            "selectGroups": ["groupid", "name"],
            "selectParentTemplates": ["templateid", "name"],
            "filter": {
                "host": hostnames
            }
        },
        "auth": token,
        "id": 1
    }

    # HTTP POST 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    host_info_list = []

    # 응답 데이터에서 호스트 정보 생성

    if 'result' in response_data and response_data['result']:
        for host in response_data['result']:
            ip_address = host['interfaces'][0]['ip'] if host['interfaces'] else 'IP 정보 없음'
            groups_info = [{'name': group['name'], 'ID': group['groupid']} for group in host['groups']]
            templates_info = [{'name': template['name'], 'ID': template['templateid']} for template in host['parentTemplates']]
            host_info = {
                'hostid': host['hostid'],
                'hostname': host['host'],
                'ip': ip_address,
                'groups': groups_info,
                'templates': templates_info
            }
            host_info_list.append(host_info)

            # 정보 출력
            print(f"호스트 ID: {host['hostid']}, 호스트 이름: {host['host']}, IP: {ip_address}")
            for group in groups_info:
                print(f"그룹 이름: {group['name']} (ID: {group['ID']})")
            for template in templates_info:
                print(f"템플릿 이름: {template['name']} (ID: {template['ID']})")
            print("-" * 40)  # 구분선
    else:
        print("해당하는 호스트 정보를 찾을 수 없습니다:", response_data.get('error'))

    return host_info_list


def getHostId(url, token, hostnames):
    # HTTP 헤더
    headers = {'Content-Type': 'application/json-rpc'}

    if not hostnames:
        print(f"getHostId host none!!")
        return [];

    # 호스트 정보와 인터페이스, 그룹 ID와 이름, 템플릿 ID와 이름을 조회하는 API 요청 데이터 구성
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host"],
            "filter": {
                "host": hostnames
            }
        },
        "auth": token,
        "id": 1
    }

    # HTTP POST 요청 보내기
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()

    host_info_list = []

    # 응답 데이터에서 호스트 정보 생성

    if 'result' in response_data and response_data['result']:
        for host in response_data['result']:
            host_info = {
                'hostid': host['hostid'],
                'hostname': host['host'],
            }
            host_info_list.append(host_info)
    else:
        print("해당하는 호스트 정보를 찾을 수 없습니다:", response_data.get('error'))

    print(host_info_list)
    return host_info_list

def zabbix_create(token, hostname, ip):
    return None; # return true or false , 중복 여부 체크 및 return 으로 hostId

def string_to_unix_time(date_string):
    # print(date_string)
    # 문자열을 datetime 객체로 변환
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    # datetime 객체를 Unix 시간으로 변환
    unix_time = int(dt.timestamp())
    return unix_time

def create_maintenance(url, token, subject , hostIds , hostgroupIds, start_time, end_time ):

    headers = {'Content-Type': 'application/json-rpc'}
 

# Maintenance 설정
    maintenance_data = {
        "jsonrpc": "2.0",
        "method": "maintenance.create",
        "params": {
            "name": subject,  # Maintenance 이름
            "active_since": start_time,  # 시작 시간 (Unix timestamp)
            "active_till": end_time,  # 종료 시간 (Unix timestamp)
            "hostids": hostIds,  # Maintenance를 적용할 호스트 그룹 IDs
            "groupids": hostgroupIds , # host IDs
            "timeperiods": [{
                "timeperiod_type": 0,
                "start_date": start_time,
                "period": end_time - start_time
            }]
        },
        "auth": token,
        "id": 1
    }

    response = requests.post(url, data=json.dumps(maintenance_data), headers=headers)
    
    return response.json()

def disable_hosts_if_ip_matches(url, token, hosts_info):
    
    headers = {'Content-Type': 'application/json-rpc'}
    success_hosts = []
    fail_hosts = []
    msg = [] 

    if not hosts_info:
        print(f"disable_hosts_if_ip_matches hosts_info none!!")
        return [];

    for host_info in hosts_info:
        hostname, expected_ip = host_info

        # 호스트 및 인터페이스 정보 조회
        find_host_data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "filter": {
                    "host": [hostname]
                }
            },
            "auth": token,
            "id": 1
        }

        find_response = requests.post(url, headers=headers, data=json.dumps(find_host_data))
        find_result = find_response.json()

        if 'result' in find_result and find_result['result']:
            # 호스트의 IP 주소 검증
            host_interfaces = find_result['result'][0]['interfaces']
  
            registered_ip = host_interfaces[0]['ip'] if host_interfaces else None

            if registered_ip == expected_ip:
                # IP 주소가 일치하면, 호스트 비활성화
                host_id = find_result['result'][0]['hostid']
                disable_data = {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {
                        "hostid": host_id,
                        "status": 1 # "status": 1은 호스트를 비활성화(disable)하는 것을 의미. 반대로, "status": 0은 호스트를 활성화(enable) 상태로 설정
                    },
                    "auth": token,
                    "id": 2
                }
                
                disable_response = requests.post(url, headers=headers, data=json.dumps(disable_data))
                disable_result = disable_response.json()

                if 'result' in disable_result and disable_result['result']:
                    print(f"{hostname} ({expected_ip}) 호스트가 성공적으로 비활성화되었습니다.")
                    success_hosts.append(hostname)
                else:
                    print(f"{hostname} ({expected_ip}) 호스트 비활성화 실패: {disable_result.get('error')}")
                    msg.append(f"{hostname} ({expected_ip}) 호스트 비활성화 실패: {disable_result.get('error')}\n")
                    fail_hosts.append(hostname)
            else:
                print(f"{hostname} 호스트의 등록된 IP({registered_ip})가 입력한 IP({expected_ip})와 다릅니다.")
                msg.append(f"{hostname} 호스트의 등록된 IP({registered_ip})가 입력한 IP({expected_ip})와 다릅니다.\n")
                fail_hosts.append(hostname)
        else:
            print(f"{hostname} ({expected_ip}) 호스트를 찾을 수 없습니다.")
            msg.append(f"{hostname} ({expected_ip}) 호스트를 찾을 수 없습니다.\n")
            fail_hosts.append(hostname)
    
    return {"success": success_hosts, "fail": fail_hosts, "msg" : msg}

def enable_hosts_if_ip_matches(url, token, hosts_info):
    
    headers = {'Content-Type': 'application/json-rpc'}
    success_hosts = []
    fail_hosts = []
    msg = []

    if not hosts_info:
        print(f"enable_hosts_if_ip_matches hosts_info none!!")
        return [];

    for host_info in hosts_info:
        hostname, expected_ip = host_info

        print("hostname : " + hostname)
        print("expected_ip : " + expected_ip)
        # 호스트 및 인터페이스 정보 조회
        find_host_data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "filter": {
                    "host": [hostname]
                }
            },
            "auth": token,
            "id": 1
        }

        find_response = requests.post(url, headers=headers, data=json.dumps(find_host_data))
        find_result = find_response.json()

        print(find_result)

        if 'result' in find_result and find_result['result']:
            # 호스트의 IP 주소 검증
            host_interfaces = find_result['result'][0]['interfaces']
  
            registered_ip = host_interfaces[0]['ip'] if host_interfaces else None

            if registered_ip == expected_ip:
                # IP 주소가 일치하면, 호스트 활성화
                host_id = find_result['result'][0]['hostid']
                disable_data = {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {
                        "hostid": host_id,
                        "status": 0 # "status": 1은 호스트를 비활성화(disable)하는 것을 의미. 반대로, "status": 0은 호스트를 활성화(enable) 상태로 설정
                    },
                    "auth": token,
                    "id": 1
                }
                
                disable_response = requests.post(url, headers=headers, data=json.dumps(disable_data))
                disable_result = disable_response.json()

                if 'result' in disable_result and disable_result['result']:
                    print(f"{hostname} ({expected_ip}) 호스트가 성공적으로 활성화되었습니다.")
                    success_hosts.append(hostname)
                else:
                    print(f"{hostname} ({expected_ip}) 호스트 활성화 실패: {disable_result.get('error')}")
                    msg.append(f"{hostname} ({expected_ip}) 호스트 활성화 실패: {disable_result.get('error')}\n")
                    fail_hosts.append(hostname)
            else:
                print(f"{hostname} 호스트의 등록된 IP({registered_ip})가 입력한 IP({expected_ip})와 다릅니다.")
                msg.append(f"{hostname} 호스트의 등록된 IP({registered_ip})가 입력한 IP({expected_ip})와 다릅니다.\n")
                fail_hosts.append(hostname)
        else:
            print(f"{hostname} ({expected_ip}) 호스트를 찾을 수 없습니다.")
            msg.append(f"{hostname} ({expected_ip}) 호스트를 찾을 수 없습니다.\n")
            fail_hosts.append(hostname)
    
    return {"success": success_hosts, "fail": fail_hosts, "msg" : msg}

def zabbix_delete_api(url, token, hosts_info):
    headers = {'Content-Type': 'application/json-rpc'}
    success_hosts = []
    fail_hosts = []
    msg = []

    if not hosts_info:
        print(f"zabbix_delete_api hosts_info none!!")
        return [];

    for host_info in hosts_info:
        hostname, expected_ip = host_info

        print("hostname : " + hostname)
        print("expected_ip : " + expected_ip)
        # 호스트 및 인터페이스 정보 조회
        delete_host_data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "host"],
                "selectInterfaces": ["ip"],
                "filter": {
                    "host": [hostname]
                }
            },
            "auth": token,
            "id": 1
        }
        print(delete_host_data)
        find_response = requests.post(url, headers=headers, data=json.dumps(delete_host_data))
        find_result = find_response.json()

        print(find_result)

        if 'result' in find_result and find_result['result']:
            # 호스트의 IP 주소 검증
            host_interfaces = find_result['result'][0]['interfaces']
  
            registered_ip = host_interfaces[0]['ip'] if host_interfaces else None

            if registered_ip == expected_ip:
                # IP 주소가 일치하면, 호스트 삭제
                host_id = find_result['result'][0]['hostid']
                print(host_id)
                delete_data = {
                    "jsonrpc": "2.0",
                    "method": "host.delete",
                    "params": [
                        host_id  # host_id는 삭제하려는 호스트의 ID를 나타내는 변수입니다.
                    ],
                    "auth": token,  # token은 사용자 인증 토큰입니다.
                    "id": 2
                }
                delete_response = requests.post(url, headers=headers, data=json.dumps(delete_data))
                delete_result = delete_response.json()

                if 'result' in delete_result and delete_result['result']:
                    print(f"{hostname} ({expected_ip}) 호스트가 성공적으로 삭제되었습니다.")
                    success_hosts.append(hostname)
                else:
                    print(f"{hostname} ({expected_ip}) 호스트 삭제 실패: {delete_result.get('error')}")
                    msg.append(f"{hostname} ({expected_ip}) 호스트 삭제 실패: {delete_result.get('error')}\n")
                    fail_hosts.append(hostname)
            else:
                print(f"{hostname} 호스트의 등록된 IP({registered_ip})가 입력한 IP({expected_ip})와 다릅니다.")
                msg.append(f"{hostname} 호스트의 등록된 IP({registered_ip})가 입력한 IP({expected_ip})와 다릅니다.\n")
                fail_hosts.append(hostname)
        else:
            print(f"{hostname} ({expected_ip}) 호스트를 찾을 수 없습니다.")
            msg.append(f"{hostname} ({expected_ip}) 호스트를 찾을 수 없습니다.\n")
            fail_hosts.append(hostname)
    
    return {"success": success_hosts, "fail": fail_hosts, "msg" : msg}

def readGroupId(url, token, hostGroupNames):
    headers = {'Content-Type': 'application/json-rpc'}
    successful_groups = []

    if not hostGroupNames:
        print(f"readGroupId hostGroupNames none!!")
        return [];

    for hostGroupName in hostGroupNames:
        read_group_data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [hostGroupName]  # 호스트 그룹명을 리스트로 전달
                }
            },
            "auth": token,
            "id": 1
        }

        response = requests.post(url, headers=headers, data=json.dumps(read_group_data))
        response_json = response.json()

        # 성공적으로 조회된 호스트 그룹의 ID를 리스트에 추가
        if "result" in response_json and len(response_json["result"]) > 0:
            for group in response_json["result"]:
                successful_groups.append((group["name"], group["groupid"]))

    return successful_groups

def readTemplateId(templateName):
    return None;  # return ID


def format_host_details_to_string(host_info_list):
    details_str = ""

    for host_info in host_info_list:
        host_details = f"호스트 ID: {host_info['hostid']}, 호스트 이름: {host_info['hostname']}, IP: {host_info['ip']}\n"
        group_details = "".join([f"그룹 이름: {group['name']} (ID: {group['ID']})\n" for group in host_info['groups']])
        template_details = "".join([f"템플릿 이름: {template['name']} (ID: {template['ID']})\n" for template in host_info['templates']])
        details_str += f"{host_details}{group_details}{template_details}{'-' * 50}"
    return details_str.strip()


def main():
    # 로그인 함수 호출
    token = zabbix_login(zabbix_url, username, password)

    if token:
        print("로그인 성공. 토큰:", token)
    else:
        print("로그인 실패.")

if __name__== "__main__":
    main()