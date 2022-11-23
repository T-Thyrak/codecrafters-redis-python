import socket
import threading
import multiprocessing
import re

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    pool = multiprocessing.Pool()
    
    while True:
        client_socket, address = server_socket.accept()
        pool.apply_async(handle_client, args=(client_socket, address))
    
def handle_client(socket, addr):
    while True:
        data = socket.recv(1024)
        # if not data:
        #     break
        
        if data == b"+PING\r\n":
            socket.send(b"+PONG\r\n")
        else:
            str_data = data.decode("utf-8")
            echo_pattern = r"\*2\r\n\$4\r\nECHO\r\n$(\d+)\r\n(.+)\r\n"
            match_echo = re.match(echo_pattern, str_data)
            
            if match_echo:
                str_len = int(match_echo.group(1))
                str_echo = match_echo.group(2)
                
                socket.send(bytes(f"${str_len}\r\n{str_echo}\r\n", "utf-8"))
        
    socket.close()

if __name__ == "__main__":
    main()
