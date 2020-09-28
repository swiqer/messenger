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
    def __init__(self, ip, port):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen()

        print(color("[!] Waiting for incoming connections ...", Colors.yellow))
        self.client_socket, addr = self.server.accept()
        print(color(f"[+] Got a connection from: ip:{addr[0]}, port:{addr[1]}", Colors.green))
        
        self.pub_key = ""
        self.reliable_send(get_pubkey(),flag=1)
        while self.pub_key == "":
            try:
                n, e = self.reliable_receive()
                self.pub_key = rsa.PublicKey(n, e)
            except Exception:
                continue

        #print(color(self.pub_key, Colors.orange))


    def reliable_send(self, data, flag=0):
        if flag == 0:
            json_data = json.dumps(rsa_encrypt(data, self.pub_key))
        else:
            json_data = json.dumps(data)
        self.client_socket.send(json_data.encode())

    def reliable_receive(self):
        json_data = "".encode()
        while True:
            try:
                json_data = json_data + self.client_socket.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def send_message(self):
        while True:
            try:
                self.message_status = True
                server_message = input("")
                self.reliable_send(server_message)
                self.message_status = False
                res = exit_func(server_message)
                if res == 1:
                    break

            except Exception:
                self.reliable_send("WTF? ITS fucking error ¯\_(ツ)_/¯")

    def get_message(self):
        while True:
            try:
                client_message = self.reliable_receive()
                message = rsa_decrypt(client_message)
                print(color(f"{message}", Colors.green))
                exit_func(client_message)

            except Exception:
                self.reliable_send("WTF? ITS fucking error ¯\_(ツ)_/¯")


    def run(self):
        self.thread1 = Thread(target=self.send_message)
        self.thread2 = Thread(target=self.get_message)
        self.thread1.start()
        self.thread2.start()
        self.thread1.join()
        self.thread2.join()
        self.server.close()
        exit()


new_server = Server('192.168.1.4', 58899)
new_server.run()
