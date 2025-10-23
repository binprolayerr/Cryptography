---
title: README.md

---

# Convert hex to base64

## Yêu cầu
Bài này cho ta một chuỗi hex
```49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d```

và yêu cầu ta chuyển thành base64 thành (kết quả là chuỗi sau)
```SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t```

## Hướng giải
Ta sẽ dùng hàm `bytes.fromhex(string)` để đọc lấy byte thô từ chuỗi hex

Sau đó sử dụng hàm chuyển bytes thành base64 `base64.b64decode()`. Để sử dụng hàm này cần thêm thư viện `base64`
