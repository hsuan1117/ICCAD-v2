import os
import subprocess
from random import randint
from uuid import uuid4
from os import system

# clear up
system(f'cp data-backup/* data')
system(f'rm compress decompress *.bin compressed.bin decompressed.bin')

# build compress
system('make compress')
system('make decompress')
print('編譯成功')

# gen binary
print("==== 自主產生測資 ====")
data = bytearray([randint(0, 255) for _ in range(0, 1024)])
fn = str(uuid4())
with open(f'{fn}.bin', 'wb') as f:
    f.write(data)
f.close()

system(f'rm compressed.bin decompressed.bin')
# compress
system(f'./compress {fn}.bin')

# decompress
system(f'./decompress compressed.bin')

# compare
print('\n自主測資')
print(f'壓縮率: {(os.stat("compressed.bin").st_size / os.stat(f"{fn}.bin").st_size) * 100}%')
system(f'md5 {fn}.bin decompressed.bin')
if subprocess.check_output(['md5', '-q', f"{fn}.bin"]) == subprocess.check_output(
        ['md5', '-q', 'decompressed.bin']):
    print('✅ 解壓縮成功')
else:
    print('❌ 解壓縮失敗')
print()
print()

# traverse `data` directory
for file in os.listdir('data'):
    if not os.path.isdir(file):
        print(f'\n{file}')
        system(f'rm compressed.bin decompressed.bin')
        system(f'./compress data/{file}')
        system(f'./decompress compressed.bin')
        file_stats_compressed = os.stat("compressed.bin")
        file_stats_decompressed = os.stat(f"data/{file}")
        print(f'壓縮率: {(file_stats_compressed.st_size / file_stats_decompressed.st_size) * 100}%')
        system(f'md5 data/{file} decompressed.bin')
        if subprocess.check_output(['md5', '-q', 'data/' + file]) == subprocess.check_output(
                ['md5', '-q', 'decompressed.bin']):
            print('✅ 解壓縮成功')
        else:
            print('❌ 解壓縮失敗')
        print()

# clear up
system(f'rm {fn}.bin compressed.bin decompressed.bin')
