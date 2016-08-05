/* ----------------------------------------------------------------------------
 *
 * Author:      Kjell Swedin
 * Description: Miscellaneous file utilities
 * Date:        5/3/2016
 *
 *----------------------------------------------------------------------------- */

#include "file_utils.h"
#include <iostream>

using std::string;
using std::vector;
using std::cout;
using std::endl;

bool
FileExists(const string& name)
{
    return FileExists(name.c_str());
}

bool
FileExists(const char* name)
{
    if(FILE *file = fopen(name, "r"))
    {
        fclose(file);
        return true;
    }
    return false;
}

bool
CheckIfAllExist(const vector<string>& files)
{
    vector<string> nonExistent;
    for(auto f : files)
    {
        if(!FileExists(f)) { nonExistent.push_back(f); }
    }

    if(0 == nonExistent.size()) { return true; }

    cout << "Error: the following files don't exist:" << endl;
    for(auto f : nonExistent)
    {
        cout << "\t" << f << endl;
    }
    return false;
}
