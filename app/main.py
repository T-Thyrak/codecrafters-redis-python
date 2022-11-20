import socket
import threading
import multiprocessing

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    pool = multiprocessing.Pool()
    
    while True:
        client_socket, address = server_socket.accept()
        pool.apply_async(handle_client, args=(client_socket, address))
    
def handle_client(socket, addr):
    while True:
        data = socket.recv(1024)
        socket.send(b"+PONG\r\n")
        
    socket.close()

if __name__ == "__main__":
    main()
