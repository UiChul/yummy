import subprocess
import threading
import time
import os

class MonitorDaemon:
    def __init__(self, script_path, log_path):
        self.script_path = script_path
        self.log_path = log_path

    def start_monitoring(self):
        monitor_thread = threading.Thread(target=self.run_script)
        monitor_thread.daemon = True
        monitor_thread.start()
        return monitor_thread

    def run_script(self):
        try:
            # 경로와 권한 확인
            if not os.path.exists(self.script_path):
                raise FileNotFoundError(f"스크립트 파일이 존재하지 않습니다: {self.script_path}")
            
            with open(self.log_path, 'a') as log_file:
                print(f"Executing script: {self.script_path}", file=log_file)
                process = subprocess.Popen(
                    ["python3.9", self.script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = process.communicate()
                if process.returncode == 0:
                    print("status_monitor가 성공적으로 작동 중입니다.", file=log_file)
                else:
                    print(f"오류 발생: {stderr.decode()}", file=log_file)
                # stdout도 기록
                if stdout:
                    print(f"출력: {stdout.decode()}", file=log_file)
        except Exception as e:
            with open(self.log_path, 'a') as log_file:
                print(f"스크립트 실행 중에 오류가 발생했습니다: {e}", file=log_file)

if __name__ == "__main__":
    monitor_script = "/home/rapa/yummy/pipeline/scripts/loader/loader_script/status_monitor.py"
    log_file = "/home/rapa/yummy/pipeline/scripts/loader/monitor_log.txt"
    
    # 로그 파일이 있는지 확인하고 새로 생성
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    
    daemon = MonitorDaemon(monitor_script, log_file)
    daemon.start_monitoring()
    
    # Main thread를 계속 실행
    try:
        while True:
            time.sleep(1)  # CPU 사용을 줄이기 위해 대기
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
