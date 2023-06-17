#include "../ZipLib/ZipFile.h"
#include "../ZipLib/streams/memstream.h"
#include "../ZipLib/methods/Bzip2Method.h"

#include <bits/stdc++.h>

using namespace std;

int main(int argc, char *argv[]) {
    if (argc <= 1) {
        std::cout << "Usage: " << argv[0] << " filename" << std::endl;
        return 0;
    }

    string filename = argv[1];
    cout << "[+] Decompressing 'compressed.bin' to 'decompressed.bin'" << endl;
    try {
        ZipArchive::Ptr archive = ZipFile::Open(filename);
        ZipArchiveEntry::Ptr entry = archive->GetEntry("file.bin");
        if (!entry) {
            throw std::exception();
        }

        entry->SetPassword("0000");
        std::istream *decompressStream = entry->GetDecompressionStream();
        ofstream out("decompressed.bin");
        auto buf = decompressStream->rdbuf();
        out << buf;

        out.seekp(0, std::ifstream::end);
        size_t origin_size = out.tellp();
        cout << "[+] Decompressed file size: " << origin_size << endl;
    } catch (const std::exception &e) {
        cout << "[!] Not a zip file, copying file to 'decompressed.bin'" << endl;
        stringstream ss;
        ss << "cp " << filename << " decompressed.bin";
        system(ss.str().c_str());
    }

    return 0;
}
