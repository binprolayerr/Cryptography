---
title: README

---

# 3. Single-byte XOR cipher

## Yêu cầu

Cho một chuỗi `1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736` đã được xor với một kí tự duy nhất.

Viết chương trình tìm khóa (key_xor) đó và giải mã thông điệp

## Hướng giải

Đầu tiên ta chuyển hex thành byte
```hex_num = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")```

Với key_xor chỉ có một kí tự, ta sẽ nghĩ đến việc dò từng kí tự một và xem thử kí tự nào sẽ cho ra thông điệp, có tất cả 256 kí tự như vậy.

Đồng thời trong lúc dò từng kí tự, ta sẽ có một hàm để đánh giá mức độ giống câu tiếng anh. Một câu tiếng anh sẽ hầu như không có các kí tự đặc biệt (@, #, $%, ...) mà thường có các chữ cái `a-z`, `A-Z`, kí tự dấu cách `' '` (ascii 32).

Hàm này sẽ đánh giá trên toàn bộ bản rõ, với kí tự nào được xor qua chuỗi cho bản rõ có độ giống tiếng anh nhất thì sẽ có thể coi là thông điệp, kí tự đó có coi là key_xor. Tất nhiên để chắc chắn, có thể kiểm tra qua một vài bản rõ có mức độ giống tiếng anh cao nhất để không bị bỏ sót.

Trước hết, ta sẽ có một mảng để lưu các kí tự trong câu văn tiếng anh
```python
ascii_text = list(range(97, 123)) + list(range(65, 91)) + [32]
```

Hàm sẽ nhận vào một chuỗi và tính xác suất bằng cách duyệt qua từng kí tự trong chuỗi và
+ Nếu kí tự `c` trong chuỗi thuộc `ascii_text` thì cộng dồn lên 1 vào một biến đếm
+ Thương số biến đếm với độ dài chuỗi sẽ là giá trị xác suất
$\rightarrow$ Rõ ràng giá trị xác suất này không vượt quá 1
Hàm này còn có thêm một thông số `rate` để đánh giá độ giống tiếng anh chấp nhận được. Cụ thể, nếu có key_xor nào cho giá trị xác suất tính ra ở trên lớn hơn `rate` thì ta sẽ coi như đó là một câu tiếng anh, đồng nghĩa với giá trị trả về của hàm là 1, còn nếu không lớn hơn `rate` thì hàm trả về giá trị 0

```python
def text_probability(string, rate):
    probability = sum([x in ascii_text for x in string]) / len(string)
    if probability > rate: return 1
    else: return 0
```

Ta sẽ chọn `rate=0.8` (có thể chọn nhỏ hơn rồi tăng dần lên), đồng thời khai báo mảng để lưu giá trị
```python
rate = 0.8
result = []
```

Ta tiến hành duyệt qua tất cả các kí tự có thể, với mỗi `key`, tạo chuỗi `string_temp` để lưu chuỗi kết quả XOR của `hex_num` với `key`

Nếu giá trị `text_probabilitty(string_temp) == 1`, ta sẽ thêm chuỗi `string_temp` và `key` đó vào mảng `result`.
```python
for key in range(256):
    string_temp = bytes([c ^ key for c in hex_num])
    if text_probability(string_temp, rate) == 1:
        result.append((string_temp.decode(errors='ignore'), key))
```

Lúc này ta có thể in mảng `result` ra để kiểm tra, có thể tăng `rate` lên nếu có nhiều bản rõ chứa kí tự không thuộc `ascii_text`.

Ta in ra thông điệp, cùng với kí tự `key`
```python
for i in range(len(result)):
    print(result[:None][0], "\nmessage:", result[i][0], "\nmy_single_xor_key:", chr(result[i][1]))
```

## Kết quả chạy chương trình
```terminal
("Cooking MC's like a pound of bacon", 88) 
message: Cooking MC's like a pound of bacon
my_single_xor_key: X
```

Chương trình cho ra kết quả với `rate = 0.8`