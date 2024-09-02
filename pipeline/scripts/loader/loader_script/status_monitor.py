import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

# 첫 번째 ChangeHandler: 기존 스크립트를 실행하는 핸들러
class ChangeHandler1(FileSystemEventHandler):
    def __init__(self, script_to_run, post_process_function=None):
        self.script_to_run = script_to_run
        self.process = None
        self.post_process_function = post_process_function  # 후속 처리를 위한 함수
        print("ChangeHandler1 초기화 완료")

    def on_modified(self, event):
        if event.src_path == "/home/rapa/yummy/pipeline/json/webhooks_report.json":
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

            # 후속 처리 함수 호출
            if self.post_process_function:
                self.post_process_function()
                print("후속 처리 완료")

if __name__ == "__main__":
    path = "/home/rapa/yummy/pipeline/json"

    # 첫 번째 핸들러 설정
    def post_process():
        print("후속 처리 로직 실행")

    event_handler1 = ChangeHandler1(
        script_to_run="/home/rapa/yummy/pipeline/scripts/loader/loader_script/get_datas_for_user.py",
        post_process_function=post_process
    )

    # Observer에 핸들러를 등록
    observer = Observer()
    observer.schedule(event_handler1, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
