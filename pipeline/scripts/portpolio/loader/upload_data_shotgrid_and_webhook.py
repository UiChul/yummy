import shotgun_api3
import requests
import json
import hmac
import hashlib
import uuid
from datetime import datetime

"""
스크립트로 shotgrid에 데이터 업로드를 했을 때, 
webhook이 반응하지 않는 이슈가 있어 만든 테스트 스크립트입니다.
shotgrid와 webhook에 동시에 데이터를 전송하여 webhook이 반응되게 하였습니다.
"""

class UploadToShotgun:
    # ShotGrid 서버 정보와 인증 정보 설정
    URL = "https://4thacademy.shotgrid.autodesk.com"
    SCRIPT_NAME = "test_hyo"
    API_KEY = "ljbgffxqg@cejveci5dQebhdx"

    # 웹훅 엔드포인트 URL과 시크릿 키
    WEBHOOK_URL = "https://3755-1-11-90-40.ngrok-free.app/webhook"  #ngrok 무료버전으로 url이 생성되기 때문에 url이 매번 바뀜
    WEBHOOK_SECRET = ""  # 웹훅에 설정해둔 키

    # ShotGrid 서버에 연결
    sg = shotgun_api3.Shotgun(URL, SCRIPT_NAME, API_KEY)

    # 버전을 추가할 프로젝트 ID 설정
    project_id = 222  # 프로젝트 id 필수 입력 (현재 YUMMIE(id:222) 프로젝트로 설정)

    # 랜덤한 UUID 생성 (딜리버리 아이디)
    delivery_id = str(uuid.uuid4())

    # 버전 또는 퍼블리시 생성 선택
    action = input("Choose action (version/publish): ").strip().lower()

    if action == "version":
        # 추가할 버전의 데이터 정의
        version_data = {
            'project': {'type': 'Project', 'id': project_id},
            'code': '0830 TEST5', #version name 필수 입력
            'description': 'This is a test version.'
        }

        # 버전 생성
        new_version = sg.create('Version', version_data)

        # 생성된 버전 출력
        print(f"Created Version: {new_version['id']} with name: {new_version['code']}")

        # 웹훅에 전달할 데이터
        webhook_data = {
            "data": {
                "id": f"{new_version['id']}.765.0",
                "event_log_entry_id": new_version['id'],
                "event_type": "Version Created",
                "operation": "create",
                "user": {
                    "type": "HumanUser",
                    "id": SCRIPT_NAME   # 현재 스크립트를 실행하는 사용자 id로 적어주세요
                },
                "entity": {
                    "type": "Version",
                    "id": new_version['id']
                },
                "project": {
                    "type": "Project",
                    "id": project_id
                },
                "meta": {
                    "type": "version_created",
                    "entity_type": "Version",
                    "entity_id": new_version['id'],
                    "hook_id": "8eb5c438-684c-40e3-8a13-2c6e75446f1e"
                },
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                "attribute_name": None,
                "session_uuid": None,
                "delivery_id": delivery_id
            },
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    elif action == "publish":
        # 추가할 퍼블리시의 데이터 정의
        publish_data = {
            'project': {'type': 'Project', 'id': project_id},
            'code': 'PUBLISH_TEST1', #퍼블리시 네임 필수 입력
            'description': 'This is a test publish.'
        }

        # 퍼블리시 생성
        new_publish = sg.create('PublishedFile', publish_data)

        # 생성된 퍼블리시 출력
        print(f"Created Publish: {new_publish['id']} with name: {new_publish['code']}")

        # 웹훅에 전달할 데이터
        webhook_data = {
            "data": {
                "id": f"{new_publish['id']}.765.0",
                "event_log_entry_id": new_publish['id'],
                "event_type": "Shotgun_PublishedFile_New",
                "operation": "create",
                "user": {
                    "type": "HumanUser",
                    "id": SCRIPT_NAME   # 현재 스크립트를 실행하는 사용자 id로 적어주세요
                },
                "entity": {
                    "type": "PublishedFile",
                    "id": new_publish['id']
                },
                "project": {
                    "type": "Project",
                    "id": project_id
                },
                "meta": {
                    "type": "publish_created",
                    "entity_type": "PublishedFile",
                    "entity_id": new_publish['id'],
                    "hook_id": "8eb5c438-684c-40e3-8a13-2c6e75446f1e"
                },
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                "attribute_name": None,
                "session_uuid": None,
                "delivery_id": delivery_id
            },
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    else:
        print("Invalid action. Please choose either 'version' or 'publish'.")
        exit()

    # 웹훅 요청을 위한 헤더 설정
    headers = {
        'Content-Type': 'application/json',
        'x-sg-signature': 'sha1=' + hmac.new(WEBHOOK_SECRET.encode(), json.dumps(webhook_data).encode(), hashlib.sha1).hexdigest()
    }

    # 웹훅 요청 전송
    response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(webhook_data))

    # 응답 출력
    print(f"Webhook response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    UploadToShotgun()