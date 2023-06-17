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

status = []

system(f'rm compressed.bin decompressed.bin')
# compress
system(f'./compress {fn}.bin')

# decompress
system(f'./decompress compressed.bin')

# compare
print('\n自主測資')
ok = False
print(f'壓縮率: {(os.stat("compressed.bin").st_size / os.stat(f"{fn}.bin").st_size) * 100}%')
system(f'md5 {fn}.bin decompressed.bin')
if subprocess.check_output(['md5', '-q', f"{fn}.bin"]) == subprocess.check_output(
        ['md5', '-q', 'decompressed.bin']):
    ok = True
    print('✅ 解壓縮成功')
else:
    print('❌ 解壓縮失敗')
print()
status.append(('自主測資', ok, (os.stat("compressed.bin").st_size / os.stat(f"{fn}.bin").st_size) * 100))

# traverse `data` directory
for file in os.listdir('data'):
    if not os.path.isdir(file):
        ok = False
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
            ok = True
            print('✅ 解壓縮成功')
        else:
            print('❌ 解壓縮失敗')
        print()
        status.append((file, ok, (file_stats_compressed.st_size / file_stats_decompressed.st_size) * 100))

# clear up
system(f'rm {fn}.bin compressed.bin decompressed.bin')

print('==== 測資結果 ====')
for i, s in enumerate(status):
    print(f'測資 [{s[0]}]: {"成功" if s[1] else "失敗"}，壓縮率: {s[2]}%')
