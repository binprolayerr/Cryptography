# chuyển chuỗi hex sang nhị phân (bytes)
hex_num = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

# tạo danh sách các kí tự trong bảng chữ cái, cùng với kí tự khoảng trống ' ' (dấu cách)
ascii_text = list(range(97, 123)) + list(range(65, 91)) + [32]

def text_probability(string, rate):
    probability = sum([x in ascii_text for x in string]) / len(string)
    if probability > rate: return 1
    else: return 0

# Khai báo rate và tạo biến mảng để lưu giá trị
rate = 0.8
result = []

for key in range(256):
    string_temp = bytes([c ^ key for c in hex_num])
    if text_probability(string_temp, rate) == 1:
        result.append((string_temp.decode(errors='ignore'), key))

print(result)

# với rate = 0.8, in ra message mà xor_key tìm được
print(result[0][0], "\nmy_single_xor_key:", chr(result[0][1]))
