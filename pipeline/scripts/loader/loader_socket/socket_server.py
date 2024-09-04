import socket
import threading

host = '192.168.5.27'
port = 55555

def handle_client(child_sock, child_addr):
    print(f'{child_addr}에서 접속')
    try:
        while True:
            message = child_sock.recv(1024)
            if not message:
                break
            print(f'{child_addr}: {message.decode()}')
            child_sock.sendall(message)
    except ConnectionResetError:
        print(f'{child_addr} 연결이 끊어졌습니다.')
    finally:
        child_sock.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as parent_sock:
        parent_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        parent_sock.bind((host, port))
        parent_sock.listen(5)
        print(f'Server IP: {host}, Port Num: {port}로 서버 실행 중...')

        while True:
            try:
                child_sock, child_addr = parent_sock.accept()
                client_thread = threading.Thread(target=handle_client, args=(child_sock, child_addr))
                client_thread.start()
            except KeyboardInterrupt:
                print("서버를 종료합니다.")
                break

if __name__ == "__main__":
    start_server()
