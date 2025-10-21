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