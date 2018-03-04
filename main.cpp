//
//  main.cpp
//  Interview_prep
//
//  Created by Tzachi Lapidot on 27/02/2018.
//  Copyright © 2018 Tzachi Lapidot. All rights reserved.
//

#include <iostream>
#include <map>
#include <vector>
#include "Estab.hpp"
#include <dirent.h>
#include <fstream>
#include <sstream>
#include <codecvt>
#include <locale>
#include <cstdlib>

void WriteUnicodetoFile(const char* myFile,  std::wstring& ws){
    std::ofstream outFile(myFile, std::ios::out | std::ios::binary);
    outFile.write((char *) ws.c_str(), ws.length() * sizeof(wchar_t));
    outFile.close();
    
}

std::wstring readUnicodeFile(const char* filename)
{
    std::ifstream wif(filename);
    std::stringstream wss;
    wss << wif.rdbuf();
    std::string  const &str = wss.str();
    std::wstring wstr;
    wstr.resize(str.size()/sizeof(wchar_t));
    std::cout<<sizeof(wstr)<<std::endl;
    std::memcpy(&wstr[0],str.c_str(),str.size()); // copy data into wstring
    std::wcout<<wstr<<std::endl;
    std::cout<<str.size()<<std::endl;
    WriteUnicodetoFile("/Users/tzachilapidot/Desktop/chiko.txt", wstr);
    return wstr;
}

void readFile(std::string filename)
{
    std::wifstream wif(filename);
    wif.imbue(std::locale("zh_CN.UTF-8"));
    
    std::wcout.imbue(std::locale("zh_CN.UTF-8"));
    std::wcout << wif.rdbuf();
}

int write_to_file (std::string path) {
    
    std::fstream fs;
    fs.open (path, std::fstream::in | std::fstream::out | std::fstream::app);
    
    fs << " more lorem ipsum";
    
    fs.close();
    
    return 0;
}

void fill_file_list(std::string path, std::vector<std::string> &files)
{
    DIR           *dirp;
    struct dirent *directory;
    
    dirp = opendir(path.c_str());
    if (dirp)
    {
        while ((directory = readdir(dirp)) != NULL)
        {
            files.push_back(std::string(directory->d_name));
        }
        
        closedir(dirp);
    }
}

int main(int argc, const char * argv[]) {
    //std::vector<std::string> files;
    //std::map<std::string,Estab> estabMap;
    std::cout<<"kawabanga\n"<<std::endl;
    readFile("/Users/tzachilapidot/Desktop/hezi.txt");
    return 0;
}
