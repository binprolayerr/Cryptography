import base64
from Crypto.Cipher import AES
key = b'YELLOW SUBMARINE'

with open('7.txt', 'r') as f:
    data = f.read().replace('\n', '')

ciphertext = base64.b64decode(data)
cipher = AES.new(key, AES.MODE_ECB)
final = cipher.decrypt(ciphertext)
print(final.decode())
