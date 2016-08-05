/* ----------------------------------------------------------------------------
 *
 * Author:      Kjell Swedin
 * Description: Miscellaneous file utilities
 * Date:        5/3/2016
 *
 *----------------------------------------------------------------------------- */

#ifndef FILE_UTILS_H
#define FILE_UTILS_H

#include <string>
#include <vector>

bool
FileExists(const std::string& name);

bool
FileExists(const char* name);

bool
CheckIfAllExist(const std::vector<std::string>& files);


#endif // FILE_UTILS_H
