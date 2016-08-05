/* -----------------------------------------------------------------Ĺ-----------
 *
 * Author:      Kjell Swedin
 * Description: Code using pugixml library to read fuelbed xml files and do
 *              sanity checks on the values. This is not well-formedness validation.
 * Date:        2/18/2016
 *
 ----------------------------------------------------------------------------- */

#include <string>
#include <vector>
#include <iostream>
#include <cassert>
#include <cstring>
#include <cmath>
#include <limits>
#include <cmath>
#include <regex>
#include <sstream>
#include <utility>
#include <algorithm>
#include "fuelbed_values.h"
#include "tsn.h"
#include "utils.h"

using std::cout;
using std::endl;
using std::string;
using std::list;
using std::tuple;
using std::pair;
using std::vector;
using std::ceil;
using std::make_pair;
using std::map;
using std::regex;
using std::regex_match;
using std::stringstream;
using std::pair;
using std::make_pair;
using std::sort;


// ----------------------------------------------------------------------------
//  Iterate through defined xpaths and gather values for later checking.
// ----------------------------------------------------------------------------
template <typename T>
void
SetNodeValue(pugi::xml_document& doc, T& container)
{
    for(auto& xpath : container)
    {
        pugi::xpath_node n = doc.select_node(xpath.second.Xpath().c_str());
        xpath.second.Value(n.node().child_value());
    }
}

bool
FuelbedValues::Read()
{
    auto xmlParseResult_ = doc_.load_file(filename_.c_str());

    if(xmlParseResult_)
    {
        SetNodeValue(doc_, fbValues_);
 
        for(auto& xpath : speciesValues_)
        {
            string desc = xpath.second.Xpath();
            desc.append("/relative_cover");
            string tsn = xpath.second.Xpath();
            tsn.append("/tsn");

            pugi::xpath_node_set descNodes = doc_.select_nodes(desc.c_str());
            pugi::xpath_node_set tsnNodes = doc_.select_nodes(tsn.c_str());

            if(descNodes.size() == tsnNodes.size())
            {
                // build up the list and add the whole thing so that writeCount behavior
                // is the same as single xml values.
                list<Species> tmp;
                for(size_t i = 0; i < descNodes.size(); i++)
                {
                    tmp.push_back(Species(tsnNodes[i].node().child_value(), descNodes[i].node().child_value()));
                }
                xpath.second.SpeciesList(tmp);
            }
            else
            {
                assert(false);
            }
        }
    }

    return xmlParseResult_;
}

// ----------------------------------------------------------------------------
//  Write - 2 variations. Write changes to the existing file. Write changes to
//   a new file of the supplied name. Prior to writing, save from intermediate
//   format into xml.
// ----------------------------------------------------------------------------
const int WRITE_THRESHOLD = 1;
template<typename T>
bool
Changed(const T& value)
{
    return value.second.WriteCount() > WRITE_THRESHOLD;
}

template<typename T>
void
FuelbedValues::SaveContainedValues(const T& values)
{
    for(auto& v : values )
    {
        if(Changed(v))
        {
            DbgPrint(v.second.Xpath() + " : " + v.second.Value());
            auto look = doc_.select_node(v.second.Xpath().c_str()).node();

            if(!look.first_child())
            {
                auto ret = look.append_child(pugi::node_pcdata);
                DbgPrint(string(ret ? "SUCCESS" : "FAILURE") + " adding pcdata for " + v.second.Xpath());
            }

            auto result = look.first_child().set_value(v.second.Value().c_str());
            DbgPrint(string((result ? "   SUCCEEDED" : "   FAILED") + v.second.Xpath()));
        }
    }
}

