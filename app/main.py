import socket
import asyncio
import threading

threads = []

async def handle_client(loop: asyncio.AbstractEventLoop, client_socket, address):
    def func(socket, addr):
        while True:
            data = socket.recv(1024)
            socket.send(b"+PONG\r\n")
        socket.close()
    
    thread = threading.Thread(target=func, args=(client_socket, address))
    threads.append(thread)
    
    thread.start()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    loop = asyncio.get_event_loop()
    
    while True:
        client_socket, address = server_socket.accept()
        loop.create_task(handle_client(loop, client_socket, address))
    
if __name__ == "__main__":
    main()
