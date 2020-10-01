from glob import glob
from validation_indices import Indices
import sys

def load_partition(fn):
    partition = []
    for line in open(fn):
        partition.append( int(line.rstrip()) )
    return partition

def compute_indices():
    # Obtain reference clusterings
    gts = dict()
    for fn in glob('parsed/*.gt'):
        name = fn[len('parsed/'):-len('.gt')]
        gts[name] = load_partition(fn)

    # We write to the file by changing sys.stdout so that all print statements are written to the file.
    original_stdout = sys.stdout
    with open("all_datasets_methods_metrics.tsv","w") as f:
        sys.stdout = f
        for fn in glob("candidates/*.cl_*"):
            dataset,method = fn[len('candidates/'):].split(".cl_")
            candidate = load_partition(fn)
            for i in Indices:
                print("\t".join(map(str,[
                    dataset,
                    "gt_vs_"+method, i.__name__,
                    (-1 if i.isdistance else 1) * i.score(gts[dataset],candidate)])))
        sys.stdout = original_stdout