void
FuelbedValues::SaveSpeciesValues()
{
    for(auto& v : speciesValues_)
    {
        if(Changed(v))
        {
            pugi::xpath_node speciesNode = doc_.select_node(v.second.XpathSpecies().c_str());

            // remove existing species_description nodes
            while(speciesNode.node().remove_child("species_description")) {}

            // add the new species_description nodes
            for(auto s : v.second.SpeciesList())
            {
                pugi::xml_node newNode = speciesNode.node().append_child("species_description");
                newNode.append_child("tsn").append_child(pugi::node_pcdata).set_value(s.tsn.c_str());
                newNode.append_child("relative_cover").append_child(pugi::node_pcdata).set_value(s.relativeCover.c_str());
            }
        }
    }
}

void
FuelbedValues::SaveToXML()
{
    SaveContainedValues(fbValues_);
    SaveSpeciesValues();
}

bool
FuelbedValues::Write()
{
    SaveToXML();
    return doc_.save_file(filename_.c_str());
}

bool
FuelbedValues::Write(const std::string& filename)
{
    SaveToXML();
    return doc_.save_file(filename.c_str());
}

// ----------------------------------------------------------------------------
//  Set values - these methods set the values in the working data. Prior to
//      writing to a file, changes to the working data are written to the
//      xml stream and saved from there.
// ----------------------------------------------------------------------------
void
FuelbedValues::SetValue(FBTypes type, const string& value)
{
    if(value.length())
    {
        bool okToAssign = true;
        UnitTypes check = fbValues_.at(type).Type();
        if(UnitTypes::eNO_UNIT != check)
        {
            // any of these types contain a non-negative, numeric value
            static regex const number_regex{"^[0-9.]+$"};
            okToAssign = regex_match(value, number_regex);
        }
        if(okToAssign)
        {
            fbValues_[type].Value(value);
        }
        else
        {
            DbgPrint(string("Regex failed, not adding - ") + fbValues_[type].Xpath() + " Value = " + value);
            assert(false);
        }
    }
    else
    {
        DbgPrint(string("Warning: empty value, not adding - ") + fbValues_[type].Xpath());
    }
}

void
FuelbedValues::SetSpeciesValue(FBSpeciesTypes type, const list<Species>& value)
{
    float shouldBeOneHundred = 0;
    for(auto species : value)
    {
        if(!tsnChecker.count(stoi(species.tsn)))
        {
            assert(false);  // Error: bad TSN in SetSpeciesValue
        }
        shouldBeOneHundred += stof(species.relativeCover);
    }
    if(100.0 != shouldBeOneHundred)
    {
        assert(false); // Error: relative covers don't add to 100.0 in SetSpeciesValue
    }
    speciesValues_[type].SpeciesList(value);
}

// ----------------------------------------------------------------------------
//  Get values - these methods get values from the working data.
// ----------------------------------------------------------------------------
string
FuelbedValues::GetValue(FBTypes type) const
{
    return fbValues_.at(type).Value();
}

list<Species>
FuelbedValues::GetSpeciesValue(FBSpeciesTypes type)
{
    return speciesValues_[type].SpeciesList();
}



// ----------------------------------------------------------------------------
//  For verification/checking.
// ----------------------------------------------------------------------------
void
FuelbedValues::Print() const
{
    vector<pair<string, string> > items;
    for(auto xpath : fbValues_)
    {
        items.push_back(make_pair(FBTypesToString(xpath.first), xpath.second.Value()));
    }
    sort(items.begin(), items.end());
    for(auto item : items)
    {
        cout << item.first << "," << item.second << endl;
    }

    items.clear();
    for(auto speciesInfo : speciesValues_ )
    {
        stringstream s;
        s << "(";
        for(auto item : speciesInfo.second.SpeciesList())
        {
            s << '(' << item.tsn << ", " << item.relativeCover << ')';
        }
        s << ")";
        items.push_back(make_pair(FBSpeciesTypesToString(speciesInfo.first), s.str()));
    }
    sort(items.begin(), items.end());
    for(auto item : items)
    {
        cout << item.first << "," << item.second << endl;
    }
}





