import socket
import asyncio


def handle_client(client_socket, address):
    while True:
        data = client_socket.recv(1024)
        client_socket.send(b"+PONG\r")
    
    client_socket.close()


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    loop = asyncio.get_event_loop()
    
    while True:
        client_socket, address = server_socket.accept()
        loop.create_task(handle_client(client_socket, address))
    
if __name__ == "__main__":
    main()
