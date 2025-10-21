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