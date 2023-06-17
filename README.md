# Compress and Decompress
Both using STDIN to read data and STDOUT to write data.
You'll need to redirect the input and output.

## Build

```shell
$HOME/opt/gcc-10.1.0/bin/g++ -o combine -O3 -Ofast -march=native -std=c++17 -I$HOME/opt/gcc-10.1.0/include -L$HOME/opt/gcc-10.1.0/lib64 -static-libstdc++ -s -static -fvisibility=hidden -fvisibility-inlines-hidden compress.cpp
$HOME/opt/gcc-10.1.0/bin/g++ -o combine -O3 -Ofast -march=native -std=c++17 -I$HOME/opt/gcc-10.1.0/include -L$HOME/opt/gcc-10.1.0/lib64 -static-libstdc++ -s -static -fvisibility=hidden -fvisibility-inlines-hidden decompress.cpp
```

## Compress

```shell
./compress < INPUT.bin > COMPRESSED.bin
```

## Decompress

```shell
./decompress < COMPRESSED.bin > ORIGIN.bin
```

## Validate

```shell
md5 INPUT.bin 
md5 ORIGIN.bin
```