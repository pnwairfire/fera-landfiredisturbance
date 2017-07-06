# Landfire Disturbance

## Purpose/Description: Specifications and scripts to modify fuelbeds to reflect a disturbance to the corresponding landscape.

High level description:

1. Start with a set of fuelbeds

2. Create a set of disturbance rules (csv file)

3. Encode the disturbance rules into python scripts using a combination of manual and scripted steps

4. Run the disturbance scripts on the set of fuelbeds to create a new (larger) set of "disturbed" fuelbeds.

Landfire-specific description:

1. Original fuelbeds are in run_landfire/fuelbeds (same set of fuelbeds that ship with FFT)

2. The disturbance rules are encoded in python scripts in the run_disturbance/scripts directory. There are currently 5 disturbances (the scripts directory contains a like-named script for each disturbance):

    * fire

    * mechanical add

    * mechanical remove

    * wind

    * insects

3. The run_landfire directory contains scripts to wrap the disturbance scripts and produce the "disturbed" fuelbeds


### Top level Landfire directory structure and components
```
landfire/
   ├── README.md
   ├── run_disturbance
   ├── run_landfire
   ├── run_regression
   └── specifications
```
### Next level directory structure
```
├── run_disturbance
│   └── scripts
├── run_landfire
│   ├── build_fofem_inputs.py
│   ├── consume_loadings.csv
│   ├── fccs_summary.csv
│   ├── FFT_FUELBEDS.zip
│   ├── fofem_input.csv
│   ├── fuelbed.jar
│   ├── fuelbeds
│   ├── LandfireAnalysis.ipynb
│   ├── lf_analyze.py
│   ├── lf_by_fuelbed_analyze.py
│   ├── main.py
│   └── out
├── run_regression
│   ├── calculated_values.csv
│   ├── expected.csv
│   ├── out
│   ├── print_values_from_xml.py
│   ├── regression_fuelbeds
│   ├── regress.py
│   └── reg.sh
└── specifications
    ├── 00.py
    ├── 1_Fire
    ├── 2_MechAdd
    ├── 3_MechRemove
    ├── 4_Wind
    ├── 5_Insects
    ├── characterize.py
    ├── DisturbanceCodes.xlsx
    ├── Documents
    ├── fire_expected.csv
    ├── generate_from_spec.py
    ├── insects_expected.csv
    ├── mechadd_expected.csv
    ├── mechremove_expected.csv
    ├── ScriptRules_Fire.xlsx
    ├── ScriptRules_I&D.xlsx
    ├── strip_commas.py
    └── wind_expected.csv

```




### Tests

### Problems/Quirks

### Links
name (link)