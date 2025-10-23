
# 7. AES in ECB mode
**Yêu cầu**: 
---
Giải mã một file đã được mã hóa bằng AES-128 ở chế độ ECB.

Hướng giải
---
Đọc chuỗi hex từ file mà đề cho.
```python
with open('7.txt', 'r') as f:
    data = f.read().replace('\n', '')
```
Decode data từ hex thành base64.
```python
ciphertext = base64.b64decode(data)
```
Tạo bộ giải mã AES với key = "YELLOW SUBMARINE" ở chế độ ECB.
```python
cipher = AES.new(key, AES.MODE_ECB)
final = cipher.decrypt(ciphertext)
```
In ra kết ra chuỗi kết quả sau khi giải mã.
```py
print(final.decode())
```
