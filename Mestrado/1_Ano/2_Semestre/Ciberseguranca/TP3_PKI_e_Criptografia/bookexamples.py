# Example 1 - AES
from Crypto.Cipher import AES
import os

seckey=os.urandom(16)
print(seckey)
print(seckey.hex())

cipher=AES.new(seckey, AES.MODE_EAX)
nonce=cipher.nonce

msg=b'This is (like) a secret!'
pad_msg=msg+(b'#'*((16-len(msg)) % 16))
print(pad_msg)

enc_msg=cipher.encrypt(pad_msg)
print(enc_msg)
print(enc_msg.hex())

decipher=AES.new(seckey, AES.MODE_EAX, nonce)
dec_msg=decipher.decrypt(enc_msg)
print(dec_msg)

# Example 2 - RSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

KeyPair=RSA.generate(2048)
pubKey=KeyPair.publickey()
print(f"Public key: (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
print(f"Private key: (n={hex(pubKey.n)}, d={hex(KeyPair.d)})")

# Armored format PEM
pubKeyPEM=pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))

privKeyPEM=KeyPair.exportKey()
print(privKeyPEM.decode('ascii'))

msg=b'This is (like) a secret!'
encryptor=PKCS1_OAEP.new(pubKey)
enc_msg=encryptor.encrypt(msg)
print("Encrypted: ", binascii.hexlify(enc_msg))

decryptor=PKCS1_OAEP.new(KeyPair)
dec_msg=decryptor.decrypt(enc_msg)
print("Decrypted: ", dec_msg)

# Example 3 - Hashes
from Crypto.Hash import MD5
h=MD5.new()
h.update(b'A simple message.')
h.hexdigest()

h.update(b'a simple message.')
h.hexdigest()

from Crypto.Hash import SHA3_256
h=SHA3_256.new()
h.update(b'A simple message.')
h.hexdigest()

h=SHA3_256.new()
h.update(b'a simple message.')
h.hexdigest()

# Example 4 - Digital SIgnatures
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
import binascii
keypair=RSA.generate(bits=1024)
msg=b'A message to sign'
msgdigest=SHA256.new(msg)
msgdigest.hexdigest()

signer=pss.new(keypair)
signature=signer.sign(msgdigest)
print("Signature: ", signature.hex())

try:
    signer.verify(msgdigest, signature)
    print("Signature is valid")
except:
    print("Signature is invalid")

msg=b'A message to sign!'
msgdigest=SHA256.new(msg)
try:
    signer.verify(msgdigest, signature)
    print("Signature is valid")
except:
      print("Signature is invalid")