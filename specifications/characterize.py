from collections import defaultdict

cell_dict = defaultdict(list)
weird = defaultdict(list)
with open('spec_all.csv', 'r') as infile:
    for line in infile:
        chunks = line.strip().split(',')
        for chunk in chunks:
            chunk = chunk.strip()
            if ' ' in line:
                key = chunk.split(' ')[0]
                if not ' ' == key:
                    cell_dict[key].append(chunk)
            else:
                if not chunk.startswith('e'):
                    weird[chunk] = chunk
    print('\nWeird')
    for key in weird.keys():
        print('\t{} : {}'.format(key, weird[key]))
    print('\nCells')
    for key in cell_dict.keys():
        print('::: {} : {}\n'.format(key, cell_dict[key]))