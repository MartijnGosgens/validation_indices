from glob import glob
import json
from collections import defaultdict
from validation_indices import Indices
import sys

def load_partition(fn):
    partition = []
    for line in open(fn):
        partition.append( int(line.rstrip()) )
    return partition

# Obtain reference clusterings
gts = dict()
for fn in glob('datasets_parsed/*.gt'):
	handle = fn.split('\\')[-1].replace(".gt","")
	gts[handle] = load_partition(fn)

# We write to the file by changing sys.stdout so that all print statements are written to the file.
original_stdout = sys.stdout
with open("all_datasets_methods_metrics.tsv","w") as f:
	sys.stdout = f
	for fn in glob("datasets_clusterized/*.cl_*"):
		dataset,method = fn.split('\\')[-1].split(".cl_")
		pt = load_partition(fn)
		for i in Indices:
			print("\t".join(map(str,[dataset, "gt_vs_"+method, i.__name__, i.score(gts[dataset],pt)])))
	sys.stdout = original_stdout
