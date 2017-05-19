import os

dirs = [
    '1_Fire',
    '5_Insects'
]

for dir in dirs:
    cd = os.getcwd()
    os.chdir(dir)
    file = '{}_Script.csv'.format(dir)
    with open(file, 'r') as infile:
        print('{},,,,,,,,,,'.format(file))
        for line in infile:
            if 'eCANOPY' in line:
                print(line.strip())
        print()
    
    os.chdir(cd)