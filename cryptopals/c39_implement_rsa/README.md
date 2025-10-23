# Implement RSA

Thuật toán RSA là hệ thống mật mã hóa khóa công khai phổ biến nhất, dựa trên độ khó của bài toán phân tích thừa số nguyên tố.

---

## I. Đặc Điểm Cốt Lõi

RSA sử dụng **hai khóa** khác nhau:

1.  **Khóa Công khai (Public Key):** Dùng để **Mã hóa** (Encrypt). Được chia sẻ công khai.
2.  **Khóa Bí mật (Private Key):** Dùng để **Giải mã** (Decrypt). Phải được giữ bí mật tuyệt đối.

---

## II. Các Giai Đoạn Chính

### 1. Sinh Khóa (Key Generation)

Quá trình tạo ra cặp khóa $(\mathbf{e}, \mathbf{N})$ và $(\mathbf{d}, \mathbf{N})$:

1.  **Chọn Số nguyên tố:** Chọn hai số nguyên tố lớn, khác nhau ($p$ và $q$). (Bí mật)
2.  **Tính Mô-đun $N$:** $N = p \times q$. (Công khai)
3.  **Tính Hàm Euler Totient $\phi(N)$:** $\phi(N) = (p - 1) \times (q - 1)$. (Bí mật)
4.  **Chọn Số mũ Mã hóa $e$:** Chọn $e$ sao cho $1 < e < \phi(N)$ và $\text{ƯCLN}(e, \phi(N)) = 1$. (Công khai)
5.  **Tính Số mũ Giải mã $d$:** Tính $d$ là nghịch đảo modulo của $e$ theo modulo $\phi(N)$.

    $$d \times e \equiv 1 \pmod{\phi(N)}$$

**Khóa Công khai:** $(\mathbf{e}, \mathbf{N})$
**Khóa Bí mật:** $(\mathbf{d}, \mathbf{N})$

---

### 2. Mã hóa (Encryption)

Người gửi (Bob) sử dụng **Khóa Công khai** $(e, N)$ của người nhận (Alice) để mã hóa thông điệp $M$:

$$C = M^e \pmod{N}$$

---

### 3. Giải mã (Decryption)

Người nhận (Alice) sử dụng **Khóa Bí mật** $(d, N)$ của mình để giải mã bản mã $C$:

$$M = C^d \pmod{N}$$

---

**Nguyên tắc Bảo mật:** Mọi người đều biết $N$ và $e$. Để giải mã $C$, cần biết $d$. Để tìm $d$, cần biết $\phi(N)$. Để tìm $\phi(N)$, cần biết $p$ và $q$. Vì $p$ và $q$ là các số nguyên tố cực lớn, việc phân tích thừa số $N$ để tìm chúng là bất khả thi về mặt tính toán.

## Code
```python
import math

# --- 1. Hàm Hỗ trợ: Thuật toán Euclid mở rộng (Extended Euclidean Algorithm) ---
# Dùng để tính toán Nghịch đảo Modulo (d)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def invmod(a, m):
    """Tính nghịch đảo modulo: a^-1 mod m"""
    g, x, y = egcd(a, m)
    if g != 1:
        # Nghịch đảo không tồn tại nếu a và m không nguyên tố cùng nhau
        # Trả về None hoặc raise Exception
        return None 
    else:
        return x % m

# --- 2. HÀM TẠO KHÓA RSA (Key Generation) ---
def generate_rsa_keys(p, q, e=65537): # e=65537 là giá trị thực tế phổ biến
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Chọn e (chúng ta sẽ dùng e cố định, nhưng cần kiểm tra GCD)
    while math.gcd(e, phi_n) != 1:
        e += 2 # Hoặc chọn e mới

    # Tính d
    d = invmod(e, phi_n)
    
    # Khóa d phải là số dương
    if d is None:
        raise ValueError("d không tồn tại. Chọn p, q, e khác.")
    
    public_key = (e, n)
    private_key = (d, n)
    
    return public_key, private_key

# --- 3. HÀM MÃ HÓA (Encryption) ---
def rsa_encrypt(public_key, m):
    e, n = public_key
    # c = m^e mod n. Python's pow(base, exp, mod) rất hiệu quả
    c = pow(m, e, n)
    return c

# --- 4. HÀM GIẢI MÃ (Decryption) ---
def rsa_decrypt(private_key, c):
    d, n = private_key
    # m = c^d mod n
    m = pow(c, d, n)
    return m

# --- THỬ NGHIỆM VỚI VÍ DỤ CƠ BẢN ---
# Chọn số nguyên tố nhỏ (theo tinh thần của thử thách)
P = 17
Q = 13
E_VALUE = 5  # Chọn E=5 để đảm bảo nguyên tố cùng nhau với phi_n = 192

# 1. Sinh khóa
PUBLIC_KEY, PRIVATE_KEY = generate_rsa_keys(P, Q, E_VALUE)
D_VALUE = PRIVATE_KEY[0]
N_VALUE = PUBLIC_KEY[1]

print(f"P={P}, Q={Q}")
print(f"N (Mô-đun): {N_VALUE}")
print(f"Phi(N): {(P-1)*(Q-1)}")
print(f"Public Key (e, n): {PUBLIC_KEY}")
print(f"Private Key (d, n): {PRIVATE_KEY}")
print("-" * 30)

# 2. Mã hóa thông điệp (số 42)
MESSAGE = 42
CIPHERTEXT = rsa_encrypt(PUBLIC_KEY, MESSAGE)
print(f"Bản rõ (m): {MESSAGE}")
print(f"Bản mã (c): {CIPHERTEXT}")
print("-" * 30)

# 3. Giải mã
DECRYPTED_MESSAGE = rsa_decrypt(PRIVATE_KEY, CIPHERTEXT)
print(f"Giải mã (m): {DECRYPTED_MESSAGE}")

if DECRYPTED_MESSAGE == MESSAGE:
    print("RSA hoạt động chính xác!")
else:
    print("Lỗi RSA.")
```
