# Đọc file 6.txt
import base64
with open(r"6.txt", "r") as f:
    data = f.read()
ciphertext = base64.b64decode(data)

# Hàm khoảng cách Hamming - Hdistance()
'''Giải thích hàm Hdistance
Input 2 bytes b1, b2
Tạo biến cộng dồn distance = 0
Với mỗi cặp x, y trong zip(b1, b2)
Nếu x ^ y = 1 (nghĩa là x khác y) thì distance += 1
'''
def Hdistance(b1, b2):
    assert len(b1) == len(b2)
    distance = 0
    for x, y in zip(b1, b2):
        # XOR từng byte rồi đếm số bit 1 trong kết quả
        distance += bin(x ^ y).count("1")
    return distance

string_1 = b"this is a test"
string_2 = b"wokka wokka!!!"

min_keysize = 2
max_keysize = 40

# Hàm dự đoán độ dài của khóa key thực tế
def guess_keysize(ciphertext):
    result_keysize = []
    for keysize in range(min_keysize, max_keysize + 1):
        abcde = len(ciphertext) // (2 * keysize) - 1
        score = 0
        for i in range(abcde):
            str1 = ciphertext[2*i*keysize:(2*i+1)*keysize]
            str2 = ciphertext[(2*i+1)*keysize:2*(i+1)*keysize]
            score += Hdistance(str1, str2)
        score /= (keysize * abcde)
        result_keysize.append((keysize, score))
    new_result = sorted(result_keysize, key = lambda x: x[1])
    return new_result[0][0]

KEYSIZE = guess_keysize(ciphertext)

# Chia nhỏ đoạn ciphertext ra thành các blocks có độ dài KEYSIZE lưu vào trong một array
break_ciphertext = [ciphertext[i:i+KEYSIZE] for i in range(0, len(ciphertext), KEYSIZE)]

# break_ciphertext lúc này là  một ma trận, ta cần chuyển vị ma trận đó
from itertools import zip_longest
transposed_array = list(zip_longest(*break_ciphertext, fillvalue=0))

# Tạo mảng lưu các kí tự của văn bản tiếng anh
ascii_text = list(range(97, 123)) + list(range(65, 91)) + [32]
rate = 0.9

# Hàm đánh giá độ giống tiếng anh
def score_text_string(string):
    score_text = sum([x in ascii_text for x in string]) / len(string)
    return score_text

# Hàm giải mã từng khối sau hoán vị
def break_block(block):
    result = []
    for key in range(256):
        string_temp = bytes([c ^ key for c in block])
        result.append((key, score_text_string(string_temp)))
    return sorted(result, key=lambda x: x[1], reverse=True)

# Tạo mảng lưu các kí tự sau khi giải mã
my_xor_key = [break_block(transposed_array[number])[0][0] for number in range(KEYSIZE)]
print(bytes([ciphertext[num] ^ my_xor_key[num%len(my_xor_key)] for num in range(len(ciphertext))]).decode())
