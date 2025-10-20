# interencdec
Ở bài này thì ban đầu khi đọc file sẽ cho ta một dòng code base64 `YidkM0JxZGtwQlRYdHFhR3g2YUhsZmF6TnFlVGwzWVROclh6ZzJhMnd6TW1zeWZRPT0nCg==` nên ta sẽ sử dụng cyberchef để decode nó ra và ta lại thu được tiếp một đoạn base64 trong ngoặc `d3BqdkpBTXtqaGx6aHlfazNqeTl3YTNrXzg2a2wzMmsyfQ==` thì ở đây ta vẫn sẽ tiếp tục decode thì được một dòng có dạng ROT13 `wpjvJAM{jhlzhy_k3jy9wa3k_86kl32k2}` nhưng ta không biết nó dịch bao nhiêu phần tử vì thế ta sẽ bruteforce ROT13 để tìm flag thì ta phát hiện nó đã dịch 19 phần tử và thu được flag.
![image](https://hackmd.io/_uploads/BkegADmRee.png)
![image](https://hackmd.io/_uploads/rkw-AD7Axg.png)
![image](https://hackmd.io/_uploads/BkvykumAee.png)
