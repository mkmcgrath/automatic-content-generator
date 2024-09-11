import os

for x in range(0, 5000):
    os.system(f"echo IMG{x} >> imgtextfile.txt")
    print(f"IMG{x} added to file")
