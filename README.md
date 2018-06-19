# Landfire Disturbance

## Purpose/Description: Specifications and scripts to modify fuelbeds to reflect a disturbance to the corresponding landscape.

High level description:

1. Start with a set of fuelbeds

2. Create a set of disturbance rules (csv files)

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

3. The run_landfire directory contains scripts to wrap the disturbance scripts and

    * produce the "disturbed" fuelbeds
    
    * run FCCS on the generated fuelbeds

    * create the 3 deliverable files (consume_loadings.csv, fofem-like input file, subset of FCCS summary file)


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

The run_regression directory contains a small set of fuelbeds in the regression_fuelbeds directory. The regress.py script runs the disturbance scripts on these fuelbeds. It gathers values from the generated fuelbeds and compares them to the independently calculated values from the 3 ../specifications/<disturance>.csv files.

Running the reg.sh script gives summary output. It looks like this:

```
fire
4968 Comparisons
	4968 Successful
	0 Unsuccessful
mechadd
4968 Comparisons
	4968 Successful
	0 Unsuccessful
mechremove
4968 Comparisons
	4968 Successful
	0 Unsuccessful
wind
4968 Comparisons
	4968 Successful
	0 Unsuccessful
insects
3312 Comparisons
	3312 Successful
	0 Unsuccessful

```

### Docker Notes

1. connect to VPN (home.airfire.org) via Cisco AnyConnect
2. clone repository to local machine (landfiredisturbance/*)
3. create Dockerfile in landfiredisturbance directory.

```
Dockerfile content:
FROM ubuntu

ADD . /

RUN apt-get update && apt-get install -y \
wget \
python3 \
python3-pip 

RUN pip3 install pandas
RUN pip3 install requests

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

```

4. from landfiredisturbance directory on local machine:
docker build -t landfireImage .
(creates the Docker image called landfireImage)
docker run -it landfireImage
(creates a Docker container based on the landfireImage)

5. at ubuntu prompt:
cd run_regression
./reg.sh
(runs regression tests)
or
cd run_landfire 
python3 main.py
(runs landfire)


### Problems/Quirks

### Links
name (link)