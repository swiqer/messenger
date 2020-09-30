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

        while True:
            try:
                self.reliable_send(get_pubkey(), flag=1)
                break
            except Exception:
                continue
        
        self.pub_key = ""
        while self.pub_key == "":
            try:
                n, e = self.reliable_receive()
                self.pub_key = rsa.PublicKey(n, e)
            except Exception:
                print(color("[!] Error saved key", Colors.red))
                continue


    def reliable_send(self, data, flag=0):
        if flag == 0:
            json_data = json.dumps(rsa_encrypt(data, self.pub_key))
            #json_data = json.dumps(data)
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
                if client_message == "exit":
                    #self.thread1.join()
                    #self.thread2.join()
                    #self.connection.close()
                    sys.exit()

            except Exception:
                self.reliable_send("WTF? ITS fucking error ¯\_(ツ)_/¯")


    def get_message(self):
        while True:
            try:
                server_message = self.reliable_receive()
                message = rsa_decrypt(server_message)
                #message = server_message
                print(color(f"{message}", Colors.green))
                if message == "exit":
                    #self.thread1.join()
                    #self.thread2.join()
                    #self.connection.close()
                    sys.exit()


            except Exception:
                self.reliable_send("WTF? ITS fucking error ¯\_(ツ)_/¯")



    def run(self):
        self.thread1 = Thread(target=self.send_message)
        self.thread2 = Thread(target=self.get_message)
        self.thread1.start()
        self.thread2.start()
        self.thread1.join()
        self.thread2.join()
        


# nickname = input("Your nickname >> ")
ip = "165.227.141.219"
port = 50005
print(color("IP", Colors.blue) + " to connect >> " + color(f"{ip}\n", Colors.blue))
print(color("PORT", Colors.blue) + " to connect >> " + color(f"{port}\n", Colors.blue))
binary = input(color("[!] ", Colors.yellow) + "Is everything right ? (" + color("y", Colors.green) + "/" + color("n", Colors.red) + ") " + color(">> ", Colors.yellow))
while binary != 'y':
    param = input(color("[!] ", Colors.yellow) + "What needs to be changed ?\n" + color("ip", Colors.blue) + "("+ color("1", Colors.orange) + "), "+ color("port", Colors.blue)+"("+ color("2",Colors.orange) + ") enter " + color("number", Colors.orange) +" >> ")
    # if param == "1":
    #    nickname = input("nickname >> ")
    if param == "1":
        ip = input(color("ip", Colors.blue) + " >> ")
    else:
        port = int(input(color("port", Colors.blue) + " >> "))
    subprocess.call("clear", shell=True)
    print(color("IP", Colors.blue) + " to connect >> " + color(f"{ip}\n", Colors.blue))
    print(color("PORT", Colors.blue) + " to connect >> " + color(f"{port}\n", Colors.blue))
    binary = input(color("[!] ", Colors.yellow) + "Is everything right ? (" + color("y", Colors.green) + "/" + color("n", Colors.red) + ") " + color(">> ", Colors.yellow))
    

subprocess.call("clear", shell=True)

new_client = Client(ip, port)
new_client.run()
