import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

"""
shotgrid에서 status가 변경되었을 때, 반응하는 webhooks_report.json을 모니터링하고
변화가 있으면 특정 스크립트를 실행하여 loader에 status를 실시간으로 반영하는 스크립트입니다
"""

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        path = "/home/rapa/sub_server/pipeline/json"
        self.script_to_run ="/home/rapa/yummy/pipeline/scripts/loader/loader_script/get_datas_for_user.py"
        self.process = None 
        observer = Observer()
        observer.schedule(self, path, recursive=False)
        observer.start()
        observer.join()
        print("status monitoring start..")
        

    def on_modified(self, event):
        #webhooks_report.json의 변화를 감지
        if event.src_path == "/home/rapa/sub_server/pipeline/json/webhooks_report.json":
            print(f"{event.src_path}가 수정되었습니다.")
            if self.process:
                # 프로세스가 이미 실행 중이면 종료
                print("기존 프로세스 종료 중...")
                self.process.terminate()
                self.process.wait()  # 프로세스 종료 대기
                
            # 새로운 프로세스를 시작
            print("새 프로세스 시작 중...")
            self.process = subprocess.Popen(["python3.9", self.script_to_run])
            self.process.wait()  # 스크립트가 끝날 때까지 대기
            print("새 프로세스 완료")

if __name__ == "__main__":

    #변화가 있을 때, 실행하는 스크립트 설정
    event_handler = ChangeHandler() 

