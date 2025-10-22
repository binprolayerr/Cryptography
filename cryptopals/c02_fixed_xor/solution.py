from Crypto.Util.number import*

# hex decoding
hex1 = bytes.fromhex("1c0111001f010100061a024b53535009181c")
hex2 = bytes.fromhex("686974207468652062756c6c277320657965")

#xor
hex_xor = bytes(a ^ b for a, b in zip(hex1, hex2)).hex()
print(hex_xor)
