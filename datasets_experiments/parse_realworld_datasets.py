from urllib.request import urlopen
from io import StringIO
from scipy.io import arff
import numpy as np
import os

# Selected datasets
datasets = [
    'arrhythmia',
    'balance-scale',
    'ecoli',
    'heart-statlog',
    'letter',
    'segment',
    'vehicle',
    'wdbc',
    'wine',
    'wisc',
    'cpu',
    'iono',
    'iris',
    'sonar',
    'thy',
    'zoo'
]

def parse_datasets(datasets=datasets):
    # The datasets are taken from this folder:
    # https://github.com/deric/clustering-benchmark/tree/master/src/main/resources/datasets/real-world
    ds2url = {
        ds: 'https://raw.githubusercontent.com/deric/clustering-benchmark/master/src/main/resources/datasets/real-world/{}.arff'.format(ds)
        for ds in datasets
    }

    for dataset,url in ds2url.items():
        print('Parsing',dataset)
        # Read the arff data
        data,meta = arff.loadarff(StringIO(urlopen(url).read().decode('utf-8')))
        # Find the ground truth column
        class_column = list(map(lambda x: x.lower(), meta._attributes)).index('class')
        # Parse the data
        data = np.array(data)
        ys = []
        xs = []
        for item in data:
            ys.append(str(item[class_column]))
            xs.append([x for i, x in enumerate(item) if i != class_column])
        classes = list(sorted(set(ys)))
        print("Found {} classes".format(len(classes)))
        ys = [classes.index(x) for x in ys]

        parsed_dir = os.path.join(os.path.dirname(__file__), 'parsed/')
        # Write to files
        with open(parsed_dir+dataset+'.features', 'w') as file:
            for item in xs:
                print("\t".join(map(str, item)), file=file)
        with open(parsed_dir+dataset+'.gt', 'w') as file:
            for item in ys:
                print(item, file=file)