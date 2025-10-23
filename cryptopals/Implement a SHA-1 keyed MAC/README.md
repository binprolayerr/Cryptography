# Implement a SHA-1 keyed MAC
## Yêu cầu
Find a SHA-1 implementation in the language you code in.
Write a function to authenticate a message under a secret key by using a secret-prefix MAC, which is simply: ```SHA1(key || message)```
Verify that you cannot tamper with the message without breaking the MAC you've produced, and that you can't produce a new MAC without knowing the secret key.
## Hàm SHA hoạt động như thế nào
### 1. Khởi tạo (Initialization)
Thuật toán bắt đầu bằng cách thiết lập năm biến băm 32-bit (còn gọi là trạng thái nội bộ), ký hiệu là H0, H1, H2, H3, H4, với các giá trị hex cố định:

H_0 = 0x67452301
H_1 = 0xEFCDAB89
H_2 = 0x98BADCFE
H_3 = 0x10325476
H_4 = 0xC3D2E1F0


Các giá trị này là "số ma thuật" (magic numbers) được sử dụng để khởi tạo quá trình băm.
### 2. Xử lý Đệm Thông điệp (Message Padding)
SHA-1 xử lý thông điệp theo các khối 512 bit (64 byte). Bước đệm đảm bảo rằng thông điệp, sau khi đệm, có độ dài (tính bằng bit) là một bội số của 512, đồng thời mã hóa độ dài ban đầu của nó.Nối bit '1': Nối một bit 1 vào cuối thông điệp gốc.Nối bit '0': Nối các bit 0 cho đến khi độ dài thông điệp mới (tính bằng bit) $\equiv 448 \pmod{512}$ (chia 512 dư 448).Nối Độ dài Gốc: Nối độ dài ban đầu của thông điệp (tính bằng bit) dưới dạng một số nguyên 64-bit Big-Endian.Mục đích: Đảm bảo rằng hàm nén luôn hoạt động trên các khối 512 bit hoàn chỉnh và ngăn chặn các cuộc tấn công nhất định.
### 3. Chuẩn bị Từ Thông điệp (Word Preparation)
Sau khi thông điệp được chia thành các khối 512 bit, mỗi khối được xử lý riêng biệt:Chia khối: Mỗi khối 512 bit được chia thành 16 từ 32-bit ($W_0$ đến $W_{15}$).Mở rộng: 16 từ này được mở rộng thành 80 từ 32-bit ($W_0$ đến $W_{79}$).Đối với $t = 16$ đến $79$, mỗi từ mới được tính bằng phép XOR giữa 4 từ trước đó, sau đó xoay trái 1 bit:
\begin{align*} 
W_t = \text{ROTL}^1(W_{t-3} \oplus W_{t-8} \oplus W_{t-14} \oplus W_{t-16}) \end{align*} (ROTL: Rotate Left - Xoay Trái).

