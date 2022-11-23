import socket
import threading
import multiprocessing
import re

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    pool = multiprocessing.Pool()
    
    while True:
        client_socket, address = server_socket.accept()
        pool.apply_async(handle_client, args=(client_socket, address), callback=lambda _: _)
    
def handle_client(socket: socket.socket, addr):
    while True:
        data = socket.recv(1024)
        # if not data:
        #     break
        
        str_data = data.decode("utf-8")
        
        ping_pattern = r"(?i)\*(\d+)\r\n\$4\r\nping\r\n(\$(\d+)\r\n(.*)\r\n)?"
        match_ping = re.match(ping_pattern, str_data)
        print(match_ping)
        if match_ping:
            if match_ping.group(2):
                str_len = int(match_ping.group(3))
                str_echo = match_ping.group(4)
                
                send_data = f"${str_len}\r\n{str_echo}\r\n"
                print(f"Sent with echo: {send_data}")
                socket.send(bytes(send_data, "utf-8"))
            else:
                print("Sent without echo")
                socket.send(b"+PONG\r\n")
                print("After send")
            continue
        
        echo_pattern = r"(?i)\*2\r\n\$4\r\nECHO\r\n$(\d+)\r\n(.*)\r\n"
        match_echo = re.match(echo_pattern, str_data)
        print(match_echo)
        
        if match_echo:
            str_len = int(match_echo.group(1))
            str_echo = match_echo.group(2)
            
            socket.send(bytes(f"${str_len}\r\n{str_echo}\r\n", "utf-8"))
            continue
    
    socket.close()

if __name__ == "__main__":
    main()
