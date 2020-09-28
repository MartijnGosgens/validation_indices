from glob import glob
import json
from collections import defaultdict
from validation_indices import Indices

def load_partition(fn):
    partition = []
    for line in open(fn):
        partition.append( int(line.rstrip()) )
    return partition

#def pt2vector(pt):
#	return partition

gts = dict()
for fn in glob('datasets_parsed/*.gt'):
	handle = fn.split('\\')[-1].replace(".gt","")
	gts[handle] = load_partition(fn)

for fn in glob("datasets_clusterized/*.cl_*"):
	dataset,method = fn.split('\\')[-1].split(".cl_")
	pt = load_partition(fn)
	for i in Indices:
		print("\t".join(map(str,[dataset, "gt_vs_"+method, i.__name__, i.score(gts[dataset],pt)])))

