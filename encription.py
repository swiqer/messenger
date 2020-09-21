import rsa
import base64
import json

(SWIQER_PUB, SWIQER_PRIV) = rsa.newkeys(1024)


def get_pubkey():
    return  SWIQER_PUB.n, SWIQER_PUB.e


def rsa_encrypt(message, pub_key=0):
    message = rsa.encrypt(message.encode('utf-8'), pub_key)
    fuck = base64.b64encode(message).decode('ascii')
    return fuck
    

def rsa_decrypt(message):
    message = base64.b64decode(message)
    return rsa.decrypt(message, SWIQER_PRIV).decode('utf-8')



#message = rsa.encrypt(message.encode('utf-8'), SWIQER_PUB)
#print(rsa_encrypt("go fuck"))
#print(rsa_decrypt(rsa_encrypt("Test RSA")))