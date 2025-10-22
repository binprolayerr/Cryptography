---
title: README

---

### 6. Break repeating-key XOR

#### Yêu cầu

Bài này yêu cầu ta bẻ khóa repeating-key xor
Một đoạn mã đã được mã hóa bằng repeating-key xor đang nằm trong file `6.txt` (ở dạng base64). Ta cần tìm ra `key` để giải mã thông điệp. Làm được điều đó đồng nghĩa với việc ta có thể bẻ khóa repeating-key xor

#### Các bước giải

Ta thực hiện theo hướng dẫn của bài, bao gồm ba phần là tìm độ dài khóa, tìm khóa, và giải mã

- Tìm độ dài khóa: hàm `Hdistance()`, hàm `guess_keysize()`
- Tìm khóa: hàm `score_text_string()`, `c03_single_xor_cipher`, hàm `break_block()`
- Giải mã: `c05_implement_repeatingkey_xor`

**Tìm độ dài khóa**

*Hàm Hamming distance - Hdistance()*

Hàm này tính độ sai khác giữa hai byte cùng độ dài, nói cách khác giá trị hàm chính là số giá trị khác nhau (theo bit) của hai byte cùng độ dài

Hàm nhận vào hai byte `b1`, `b2`, tạo biến đếm `distance=0`
để cộng dồn. Với mỗi cặp $(x, y)$ là cặp bit ở vị trí tương ứng của 2 byte `b1`, `b2`, nếu `x` khác `y` thì kết quả xor giữa chúng cho ra kết quả 1, ta cộng dồn kết quả này vào `distance`. Cuối cùng, hàm trả về giá trị `distance`
```python
def Hdistance(b1, b2):
    assert len(b1) == len(b2)
    distance = 0
    for x, y in zip(b1, b2):
        distance += bin(x ^ y).count("1")
    return distance
```
Ta có thể kiểm tra hàm hoạt động đúng với
```python
string_1 = b"this is a test"
string_2 = b"wokka wokka!!!"
print(Hdistance(string_1, string_2))
```

*Hàm dự đoán độ dài khóa - guess_keysize()*

Bài toán giới hạn độ dài chỉ dao động trong khoảng 2 đến 40 kí tự, do đó ta sẽ duyệt qua tất cả các keysize trong khoảng đó.

Tạo mảng `result_keysize = []` để lưu kết quả

Hàm sẽ nhận vào `ciphertext` (từ `6.txt`). Với mỗi giá trị `keysize` từ 2 đế 40, ta chia ciphertext thành các đoạn với mỗi đoạn có độ dài `2 * keysize`. Trong mỗi đoạn như vậy ta sẽ chia đôi thành 2 đoạn nhỏ hơn có độ dài `keysize` và tiến hành tính giá trị `Hdistance()` giữa 2 đoạn này. Thực hiện tương tự cho các đoạn độ dài `2 * keysize` còn lại, kết quả được cộng dồn vào biến `score`.

Ta lấy giá trị trung bình bằng cách chia `score` cho số lần tính `Hdistance()` (chính bằng số đoạn độ dài `2 * keysize`). Vì `keysize` qua mỗi lần duyệt có độ dài khác nhau nên ta chuẩn hóa bằng cách lấy kết quá trung bình chia cho `keysize`.

Sau khi duyệt qua mỗi `keysize`, thêm vào `result_keysize = []` cặp giá trị `(keysize, score)` (score lúc này đã được chuẩn hóa). Sắp xếp (không giảm) mảng `result_keysize = []` sau khi đã thêm vào đủ các trường hợp của `keysize`.

