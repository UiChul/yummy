import socket

server_host = '192.168.5.27'
server_port = 55555

def start_client():
    try:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 서버와 연결
        client_sock.connect((server_host, server_port))
        print(f'Server: {server_host}, {server_port}와 정상적으로 연결')

        while True:
            message = input(">>> ")
            if message.lower() == 'exit':
                print("연결 종료 중...")
                break
            client_sock.sendall(message.encode('utf-8'))

            try:
                response = client_sock.recv(1024)
                if not response:
                    print("서버와의 연결이 끊어졌습니다.")
                    break
                print(f"server: {response.decode()}")
            except socket.error as e:
                print(f"수신 오류: {e}")
                break

    except socket.error as e:
        print(f"소켓 오류: {e}")
    finally:
        client_sock.close()

if __name__ == "__main__":
    start_client()
