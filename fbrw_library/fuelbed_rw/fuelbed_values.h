/* ----------------------------------------------------------------------------
 *
 * Author:      Kjell Swedin
 * Description: Code using pugixml library to read fuelbed xml files and do
 *              sanity checks on the values. This is not well-formedness validation.
 * Date:        2/18/2016
 *
 ----------------------------------------------------------------------------- */
 
#ifndef FUELBED_VALUES_H
#define FUELBED_VALUES_H

#include <map>
#include <list>
#include <string>
#include <tuple>
#include <utility>
#include "pugixml.hpp"
#include "fuelbed_ids.h"
#include "utils.h"

// the unit type associated with the quantity variable
enum class UnitTypes
{
    eFEET,
    eINCHES,
    eNUMBER,
    eNUMBER_PER_ACRE,
    eTONS_PER_ACRE,
	eNO_UNIT
};

//
enum class STATUS_ANY_ALL
{
    eALL,
    eNONE,
    eERROR
};

// ----------------------------------------------------------------------------
//  Adds the variable type to the single value.
// -----------------------------------------------------------------------------
class XMLValue
{
    UnitTypes type_;
    std::string xpath_;
    std::string value_;
    int writeCount_;

public:
    XMLValue() : type_(UnitTypes::eNO_UNIT), writeCount_(0) {}

    XMLValue(std::string xpath, UnitTypes type)
        : type_(type), xpath_(xpath), writeCount_(0) {}
        
    std::string Xpath() const
    {
        return xpath_;
    }

    void Value(std::string value)
    {
        value_ = value;
        writeCount_++;
    }

    std::string Value() const
    {
        return value_;
    }
	
	UnitTypes Type() const
	{
		return type_;
	}
    
    void Reset()
    {
        value_ = "";
        writeCount_ = 0;
    }

    int WriteCount() const { return writeCount_; }
};

struct Species
{
    std::string tsn;
    std::string relativeCover;

    Species(std::string tsn, std::string rcover)
        : tsn(tsn), relativeCover(rcover) {}
};

// ----------------------------------------------------------------------------
//  Single xpath denotes a collection of elements.
// -----------------------------------------------------------------------------
class SpeciesValue
{
    std::string xpathBase_;
    std::list<Species> perSpeciesValues_;
    int writeCount_;

public:
    SpeciesValue() : writeCount_(0) {}
    SpeciesValue(std::string xpath)
        : xpathBase_(xpath), writeCount_(0) {}

    std::string Xpath() const { return xpathBase_; }

    // lop off the "species_description" portion of the path (last element)
    std::string XpathSpecies() const
    {
        return xpathBase_.substr(0, xpathBase_.find_last_of("/"));
    }

    std::list<Species> SpeciesList() const
    {
        return perSpeciesValues_;
    }

    void SpeciesList(std::list<Species> species)
    {
        perSpeciesValues_ = species;
        writeCount_++;
    }
    
    void Reset()
    {
        perSpeciesValues_.clear();
        writeCount_ = 0;
    }

    int WriteCount() const { return writeCount_; }
};

// ----------------------------------------------------------------------------
//  Class that encapsulates fuelbed values, how they relate, and the checks
//   to perform.
// ----------------------------------------------------------------------------
class FuelbedValues
{
    std::string filename_;
    pugi::xml_document doc_;

public:
    // Preferred public interface - not great for unit testing
    FuelbedValues(const std::string& filename) 
        : filename_(filename) {};
        
    ~FuelbedValues()
    {
        doc_.reset();
        for(auto i : fbValues_)
        {
            i.second.Reset();
        }
        for(auto i : speciesValues_)
        {
            i.second.Reset();
        }
    };
    bool Read();
    bool Write();
    bool Write(const std::string& filename);
    void Print() const;

    const pugi::xml_document& GetXMLDoc() const { return doc_; }

    // setting
    void SetValue(FBTypes type, const std::string& value);
    void SetSpeciesValue(FBSpeciesTypes type, const std::list<Species>& value);

    // getting
    std::string GetValue(FBTypes type) const;
    std::list<Species> GetSpeciesValue(FBSpeciesTypes type);

private:
    void SaveToXML();
    template<typename T> void SaveContainedValues(const T& values);
    void SaveSpeciesValues();