Hàm trả về kết quả `keysize` nằm trong cặp phần tử `(keysize, score)` mà có giá trị `score` nhỏ nhất (là phần tử đầu tiên trong mảng sau sắp xếp)
```python
min_keysize = 2
max_keysize = 40

def guess_keysize(ciphertext):
    result_keysize = []
    for keysize in range(min_keysize, max_keysize + 1):
        temp = len(ciphertext) // (2 * keysize) - 1
        score = 0
        for i in range(temp):
            str1 = ciphertext[2*i*keysize:(2*i+1)*keysize]
            str2 = ciphertext[(2*i+1)*keysize:2*(i+1)*keysize]
            score += Hdistance(str1, str2)
        score /= (keysize * temp)
        result_keysize.append((keysize, score))
    new_result = sorted(result_keysize, key = lambda x: x[1])
    return new_result[0][0]
```

**Tìm khóa**

Sau khi đoán được `keysize`, theo cách hoạt động của repeating-key xor, ta chia ciphertext thành các block có độ dài `keysize`, lưu các block này vào một mảng
```python
KEYSIZE = guess_keysize(ciphertext)

break_ciphertext = [ciphertext[i:i+KEYSIZE] for i in range(0, len(ciphertext), KEYSIZE)]
```

Có thể nói `break_ciphertext` lúc này như một ma trận với các hàng là các block độ dài `KEYSIZE`

`break_ciphertext = [block[0], block[1], ..., block[k]]`
`block[i] = "abc...xyz"` # độ dài `KEYSIZE`
Vậy thì với mỗi $j$, cố định $j$, $\forall i_1\neq i_2: block[i_1][j]$ và $block[i_2][j]$ sẽ được xor với cùng kí tự $key[j]$ khi thực hiện repeating-key xor. Nói cách khác các mỗi phần tử nằm trên cột $i$ của ma trận `break_ciphertext` sẽ được xor với cùng kí tự $key[i]$. Lúc này nếu coi mỗi cột như một chuỗi kí tự, thì bài toán quy về giải mã xor với key có đúng 1 kí tự.

Để hiện thực ý tưởng này, ta có thể chuyển vị ma trận `break_ciphertext` để đưa các cột về hàng để dễ thao tác. Ma trận sau chuyển vị là `transposed_array`
```python
from itertools import zip_longest
transposed_array = list(zip_longest(*break_ciphertext, fillvalue=0))
```
Lúc này ta giải lại bài toán giải mã xor với key là 1 kí tự (c03_single_xor_cipher)

*Hàm đánh giá mức độ giống tiếng anh - score_text_string()*

```python
ascii_text = list(range(97, 123)) + list(range(65, 91)) + [32]
rate = 0.9

def score_text_string(string):
    score_text = sum([x in ascii_text for x in string]) / len(string)
    return score_text
```

*Hàm giải mã từng block - break_block()*

Với mỗi block, ta sẽ duyệt từ kí tự `key` từ 0 đến 255.
+ Với mỗi `key`, ta tạo `string_temp` là kết quả xor của `key` với 1 hàng của `transposed_array`.
+ Thêm cặp giá trị `((key, score_text_string(string_temp)))` vào mảng lưu trữ `result = []`
+ Trả về mảng result = [] đã được sắp xếp (không tăng) theo giá trị `score_text_string()`
```python
def break_block(block):
    result = []
    for key in range(256):
        string_temp = bytes([c ^ key for c in block])
        result.append((key, score_text_string(string_temp)))
    return sorted(result, key=lambda x: x[1], reverse=True)
```

Cuối cùng, thực hiện hàm `break_block()` cho tất cả các hàng của `transposed_array`, và lưu theo thứ tự các single-key-xor vào một mảng `my_xor_key = []`
```python
my_xor_key = [break_block(transposed_array[number])[0][0] for number in range(KEYSIZE)]
```
**Giải mã**

Như vậy đã hoàn thành việc tìm ra `key` để giải mã, tiến hành giải mã `ciphertext` tương tự như `c05_implement_repeatingkey_xor`

```python
print(bytes([ciphertext[num] ^ my_xor_key[num%len(my_xor_key)] for num in range(len(ciphertext))]).decode())
```