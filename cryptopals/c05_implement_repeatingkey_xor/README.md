---
title: README

---

# 5. Implement repeating-key XOR

## Yêu cầu

Cho hai câu tiếng anh
```
Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal
```

Hãy mã hóa hai câu trên bằng cách sử dụng repeating-key XOR với key "ICE", kết quả mã hóa ở dạng hex_string

## Giải thích

Repeating-key XOR là một kĩ thuật mã hóa với các kí tự từ plaintext sẽ lần lược XOR với một kí tự trong key theo chu kì.

Ví dụ với key = "ICE", lúc này
```python
ciphertext[0] = plaintext[0] ^ 'I'
ciphertext[1] = plaintext[1] ^ 'C'
ciphertext[2] = plaintext[2] ^ 'E'
ciphertext[3] = plaintext[3] ^ 'I'
ciphertext[4] = plaintext[4] ^ 'E'
...
```
Cứ như thế cho đến hết plaintext

## Hướng giải

Đầu tiên chuyển 2 câu tiếng anh và key "ICE" thành byte
```python
string1 = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"
```

Tạo mảng để lưu các kí tự sau khi xor
```python
[string1[num] ^ key[num%len(key)] for num in range(len(string1))]
```
chỉ số mảng `num%len(key)` sẽ chạy lần lượt `0, 1, ..., len(key)-1, 0, 1, ...` lặp lại như vậy.

Cuối cùng chuyển mảng trên thành byte và in ra
```python
print(bytes([string1[num] ^ key[num%len(key)] for num in range(len(string1))]).hex())
```