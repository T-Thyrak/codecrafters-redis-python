import socket
import threading
import multiprocessing
import re

from expdict import ExpDict

database = ExpDict()

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    
    # pool = multiprocessing.Pool()
    
    while True:
        client_socket, address = server_socket.accept()
        # pool.apply_async(handle_client, args=(client_socket, address))
        
        proc = multiprocessing.Process(target=handle_client, args=(client_socket, address))
        proc.start()
    
def handle_client(socket: socket.socket, addr):
    while True:
        data = socket.recv(1024)
        if not data:
            break
        
        str_data = data.decode("utf-8")
        
        ping_pattern = r"(?i)^\*(\d+)\r\n\$4\r\nping\r\n(\$(\d+)\r\n(.*)\r\n)?$"
        match_ping = re.match(ping_pattern, str_data)
        if match_ping:
            if match_ping.group(2):
                str_len = int(match_ping.group(3))
                str_echo = match_ping.group(4)
                
                send_data = f"${str_len}\r\n{str_echo}\r\n"
                socket.send(bytes(send_data, "utf-8"))
            else:
                socket.send(b"+PONG\r\n")
            continue
        
        echo_pattern = r"(?i)^\*2\r\n\$4\r\nECHO\r\n\$(\d+)\r\n(.*)\r\n$"
        match_echo = re.match(echo_pattern, str_data)
        
        if match_echo:
            str_len = int(match_echo.group(1))
            str_echo = match_echo.group(2)
            
            socket.send(bytes(f"${str_len}\r\n{str_echo}\r\n", "utf-8"))
            continue
        
        set_pattern = r"(?i)^\*\r\n\$3\r\nSET\r\n\$(\d+)\r\n(.*)\r\n\$(\d+)\r\n(.*)\r\n$"
        match_set = re.match(set_pattern, str_data)
        
        if match_set:
            key_len = int(match_set.group(1))
            key = match_set.group(2)
            
            value_len = int(match_set.group(3))
            value = match_set.group(4)
            
            database.set(key, value)
            
            socket.send(bytes("+OK\r\n", "utf-8"))
            continue
        
        get_pattern = r"(?i)^\*\r\n\$3\r\nGET\r\n\$(\d+)\r\n(.*)\r\n$"
        match_get = re.match(get_pattern, str_data)
        
        if match_get:
            key_len = int(match_get.group(1))
            key = match_get.group(2)
            
            value = database.get(key)
            
            if value is None:
                socket.send(bytes("$-1\r\n", "utf-8"))
            else:
                socket.send(bytes(f"${len(value)}\r\n{value}\r\n", "utf-8"))
                
            continue
        
    socket.close()

if __name__ == "__main__":
    main()
