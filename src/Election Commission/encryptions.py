import Crypto
from Crypto import Random
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA
#import base64
#from Crypto.Cipher import PKCS1_v1_5 as csign

def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256*4 # use larger value in production
    private_key = DSA.generate(modulus_length, Random.new().read)
    public_key = private_key.publickey()
    return private_key, public_key


def sign(private_key,message):
    h = SHA.new(message).digest()
    sig = private_key.sign(h,private_key)
    return h, sig 

def verify(public_key,hdata,sign):
    if public_key.verify(hdata,sign):
        return True
    else:
        return False

#def sign(privatekey,data):
#    cipher = csign.new(privatekey)
#    cipher_text = cipher.encrypt(data.encode())
#    return base64.b64encode(cipher_text)

#def verify(rsa_privatekey,b64cipher):
#     decoded_ciphertext = base64.b64decode(b64cipher)
#     plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
#     return plaintext
