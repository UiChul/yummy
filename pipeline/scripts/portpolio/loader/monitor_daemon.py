import subprocess
import threading
import time

"""
loader가 실행될 때 백그라운드 상태로 status_monitor.py이 실행되는 데몬 스크립트입니다.
"""

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
        except Exception as e:
            with open(self.log_path, 'a') as log_file:
                print(f"스크립트 실행 중에 오류가 발생했습니다: {e}", file=log_file)

if __name__ == "__main__":
    monitor_script = "/home/rapa/yummy/pipeline/scripts/loader/loader_script/status_monitor.py"
    log_file = "/home/rapa/yummy/pipeline/scripts/loader/monitor_log.txt"
    daemon = MonitorDaemon(monitor_script, log_file)
    daemon.start_monitoring()
    
   #스레드가 종료되지 않기 위한 무한루프
    try:
        while True:
            time.sleep(1)  #CPU 사용량 절약
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
