data = open("8.txt", "r").read()

for s in data.split(): 
    myset = set()
    for i in range(0, len(s), 32):
        block = s[i : i + 32]
        myset.add(block)
        
    total_blocks = len(s) // 32
    unique_blocks = len(myset)
    
    if total_blocks > unique_blocks:
        print(s)
