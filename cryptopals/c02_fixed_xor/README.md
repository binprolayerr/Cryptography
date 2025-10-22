---
title: 2. Fixed_XOR

---

# 2. Fixed_XOR

## Yêu cầu

Viết một hàm nhận vào hai chuỗi (hex) có độ dài bằng nhau và trả về kết quả của phép XOR từng byte tương ứng của chúng

Đây là hai chuỗi đó
```1c0111001f010100061a024b53535009181c```
```686974207468652062756c6c277320657965```

## Hướng giải

Đầu tiên ta chuyển chuỗi hex thành byte
```javas
hex1 = bytes.fromhex("1c0111001f010100061a024b53535009181c")
hex2 = bytes.fromhex("686974207468652062756c6c277320657965")
```

Để lấy ra cặp phần tử $(x, y)$ ở vị trí tương ứng ở hai chuỗi để thực hiện xor thì ta dùng `zip(hex1, hex2)`

Ta sẽ lưu kết quả xor vào một mảng 
```javas
[a ^ b for a, b in zip(hex1, hex2)]
```

Cuối cùng chuyển mảng trên thành byte và chuyển sang chuỗi hex
```javas
hex_xor = bytes([a ^ b for a, b in zip(hex1, hex2)]).hex()
print(hex_xor)
```