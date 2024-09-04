from flask import Flask, request, jsonify
import json
import os
import threading
import time

"""
shotgrid에서 status 상태가 변경되었을 때, 
flask로 webhooks 반응을 받아 webhooks_report.json에 데이터 저장하는 스크립트입니다
이 스크립트가 실행 후 ngrok을 실행하여 shotgrid에서 인식할 수 있는 url로 변경합니다.
"""

class WebhookServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port

        @self.app.route('/webhook', methods=['POST'])  # http://127.0.0.1:5000/webhook >> ngrok >> URL/webhook으로 보내지는 POST요청에 반응
        def webhook():
            data = request.get_json() # json 데이터 파싱
            print("Received webhook data:")
            print(json.dumps(data, indent=4, ensure_ascii=False))

            self.save_json_to_file(data)

            response_data = {
                'status': 'success',
                'received_data': data
            }

            return jsonify(response_data), 200

    def save_json_to_file(self, new_data):
        file_path = "/home/rapa/sub_server/pipeline/json/webhooks_report.json"
        
        # 기존 파일이 있으면 데이터를 불러온다.
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # 새 데이터를 기존 데이터에 추가
        existing_data.append(new_data)

        # json 파일에 다시 저장
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
        
        print(f"Data saved to {file_path}")

    def run(self):
        self.app.run(host=self.host, port=self.port)

    def run_in_background(self):
        threading.Thread(target=self.run, daemon=True).start()

if __name__ == '__main__':
    server = WebhookServer()
    server.run_in_background()

    # 메인 스레드에서 다른 작업을 수행할 수 있습니다.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server stopped by user.")
