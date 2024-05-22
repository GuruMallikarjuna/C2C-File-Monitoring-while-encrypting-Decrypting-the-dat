# server.py
import socket

def start_server(host='0.0.0.0', port=80):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")
        
        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connected by {addr}")
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    print("Received:", data.decode())

if __name__ == "__main__":
    start_server()

