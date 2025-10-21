# Detect AES in ECB mode
## Yêu cầu 
In [this file](https://cryptopals.com/static/challenge-data/8.txt) are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

## AES (Advanced Encryption Standard) là gì?
Bản chất: Là một thuật toán mã hóa khối đối xứng (Symmetric Block Cipher) tiêu chuẩn và được sử dụng rộng rãi nhất trên thế giới.

Đối xứng: Sử dụng một khóa bí mật duy nhất cho cả quá trình mã hóa và giải mã.

Khối (Block): AES chia dữ liệu thành các khối có kích thước cố định là 16 byte (128 bit) để xử lý.

## Chế độ ECB (Electronic Codebook) là gì?
ECB là một trong những chế độ hoạt động (mode of operation) của AES, nhưng nó là chế độ đơn giản nhất và kém an toàn nhất.

Nguyên tắc hoạt động: Mỗi khối dữ liệu 16 byte được mã hóa hoàn toàn độc lập với các khối khác, chỉ sử dụng khóa bí mật.
## Lời giải
Đề bài chỉ yêu cầu chúng ta tìm đoạn hex-encoded ciphertexts mà bị mã hóa bằng ECB.

Một chuỗi Hex (Thập lục phân) ciphertext được mã hóa bằng ECB sẽ có các khối 32 ký tự Hex lặp lại nếu văn bản gốc (plaintext) có các khối 16 byte giống nhau.
(1 Hex = 4 bit = 1/2 bytes -> 32 Hex = 16 bytes)
    
Vì thế ta chỉ cần tìm chuỗi bị lặp 32 ký tự.

## Code
```python
data = open("8.txt", "r").read()

for s in data.split(): 
    myset = set()
    for i in range(0, len(s), 32):
        block = s[i : i + 32]
        myset.add(block)
    total_blocks = len(s) 
    unique_blocks = len(myset)
    if total_blocks > unique_blocks:
        print(s)
```

