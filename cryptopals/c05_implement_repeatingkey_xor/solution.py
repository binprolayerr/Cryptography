string1 = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"

print(bytes([string1[num] ^ key[num%len(key)] for num in range(len(string1))]).hex())
