/* ----------------------------------------------------------------------------
 *
 * Author:      Kjell Swedin
 * Description: Miscellaneous utilities
 * Date:        5/4/2016
 *
 *----------------------------------------------------------------------------- */

#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <vector>
#include <algorithm>

// including boost caused problems for the cross compiler. Workaround.
std::string trim(std::string str);


template<class C, class T>
bool contains(const C& v, const T& x)
{
    return std::end(v) != std::find(std::begin(v), std::end(v), x);
}

template<typename T>
std::vector<T> 
split(const T & str, const T & delimiters)
{
    std::vector<T> v;
    typename T::size_type start = 0;
    auto pos = str.find_first_of(delimiters, start);
    while(pos != T::npos)
    {
        if(pos != start) // ignore empty tokens
            v.emplace_back(str, start, pos - start);
        start = pos + 1;
        pos = str.find_first_of(delimiters, start);
    }
    if(start < str.length()) // ignore trailing delimiter
        v.emplace_back(str, start, str.length() - start); // add what's left of the string
    return v;
}


#define DBG_PRINT 1
void
DbgPrint(const std::string& msg);

#endif  // UTILS_H
