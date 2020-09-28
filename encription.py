import rsa
import base64
import json
from colorit import *

(SWIQER_PUB, SWIQER_PRIV) = rsa.newkeys(1024)


def get_pubkey():
    return  SWIQER_PUB.n, SWIQER_PUB.e


def rsa_encrypt(message, pub_key=0):
    try:
        message = rsa.encrypt(message.encode('utf-8'), pub_key)
        fuck = base64.b64encode(message).decode('ascii')
        return fuck
    except Exception:
        print(color("[!] Encript ERROR", Colors.red))
    

def rsa_decrypt(message):
    try:
        message = base64.b64decode(message)
        return rsa.decrypt(message, SWIQER_PRIV).decode('utf-8')
    except Exception:
        print(color("[!] Decrypt ERROR", Colors.red))



#message = rsa.encrypt(message.encode('utf-8'), SWIQER_PUB)
#print(rsa_encrypt("go fuck"))
#print(rsa_decrypt(rsa_encrypt("Test RSA")))