    std::map<FBTypes, XMLValue> fbValues_ = {
        { FBTypes::eFUELBED_NUMBER,
            XMLValue("/FCCS_file/fuelbed_number", UnitTypes::eNO_UNIT) },
        { FBTypes::eFUELBED_NAME,
            XMLValue("/FCCS_file/fuelbed_name", UnitTypes::eNO_UNIT) },
        { FBTypes::eFUELBED_DESCRIPTION,
            XMLValue("/FCCS_file/fuelbed_description", UnitTypes::eNO_UNIT) },
        { FBTypes::eECOREGION,
            XMLValue("/FCCS_file/ecoregion", UnitTypes::eNO_UNIT) },
        { FBTypes::eVEGETATION_FORM,
            XMLValue("/FCCS_file/vegetation_form", UnitTypes::eNO_UNIT) },
        { FBTypes::eSTRUCTURAL_CLASS,
            XMLValue("/FCCS_file/structural_class", UnitTypes::eNO_UNIT) },
        { FBTypes::eCOVER_TYPE,
            XMLValue("/FCCS_file/cover_type", UnitTypes::eNO_UNIT) },
        { FBTypes::eCHANGE_AGENT,
            XMLValue("/FCCS_file/change_agent", UnitTypes::eNO_UNIT) },
        { FBTypes::eNATURAL_FIRE_REGIME,
            XMLValue("/FCCS_file/natural_fire_regime", UnitTypes::eNO_UNIT) },
        { FBTypes::eCONDITION_CLASS,
            XMLValue("/FCCS_file/condition_class", UnitTypes::eNO_UNIT) },
        { FBTypes::eUSER_NAME,
            XMLValue("/FCCS_file/user_name", UnitTypes::eNO_UNIT) },
        { FBTypes::eADDRESS,
            XMLValue("/FCCS_file/address", UnitTypes::eNO_UNIT) },
        { FBTypes::eAFFILIATION,
            XMLValue("/FCCS_file/affiliation", UnitTypes::eNO_UNIT) },
        { FBTypes::ePHONE,
            XMLValue("/FCCS_file/phone", UnitTypes::eNO_UNIT) },
        { FBTypes::eFILE_OWNER_EMAIL,
            XMLValue("/FCCS_file/file_owner_email", UnitTypes::eNO_UNIT) },
        { FBTypes::eNOTES,
            XMLValue("/FCCS_file/notes", UnitTypes::eNO_UNIT) },
        { FBTypes::eDATE_COLLECTED,
            XMLValue("/FCCS_file/date_collected", UnitTypes::eNO_UNIT) },
        { FBTypes::eFUELBED_CONFIDENCE,
            XMLValue("/FCCS_file/fuelbed_confidence", UnitTypes::eNO_UNIT) },
        { FBTypes::eCANOPY_LADDER_FUELS_MAXIMUM_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/ladder_fuels/maximum_height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_LADDER_FUELS_MINIMUM_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/ladder_fuels/minimum_height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_all_others/diameter",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_all_others/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_all_others/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_conifers_with_foliage/diameter",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_conifers_with_foliage/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT_TO_CROWN_BASE,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_conifers_with_foliage/height_to_crown_base",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_conifers_with_foliage/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_1_conifers_with_foliage/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eCANOPY_SNAGS_CLASS_2_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_2/diameter",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_SNAGS_CLASS_2_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_2/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_SNAGS_CLASS_2_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_2/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eCANOPY_SNAGS_CLASS_3_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_3/diameter",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_SNAGS_CLASS_3_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_3/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_SNAGS_CLASS_3_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/snags/class_3/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/midstory/diameter_at_breast_height",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_TREES_MIDSTORY_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/midstory/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/midstory/height_to_live_crown",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_TREES_MIDSTORY_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/midstory/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eCANOPY_TREES_MIDSTORY_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/midstory/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/overstory/diameter_at_breast_height",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_TREES_OVERSTORY_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/overstory/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/overstory/height_to_live_crown",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_TREES_OVERSTORY_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/overstory/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eCANOPY_TREES_OVERSTORY_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/overstory/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eCANOPY_TREES_TOTAL_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/total_percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eCANOPY_TREES_UNDERSTORY_DIAMETER_AT_BREAST_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/understory/diameter_at_breast_height",UnitTypes::eINCHES) },
        { FBTypes::eCANOPY_TREES_UNDERSTORY_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/understory/height",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/understory/height_to_live_crown",UnitTypes::eFEET) },
        { FBTypes::eCANOPY_TREES_UNDERSTORY_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/understory/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eCANOPY_TREES_UNDERSTORY_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/canopy/trees/understory/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eGROUND_FUEL_BASAL_ACCUMULATION_DEPTH,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/basal_accumulation/depth",UnitTypes::eINCHES) },
        { FBTypes::eGROUND_FUEL_BASAL_ACCUMULATION_NUMBER_PER_UNIT_AREA,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/basal_accumulation/number_per_unit_area",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eGROUND_FUEL_BASAL_ACCUMULATION_RADIUS,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/basal_accumulation/radius",UnitTypes::eFEET) },
        { FBTypes::eGROUND_FUEL_DUFF_LOWER_DEPTH,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/duff/lower/depth",UnitTypes::eINCHES) },
        { FBTypes::eGROUND_FUEL_DUFF_LOWER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/duff/lower/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eGROUND_FUEL_DUFF_UPPER_DEPTH,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/duff/upper/depth",UnitTypes::eINCHES) },
        { FBTypes::eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/duff/upper/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eGROUND_FUEL_SQUIRREL_MIDDENS_DEPTH,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/squirrel_middens/depth",UnitTypes::eINCHES) },
        { FBTypes::eGROUND_FUEL_SQUIRREL_MIDDENS_NUMBER_PER_UNIT_AREA,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/squirrel_middens/number_per_unit_area",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eGROUND_FUEL_SQUIRREL_MIDDENS_RADIUS,
            XMLValue("/FCCS_file/fuelbed/ground_fuel/squirrel_middens/radius",UnitTypes::eFEET) },
        { FBTypes::eHERBACEOUS_PRIMARY_LAYER_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/herbaceous/primary_layer/height",UnitTypes::eFEET) },
        { FBTypes::eHERBACEOUS_PRIMARY_LAYER_LOADING,
            XMLValue("/FCCS_file/fuelbed/herbaceous/primary_layer/loading",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/herbaceous/primary_layer/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,
            XMLValue("/FCCS_file/fuelbed/herbaceous/primary_layer/percent_live",UnitTypes::eNUMBER) },
        { FBTypes::eHERBACEOUS_SECONDARY_LAYER_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/herbaceous/secondary_layer/height",UnitTypes::eFEET) },
        { FBTypes::eHERBACEOUS_SECONDARY_LAYER_LOADING,
            XMLValue("/FCCS_file/fuelbed/herbaceous/secondary_layer/loading",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/herbaceous/secondary_layer/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,
            XMLValue("/FCCS_file/fuelbed/herbaceous/secondary_layer/percent_live",UnitTypes::eNUMBER) },
        { FBTypes::eMOSS_LICHEN_LITTER_GROUND_LICHEN_DEPTH,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/ground_lichen/depth",UnitTypes::eINCHES) },
        { FBTypes::eMOSS_LICHEN_LITTER_GROUND_LICHEN_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/ground_lichen/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eMOSS_LICHEN_LITTER_LITTER_DEPTH,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/depth",UnitTypes::eINCHES) },
        { FBTypes::eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eMOSS_LICHEN_LITTER_MOSS_DEPTH,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/moss/depth",UnitTypes::eINCHES) },
        { FBTypes::eMOSS_LICHEN_LITTER_MOSS_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/moss/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eSHRUBS_PRIMARY_LAYER_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/shrubs/primary_layer/height",UnitTypes::eFEET) },
        { FBTypes::eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/shrubs/primary_layer/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,
            XMLValue("/FCCS_file/fuelbed/shrubs/primary_layer/percent_live",UnitTypes::eNUMBER) },
        { FBTypes::eSHRUBS_SECONDARY_LAYER_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/shrubs/secondary_layer/height",UnitTypes::eFEET) },
        { FBTypes::eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/shrubs/secondary_layer/percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,
            XMLValue("/FCCS_file/fuelbed/shrubs/secondary_layer/percent_live",UnitTypes::eNUMBER) },
        { FBTypes::eSHRUBS_NEEDLE_DRAPE_AFFECTS_FIRE_BEHAVIOR,
            XMLValue("/FCCS_file/fuelbed/shrubs/needle_drape/is_sufficient_to_affect_fire_behavior",UnitTypes::eNO_UNIT) },
        { FBTypes::eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/all_downed_woody_fuel/depth",UnitTypes::eINCHES) },
        { FBTypes::eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/all_downed_woody_fuel/total_percent_cover",UnitTypes::eNUMBER) },
        { FBTypes::eWOODY_FUEL_PILES_CLEAN_LOADING,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/piles/clean_loading",UnitTypes::eNUMBER) },
        { FBTypes::eWOODY_FUEL_PILES_DIRTY_LOADING,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/piles/dirty_loading",UnitTypes::eNUMBER) },
        { FBTypes::eWOODY_FUEL_PILES_VERYDIRTY_LOADING,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/piles/verydirty_loading",UnitTypes::eNUMBER) },
        { FBTypes::eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/rotten_wood/loadings_greater_than_three_inches/greater_than_twenty_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/rotten_wood/loadings_greater_than_three_inches/nine_to_twenty_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/rotten_wood/loadings_greater_than_three_inches/three_to_nine_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/loadings_greater_than_three_inches/greater_than_twenty_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/loadings_greater_than_three_inches/nine_to_twenty_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/loadings_greater_than_three_inches/three_to_nine_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/loadings_zero_to_three_inches/one_to_three_inches",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/loadings_zero_to_three_inches/quarter_inch_to_one_inch",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/loadings_zero_to_three_inches/zero_to_quarter_inch",UnitTypes::eTONS_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/lightered_pitchy/diameter",UnitTypes::eINCHES) },
        { FBTypes::eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/lightered_pitchy/height",UnitTypes::eFEET) },
        { FBTypes::eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/lightered_pitchy/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_STUMPS_ROTTEN_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/rotten/diameter",UnitTypes::eINCHES) },
        { FBTypes::eWOODY_FUEL_STUMPS_ROTTEN_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/rotten/height",UnitTypes::eFEET) },
        { FBTypes::eWOODY_FUEL_STUMPS_ROTTEN_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/rotten/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eWOODY_FUEL_STUMPS_SOUND_DIAMETER,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/sound/diameter",UnitTypes::eINCHES) },
        { FBTypes::eWOODY_FUEL_STUMPS_SOUND_HEIGHT,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/sound/height",UnitTypes::eFEET) },
        { FBTypes::eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY,
            XMLValue("/FCCS_file/fuelbed/woody_fuel/stumps/sound/stem_density",UnitTypes::eNUMBER_PER_ACRE) },
        { FBTypes::eLITTER_ARRANGEMENT,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/arrangement", UnitTypes::eNO_UNIT) },
        { FBTypes::eLITTER_LITTER_TYPE_SHORT_NEEDLE_PINE_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/short_needle_pine/relative_cover",UnitTypes::eNUMBER) },
        { FBTypes::eLITTER_LITTER_TYPE_LONG_NEEDLE_PINE_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/long_needle_pine/relative_cover",UnitTypes::eNUMBER) },
        { FBTypes::eLITTER_LITTER_TYPE_OTHER_CONIFER_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/other_conifer/relative_cover",UnitTypes::eNUMBER) },
        { FBTypes::eLITTER_LITTER_TYPE_BROADLEAF_DECIDUOUS_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/broadleaf_deciduous/relative_cover",UnitTypes::eNUMBER) },
        { FBTypes::eLITTER_LITTER_TYPE_BROADLEAF_EVERGREEN_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/broadleaf_evergreen/relative_cover",UnitTypes::eNUMBER) },
        { FBTypes::eLITTER_LITTER_TYPE_PALM_FROND_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/palm_frond/relative_cover",UnitTypes::eNUMBER) },
        { FBTypes::eLITTER_LITTER_TYPE_GRASS_RELATIVE_COVER,
            XMLValue("/FCCS_file/fuelbed/moss_lichen_litter/litter/litter_type/grass/relative_cover",UnitTypes::eNUMBER) },
    };

    std::map<FBSpeciesTypes, SpeciesValue> speciesValues_ = {
        { FBSpeciesTypes::eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/snags/class_1_all_others/species/species_description") },
        { FBSpeciesTypes::eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/snags/class_1_conifers_with_foliage/species/species_description") },
        { FBSpeciesTypes::eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/snags/class_2/species/species_description") },
        { FBSpeciesTypes::eCANOPY_SNAGS_CLASS_3_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/snags/class_3/species/species_description") },
        { FBSpeciesTypes::eCANOPY_TREES_MIDSTORY_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/trees/midstory/species/species_description") },
        { FBSpeciesTypes::eCANOPY_TREES_OVERSTORY_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/trees/overstory/species/species_description") },
        { FBSpeciesTypes::eCANOPY_TREES_UNDERSTORY_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/canopy/trees/understory/species/species_description") },
        { FBSpeciesTypes::eHERBACEOUS_PRIMARY_LAYER_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/herbaceous/primary_layer/species/species_description") },
        { FBSpeciesTypes::eHERBACEOUS_SECONDARY_LAYER_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/herbaceous/secondary_layer/species/species_description") },
        { FBSpeciesTypes::eSHRUBS_PRIMARY_LAYER_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/shrubs/primary_layer/species/species_description") },
        { FBSpeciesTypes::eSHRUBS_SECONDARY_LAYER_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/shrubs/secondary_layer/species/species_description") },
        { FBSpeciesTypes::eWOODY_FUEL_ROTTEN_WOOD_ALL_ROTTEN_WOOD_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/woody_fuel/rotten_wood/all_rotten_wood/species/species_description") },
        { FBSpeciesTypes::eWOODY_FUEL_SOUND_WOOD_ALL_SOUND_WOOD_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/woody_fuel/sound_wood/all_sound_wood/species/species_description") },
        { FBSpeciesTypes::eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/woody_fuel/stumps/lightered_pitchy/species/species_description") },
        { FBSpeciesTypes::eWOODY_FUEL_STUMPS_ROTTEN_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/woody_fuel/stumps/rotten/species/species_description") },
        { FBSpeciesTypes::eWOODY_FUEL_STUMPS_SOUND_SPECIES_SPECIES_DESCRIPTION,
            SpeciesValue("/FCCS_file/fuelbed/woody_fuel/stumps/sound/species/species_description") },
    };
};


#endif  // FUELBED_VALUES_H
