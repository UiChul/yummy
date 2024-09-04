import socket

server_host = '192.168.5.27'
server_port = 55555

def startserver():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((server_host, server_port))
    server_sock.listen(1)
    print(f"서버가 {server_host}:{server_port}에서 대기 중입니다.")

    conn, addr = server_sock.accept()
    print(f"클라이언트 {addr}와 연결되었습니다.")

    while True:
        data = conn.recv(1024)
        if not data:
            print("클라이언트와의 연결이 끊어졌습니다.")
            break
        print(f"클라이언트로부터 받은 메시지: {data.decode()}")
        conn.sendall(data)

    conn.close()
    server_sock.close()

if __name__ == "__main__":
    startserver()
