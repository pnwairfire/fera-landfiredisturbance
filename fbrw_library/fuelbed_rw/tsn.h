//  !!! Generated file - DO NOT MODIFY !!!

#ifndef TSN_H
#define TSN_H
#include <map>
#include <string>

enum class StratumType {
    eCANOPY = 1,
    eNONWOODY = 2,
    eSHRUB = 4,
    eWOODY = 8,
};

struct TSNInfo {
    int stratumType;
    std::string commonName;
    std::string scientificName;

    TSNInfo(int type, char const* cName, char const* sName)
        : stratumType(type), commonName(cName), scientificName(sName) {}
};

extern std::map<int, TSNInfo> tsnChecker;

#endif
