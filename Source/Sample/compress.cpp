#include "../ZipLib/ZipFile.h"
#include "../ZipLib/streams/memstream.h"
#include "../ZipLib/methods/Bzip2Method.h"

#include <bits/stdc++.h>

using namespace std;

int main(int argc, char *argv[]) {
    srand(time(NULL));

    if (argc <= 1) {
        std::cout << "Usage: " << argv[0] << " filename" << std::endl;
        return 0;
    }

    string filename = argv[1];
    string zipFilename = "compressed.bin";

    printf("[+] Compressing '%s' to compress.bin\n", filename.c_str());

    ifstream contentStream(filename, ios::binary | ios::in);
    ZipArchive::Ptr archive = ZipFile::Open(zipFilename);

    ZipArchiveEntry::Ptr entry = archive->CreateEntry("file.bin");

    for (int i = 0; i < rand() % (1000 - 10 + 1) + 10; i++) {
        stringstream ss;
        ss << i;
        archive->CreateEntry(ss.str())->SetPassword("0000");
    }


    entry->SetPassword("0000");
    entry->SetCompressionStream(contentStream, DeflateMethod::Create());

    ZipFile::SaveAndClose(archive, zipFilename);

    fstream zipped(zipFilename, ios::binary | ios::in | ios::out);
    fstream origin(filename, ios::binary | ios::in | ios::out);

    zipped.seekg(0, std::ifstream::end);
    size_t zipped_size = zipped.tellg();

    origin.seekg(0, std::ifstream::end);
    size_t origin_size = origin.tellg();

    cout << "[+] Compressed file size: " << zipped_size << endl;
    cout << "[+] Original file size: " << origin_size << endl;

    if (zipped_size > origin_size) {
        cout << "[!] Compressed file is larger than original file" << endl;
        stringstream ss;
        ss << "cp " << filename << " compressed.bin";
        system(ss.str().c_str());
    }
//    zipped.close();
//    origin.close();
    return 0;
}
