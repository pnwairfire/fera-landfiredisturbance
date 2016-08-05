/* ----------------------------------------------------------------------------
 *
 * Author:      Kjell Swedin
 * Description: Miscellaneous utilities
 * Date:        5/4/2016
 *
 *----------------------------------------------------------------------------- */

#include "utils.h"
#include <algorithm>
#include <iostream>
#include <cctype>

using std::string;
using std::cout;

// including boost caused problems for the cross compiler. Workaround.
string
trim(string str)
{
    str.erase(str.begin(), find_if(str.begin(), str.end(),
        [](char& ch)->bool { return !isspace(ch); }));
    str.erase(find_if(str.rbegin(), str.rend(),
        [](char& ch)->bool { return !isspace(ch); }).base(), str.end());
    return str;
}


#if DBG_PRINT
void
DbgPrint(const string& msg)
{
    cout << msg << "\n";
}
#else
void
DbgPrint(const string& msg) {;}
#endif

