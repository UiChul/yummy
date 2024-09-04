from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received webhook data:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    save_json_to_file(data)

    response_data = {
        'status': 'success',
        'received_data': data
    }

    return jsonify(response_data), 200

def save_json_to_file(new_data):
    file_path = "/home/rapa/YUMMY/pipeline/json/webhooks_report.json"
    
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

    # JSON 파일에 다시 저장
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
    
    print(f"Data saved to {file_path}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
