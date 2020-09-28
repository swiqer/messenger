import socket
import json
import subprocess
from threading import Thread
from colorit import *
from encription import *


subprocess.call("clear", shell=True)


def exit_func(message):
    if message == "exit":
        return 1


class Server:
    def __init__(self, ip, port1, port2):

        self.server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server1.bind((ip, port1))
        self.server1.listen()

        print(color("[!] Waiting for incoming connections ...", Colors.yellow))
        self.client_socket1, self.addr1 = self.server1.accept()
        print(color(f"[+] Got a connection from: ip:{self.addr1[0]}, port:{self.addr1[1]}", Colors.green))
        
        self.server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server2.bind((ip, port2))
        self.server2.listen()

        print(color("[!] Waiting for incoming connections ...", Colors.yellow))
        self.client_socket2, self.addr2 = self.server2.accept()
        print(color(f"[+] Got a connection from: ip:{self.addr2[0]}, port:{self.addr2[1]}", Colors.green))
        

        pub_key1 = ""
        while pub_key1 == "":
            try:
                pub_key1 = self.reliable_receive_1(1)
            except Exception:
                continue
        print(color(f"[+] Got a pub_key1", Colors.green))

        pub_key2 = ""
        while pub_key2 == "":
            try:
                pub_key2 = self.reliable_receive_2(1)
            except Exception:
                continue
        print(color(f"[+] Got a pub_key2", Colors.green))


        self.reliable_send_1(pub_key2)
        self.reliable_send_2(pub_key1)
        
    


    def reliable_send_1(self, json_data):
        self.client_socket2.send(json_data)

    def reliable_receive_1(self, flag=0):
        json_data = "".encode()
        while True:
            try:
                json_data = json_data + self.client_socket1.recv(1024)
                if flag == 0:
                    self.reliable_send_1(json_data)
                elif flag == 1:
                    return json_data
            except ValueError:
                continue


    def reliable_send_2(self, json_data):
        self.client_socket1.send(json_data)

    def reliable_receive_2(self, flag=0):
        json_data = "".encode()
        while True:
            try:
                json_data = json_data + self.client_socket2.recv(1024)
                if flag == 0:
                    self.reliable_send_2(json_data)
                elif flag == 1:
                    return json_data
            except ValueError:
                continue

    def start_1(self):
        while True:
            self.reliable_receive_1()
    
    def start_2(self):
        while True:
            self.reliable_receive_2()


    def run(self):
        self.thread1 = Thread(target=self.start_1)
        self.thread2 = Thread(target=self.start_2)
        self.thread1.start()
        self.thread2.start()
        self.thread1.join()
        self.thread2.join()
        self.server1.close()
        self.server2.close()


new_server = Server('192.168.1.4', 50028, 50029)
new_server.run()
