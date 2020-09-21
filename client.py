import socket
import time
import json
import subprocess
from threading import Thread
from colorit import *
from encription import *


subprocess.call("clear", shell=True)


def print_localhost_ip(ip):
    return ip if ip != "localhost" else '127.0.0.1'


def exit_func(message):
    if message == "exit":
        #exit()
        return 1


class Client:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        print(color(f"[+] Got a connection from: ip:{ip}, port:{port}", Colors.green))

        self.pub_key = ""
        while self.pub_key == "":
            try:
                n, e = self.reliable_receive()
                self.pub_key = rsa.PublicKey(n, e)
            except Exception:
                continue
        self.reliable_send(get_pubkey(), flag=1)

        #print(color(self.pub_key, Colors.orange))

        #except Exception:
        #    time.sleep(5)


    def reliable_send(self, data, flag=0):
        if flag == 0:
            json_data = json.dumps(rsa_encrypt(data, self.pub_key))
        else:
            json_data = json.dumps(data)
        self.connection.send(json_data.encode())


    def reliable_receive(self):
        json_data = "".encode()
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def send_message(self):
        while True:
            try:
                self.message_status = True
                client_message = input("")
                self.reliable_send(client_message)
                self.message_status = False
                res = exit_func(client_message)
                if res == 1:
                    break

            except Exception:
                self.reliable_send("WTF? ITS fucking error ¯\_(ツ)_/¯")


    def get_message(self):
        while True:
            try:
                server_message = self.reliable_receive()
                message = rsa_decrypt(server_message)
                print(color(f"{message}", Colors.green))
                exit_func(server_message)

            except Exception:
                self.reliable_send("WTF? ITS fucking error ¯\_(ツ)_/¯")



    def run(self):
        self.thread1 = Thread(target=self.send_message)
        self.thread2 = Thread(target=self.get_message)
        self.thread1.start()
        self.thread2.start()
        self.thread1.join()
        self.thread2.join()
        self.connection.close()


# nickname = input("Your nickname >> ")
"""ip = input("IP to connect >> ")
port = int(input("PORT to connect >> "))
binary = input("Is everything right ?(y/n) >> ")
while binary != 'y':
    param = input("What needs to be changed ?\nip(1), port(2) enter number >> ")
    # if param == "1":
    #    nickname = input("nickname >> ")
    if param == "1":
        ip = input("ip >> ")
    else:
        port = int(input("port >> "))
    binary = input("Is everything right ?(y/n) >> ")

subprocess.call("clear", shell=True)"""

new_client = Client("192.168.1.6", 58899)
new_client.run()
