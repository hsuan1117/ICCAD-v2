# Final names of binaries
EXECUTABLE = Bin/zipsample
COMPRESS_EXEC = compress
DECOMPRESS_EXEC = decompress
SO_LIBRARY = Bin/libzip.so

# C & C++ compiler

# if linux
ifeq ($(shell uname -s),Linux)
CC       = /project/cad/cad18/cad18/cade0019/cade0019_alpha/opt/gcc-10.1.0/bin/gcc
CXX      = /project/cad/cad18/cad18/cade0019/cade0019_alpha/opt/gcc-10.1.0/bin/g++
CFLAGS    = -fPIC -Wno-enum-conversion -O3 -I/project/cad/cad18/cad18/cade0019/cade0019_alpha/opt/gcc-10.1.0/include -L/project/cad/cad18/cad18/cade0019/cade0019_alpha/opt/gcc-10.1.0/lib64
CXXFLAGS  = -fPIC -std=c++11 -O3 -march=native -I/project/cad/cad18/cad18/cade0019/cade0019_alpha/opt/gcc-10.1.0/include -L/project/cad/cad18/cad18/cade0019/cade0019_alpha/opt/gcc-10.1.0/lib64 -static-libstdc++ -s -static -fvisibility=hidden -fvisibility-inlines-hidden
else
CC        = clang
CXX       = g++-13
CFLAGS    = -fPIC -Wno-enum-conversion -O3
CXXFLAGS  = -fPIC -std=c++11 -O3 -g
endif

# Linker flags
LDFLAGS   = -pthread

# Sources of external libraries
SRC_ZLIB  = $(wildcard Source/ZipLib/extlibs/zlib/*.c)
SRC_LZMA  = $(wildcard Source/ZipLib/extlibs/lzma/unix/*.c)
SRC_BZIP2 = $(wildcard Source/ZipLib/extlibs/bzip2/*.c)

# ZipLib sources
SRC = \
		$(wildcard Source/ZipLib/*.cpp)        \
		$(wildcard Source/ZipLib/detail/*.cpp)

# Object files			
OBJS = \
		$(SRC:.cpp=.o)	   \
		$(SRC_ZLIB:.c=.o)  \
		$(SRC_LZMA:.c=.o)  \
		$(SRC_BZIP2:.c=.o)

# Rules
compress: $(COMPRESS_EXEC) $(SO_LIBRARY)
$(COMPRESS_EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) Source/Sample/compress.cpp -o $@ $^

decompress: $(DECOMPRESS_EXEC) $(SO_LIBRARY)
$(DECOMPRESS_EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) Source/Sample/decompress.cpp -o $@ $^

$(SO_LIBRARY): $(OBJS)
	$(CXX) $(LDFLAGS) -shared -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf `find Source -name '*.o'` ziplib.tar.gz Bin/*.zip Bin/out* $(EXECUTABLE) $(SO_LIBRARY)

tarball:
	tar -zcvf ziplib.tar.gz *
	