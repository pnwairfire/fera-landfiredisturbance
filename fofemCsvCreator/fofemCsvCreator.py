import xml.etree.ElementTree as ET
import csv
import xmltodict
import os


# copy input file from this repository:
# https://github.com/pnwairfire/fera-apps-consume/blob/master/consume/input_data/fccs_loadings.csv

# unzip fuelbeds.zip to same location as this script.
# note: fuelbeds.zip contains the standard fuelbeds 0-1299 and Landfire disturbance variations
# the zip file was created from /Users/briandrye/Documents/FCCSwebPython3Java/python-consume-fera/fccs/fuelbeds
# (these are the fuelbeds in WFEIS)

fccs_loadings = "fccs_loadings.csv"   # input file
output_file_name = "FOF_FCCS.csv"

lines = list(csv.DictReader(list(open(fccs_loadings))[1:]))

outputfile = open(output_file_name, 'w')

outputfile.write("Reg,Reg,Reg,Reg,Fuelbed_number,Fuelbed_Name,Litter,Duff,Depth,Shrub,Herb,1Hr,10Hr,100Hr,3-9S,9-20S,20+S,3-9R,9-20R,20+R,Foli,Bran,CTG,Flame EF,Duff EF,Smolder 1K EF\n")

i = 0
for line in lines:
#    if i == 3:         # for testing: if you only want a few lines of output.
#        break
    filename = line["filename"]

    print(filename)
    if filename == '':
        break

    with open('fuelbeds/' + filename) as fd:
        doc = xmltodict.parse(fd.read())

    outputfile.write("P,I,N,S,")
    outputfile.write(doc['FCCS_file']['fuelbed_number'] + ',')

    # fuelbed_name is not in csv file
    # lookup up fuelbed_name from filename
    # truncate fb name to 60 characters
    fb_name = doc['FCCS_file']['fuelbed_name']
    fb_name = (fb_name[:60]) if len(fb_name) > 60 else fb_name
    outputfile.write(fb_name + ',')

    outputfile.write(line["litter_loading"] + ',')
    # if < .1 or > 356...
    duff_loading = float(line["duff_upper_loading"])
    if duff_loading > 0 and duff_loading <= .1:
        duff_loading = .1
    if duff_loading > 356:
        duff_loading = 356
    outputfile.write(str(duff_loading) + ',')

    outputfile.write(line["duff_upper_depth"] + ',')

    shrub = float(line["shrubs_primary_loading"]) + float(line["shrubs_secondary_loading"])
    outputfile.write(str(shrub) + ',')

    herb = float(line["nw_primary_loading"]) + float(line["nw_secondary_loading"])
    outputfile.write(str(herb) + ',')

    outputfile.write(line["w_sound_0_quarter_loading"] + ',')   # 1Hr
    outputfile.write(line["w_sound_quarter_1_loading"] + ',')   # 10Hr
    outputfile.write(line["w_sound_1_3_loading"] + ',')         # 100Hr
    outputfile.write(line["w_sound_3_9_loading"] + ',')         # 3-9S
    outputfile.write(line["w_sound_9_20_loading"] + ',')        # 9-20S
    outputfile.write(line["w_sound_gt20_loading"] + ',')        # 20+S
    outputfile.write(line["w_rotten_3_9_loading"] + ',')        # 3-9R
    outputfile.write(line["w_rotten_9_20_loading"] + ',')       # 9-20R
    outputfile.write(line["w_rotten_gt20_loading"] + ',')       # 20+R

    loading = float(line["overstory_loading"]) + float(line["midstory_loading"]) + float(line["understory_loading"]) + \
              float(line["snags_c1_foliage_loading"])

    #print(loading)

    outputfile.write(str(loading * 0.8) + ',')   # Foli
    outputfile.write(str(loading * 0.2) + ',')   # Bran
    outputfile.write("User Supplied,User Supplied,User Supplied,User Supplied")
    outputfile.write("\n")
    i = i + 1

print(output_file_name + " created.")