### 4. Hàm Nén (The Compression Function)
Đây là lõi của thuật toán, nơi dữ liệu thực sự được băm. Nó thực hiện 80 vòng lặp trên 5 biến băm làm việc ($A, B, C, D, E$), được khởi tạo từ $H_0$ đến $H_4$ trước khi xử lý mỗi khối 512 bit.Trong mỗi vòng $t$ (từ 0 đến 79), một giá trị Temp (tạm thời) được tính toán:$$\text{Temp} = \text{ROTL}^5(A) + f_t(B, C, D) + E + K_t + W_t \pmod{2^{32}}$$Trong đó:$A, B, C, D, E$: Các biến làm việc 32-bit.$\text{ROTL}^5(A)$: Xoay trái $A$ 5 bit.$f_t(B, C, D)$: Một hàm logic phi tuyến tính khác nhau tùy thuộc vào vòng (sử dụng XOR, AND, NOT).$K_t$: Hằng số vòng (Round Constant) 32-bit, thay đổi sau mỗi 20 vòng.$W_t$: Từ thông điệp đã mở rộng ở vòng $t$.$+$: Phép Cộng Modulo $2^{32}$.Sau khi tính toán $\text{Temp}$, các biến làm việc được cập nhật:
\begin{align*} E &= D \\ D &= C \\ C &= \text{ROTL}^{30}(B) \\ B &= A \\ A &= \text{Temp} \end{align*}
Cập nhật Trạng thái BămSau khi hoàn thành 80 vòng lặp cho một khối 512 bit, các biến làm việc ($A, B, C, D, E$) được cộng (modulo $2^{32}$) vào các giá trị băm khởi tạo $H_0$ đến $H_4$:$$H_i = H_i + \text{Biến làm việc tương ứng } \pmod{2^{32}}$$Quy trình này được lặp lại cho tất cả các khối 512 bit đã được đệm.
### 5. Kết quả Đầu ra (Final Hash)
Giá trị băm SHA-1 cuối cùng là sự nối (concatenation) của năm giá trị băm cuối cùng:$$\text{Hash} = H_0 \text{ || } H_1 \text{ || } H_2 \text{ || } H_3 \text{ || } H_4$$Kết quả là một giá trị băm 160-bit (40 ký tự hexa).
## Code
```python
import struct

# --- Các Hàm Xử Lý Bit Cơ Bản ---

MASK = 0xFFFFFFFF  # Modulo 2^32

def ROTL(n, x):
    return ((x << n) | (x >> (32 - n))) & MASK

def F(t, B, C, D):
    if 0 <= t <= 19:
        return (B & C) ^ (~B & D) & MASK
    elif 20 <= t <= 39:
        return B ^ C ^ D
    elif 40 <= t <= 59:
        return (B & C) ^ (B & D) ^ (C & D)
    elif 60 <= t <= 79:
        return B ^ C ^ D

class PureSHA1:
    
    # 1. Hằng số Khởi tạo (Initial Hash Values - 32-bit)
    H = [
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0
    ]
    
    # Hằng số Vòng (Round Constants - 32-bit)
    K = [
        0x5A827999,  # 0 <= t <= 19
        0x6ED9EBA1,  # 20 <= t <= 39
        0x8F1BBCDC,  # 40 <= t <= 59
        0xCA62C1D6   # 60 <= t <= 79
    ]

    def __init__(self, data: bytes):
        self._message = data
        self._total_bits = len(data) * 8
        self._hash = list(self.H) # Khởi tạo giá trị băm
        self._process()

    # 2. Xử lý Đệm Thông điệp (Message Padding)
    def _pad(self) -> bytes:
        """Thực hiện đệm theo chuẩn SHA-1."""
        
        # Bước 1: Nối bit '1' (byte 0x80)
        padded_message = self._message + b'\x80'
        
        # Bước 2: Nối bit '0' đệm (đến 448 mod 512, hay 56 mod 64)
        L = len(padded_message)
        k_bytes = (56 - (L % 64)) % 64
        padded_message += b'\x00' * k_bytes
        
        # Bước 3: Nối Độ dài Gốc (64 bit Big-Endian)
        length_suffix = self._total_bits.to_bytes(8, byteorder='big')
        padded_message += length_suffix
        
        return padded_message

    # 3 & 4. Hàm Nén (Compression Function)
    def _process_block(self, block: bytes):
        """Xử lý một khối 512 bit (64 byte)."""
        
        # 3. Chuẩn bị Từ Thông điệp (Word Preparation)
        
        # Chia khối 64 byte thành 16 từ 32-bit (Big-Endian)
        W = list(struct.unpack('>16L', block)) # unpack '>16L' đọc 16 số nguyên 32-bit Big-Endian

        # Mở rộng thành 80 từ (W[16] - W[79])
        for t in range(16, 80):
            # W[t] = ROTL^1(W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16])
            temp = W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]
            W.append(ROTL(1, temp))
        
        # Khởi tạo các biến làm việc A, B, C, D, E
        A, B, C, D, E = self._hash
        
        # Vòng lặp 80 bước
        for t in range(80):
            K_t = self.K[t // 20]
            Temp = (ROTL(5, A) + F(t, B, C, D)) & MASK
            Temp = (Temp + E) & MASK
            Temp = (Temp + K_t) & MASK
            Temp = (Temp + W[t]) & MASK

            # Cập nhật các biến A, B, C, D, E
            E = D
            D = C
            C = ROTL(30, B)
            B = A
            A = Temp

        # Cập nhật giá trị băm: H_i = H_i + Working_Variable_i (MODULO 2^32)
        self._hash[0] = (self._hash[0] + A) & MASK
        self._hash[1] = (self._hash[1] + B) & MASK
        self._hash[2] = (self._hash[2] + C) & MASK
        self._hash[3] = (self._hash[3] + D) & MASK
        self._hash[4] = (self._hash[4] + E) & MASK

    def _process(self):
        """Thực hiện băm toàn bộ thông điệp."""
        padded_message = self._pad()
        
        block_size = 64 # 64 bytes = 512 bits
        for i in range(0, len(padded_message), block_size):
            block = padded_message[i:i + block_size]
            self._process_block(block)

    # 5. Kết quả Đầu ra (Final Hash)
    def hexdigest(self) -> str:
        """Trả về chuỗi băm 40 ký tự hexa."""
        # Nối 5 giá trị H_i để tạo ra kết quả băm 160 bit
        return ''.join(f'{h:08x}' for h in self._hash)


# --- Ví dụ Sử Dụng ---
key = "dpziczac"
s = "The quick brown fox jumps over the lazy dog"
temp = key + s; 

sha1_instance = PureSHA1(temp.encode('ascii'))
result_hash = sha1_instance.hexdigest()

print(f"SHA-1: {result_hash}")

# Kết quả mong đợi để kiểm tra (từ các thư viện chuẩn):
# 2fd4e1c67a2d28fced849ee1bb76e7391b93eb12

```



