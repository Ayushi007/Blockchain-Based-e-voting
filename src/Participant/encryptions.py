import Crypto
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256*4 # use larger value in production
    private_key = RSA.generate(modulus_length, Random.new().read)
    public_key = private_key.publickey()
    return private_key, public_key

def sign(privatekey,data):
    return base64.b64encode(str((privatekey.sign(data, ''))[0]).encode())

def verify(publickey,data,sign):
     return publickey.verify(data, (int(base64.b64decode(sign)),))
