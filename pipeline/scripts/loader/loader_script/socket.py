import socket
from _thread import start_new_thread

HOST = '0.0.0.0'  # 서버의 공인 IP 주소로 변경
PORT = 9999

def recvdata(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("서버와의 연결이 끊어졌습니다.")
                break
            print("받은 메시지: ", repr(data.decode()))
        except Exception as e:
            print(f'데이터 수신 오류: {e}')
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            print('>> 서버에 연결됨')

            # 서버에서 이름 입력 요청
            name = input("이름을 입력하세요: ")
            client_socket.sendall(name.encode())

            start_new_thread(recvdata, (client_socket,))

            while True:
                message = input()
                if message.lower() == 'quit':
                    print("연결 종료...")
                    break
                client_socket.send(message.encode())

        except Exception as e:
            print(f'오류: {e}')

    client_socket.close()

if __name__ == "__main__":
    main()