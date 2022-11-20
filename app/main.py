import socket
import asyncio
import threading


async def handle_client(loop: asyncio.AbstractEventLoop, client_socket, address):
    while True:
        data = await loop.sock_recv(client_socket)
        
        loop.sock_sendall(client_socket, b"+PONG\r\n")
    
    connection.close()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    loop = asyncio.get_event_loop()
    
    while True:
        client_socket, address = server_socket.accept()
        loop.create_task(handle_client(loop, client_socket, address))
    
if __name__ == "__main__":
    main()
