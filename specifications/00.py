import os

dirs = [
    '1_Fire',
    '2_MechAdd',
    '3_MechRemove',
    '4_Wind',
    '5_Insects',
]

for dir in dirs:
    cd = os.getcwd()
    os.chdir(dir)
    file = '{}_Script.csv'.format(dir)
    with open(file, 'r') as infile:
        print('{},,,,,,,,,,'.format(file))
        for line in infile:
            if not ',,,,,,,,,' in line:
                print(line.strip())
        print()
    
    os.chdir(cd)