from validation_indices import Indices
import itertools as it
from collections import defaultdict
from numpy import sign

# Names of all indices
indices = [
    I.__name__
    for I in Indices
]

idx2latex = {
    'AvgNMI': 'NMI',
    'MaxNMI': r'NMI$_\text{max}$',
    'VariationOfInformation': 'VI',
    'FairNMI': 'FNMI',
    'AdjustedMutualInformation': 'AMI',
    'RandIndex': 'R',
    'AdjustedRandIndex': 'AR',
    'JaccardIndex': 'J',
    'WallaceIndex': 'W',
    'SokalAndSneath1': r'S\&S1',
    'PearsonCoefficient': 'CC',
    'FMeasure': 'FMeas',
    'BCubed': 'BCub'
}

idx2latex_mini = {
    'AvgNMI': r'\textbf{NMI}',
    'VariationOfInformation': r'\textbf{VI}',
    'AdjustedRandIndex': r'\textbf{AR}',
    'SokalAndSneath1': r'S\&S1',
    'PearsonCoefficient': r'\textbf{CC}',
}

# e.g. exclude_condition=lambda line: line.startswith('artificial')
def read_file(exclude_condition=None):
    # A triple mapping from datasets to comparisons to indices to the index-value on this comparison.
    ds2comp2idx2score = defaultdict(lambda: defaultdict(dict))

    # Collect scores
    for line in open('all_datasets_methods_metrics.tsv'):
        if exclude_condition is not None and exclude_condition(line): continue
        ds, comp, idx, val = line.strip().split("\t")

        # Invert for distances
        val = float(val)
        # Add index value
        ds2comp2idx2score[ds][comp][idx] = val
    return ds2comp2idx2score

def count_agreements(exclude_condition=None):
    ds2comp2idx2score = read_file(exclude_condition=exclude_condition)

    # Mapping from dataset to the total number of candidate pairs (i.e. clustering triplets)
    ds2total_triplets = {
        ds: len(comps) * (len(comps) - 1) / 2
        for ds, comps in ds2comp2idx2score.items()
    }
    # Double mapping from datasets to index-pairs to the number of triplets they agree on
    ds2idxs2agreements = {
        ds: {
            (idx1, idx2): len([
                1  # Count the number of candidate pairs that these indices agree on
                for idx2comp1, idx2comp2 in it.combinations(comp2idx2score.values(), 2)
                if sign(idx2comp1[idx1] - idx2comp2[idx1]) == sign(idx2comp1[idx2] - idx2comp2[idx2])
            ])
            for idx1, idx2 in it.combinations(indices, 2)
        }
        for ds, comp2idx2score in ds2comp2idx2score.items()
    }
    return (ds2idxs2agreements,ds2total_triplets)


def totals(ds2idxs2agreements,ds2total_triplets):
    # Add 'total' dataset containing all the counts
    totals = sum(ds2total_triplets.values())
    idxs2agreements = {
        idxs: sum([
            idxs2agreements[idxs]
            for idxs2agreements in ds2idxs2agreements.values()
        ])
        for idxs in it.combinations(indices, 2)
    }
    return (idxs2agreements,totals)

def get_kmeans():
    exclude_condition = lambda line: line.startswith('artificial') or ('kmeans_2' not in line and 'kmeans_gt_double' not in line)
    ds2comp2blah = read_file(exclude_condition=exclude_condition)
    return {
        ds: comp2blah
        for ds, comp2blah in ds2comp2blah.items()
        if len(comp2blah)==2 and 'glass' not in ds
    }

def get_kmeans_preference():
    kmeans_data = get_kmeans()

    k2idx2count = defaultdict(lambda : defaultdict(int))
    for ds, comp2idx2score in kmeans_data.items():
        for idx in indices:
            k2idx2count[max(comp2idx2score,key=lambda comp: comp2idx2score[comp][idx])][idx] += 1
    return k2idx2count

def print_kmeans_preferences(idx2latex=idx2latex):
    import sys
    stdout_orig = sys.stdout
    sys.stdout = open("preferences.txt","w")
    print("&".join(['']+list(idx2latex.values()))+r'\\')
    for k,idx2count in get_kmeans_preference().items():
        print("&".join([k]+[str(idx2count[idx]) for idx in idx2latex.keys()])+r'\\')
    sys.stdout = stdout_orig

def print_table(idxs2agreements,total_triplets,show_agreements=False,output_file=None):
    val = lambda agreements: str(round((
            agreements if show_agreements else total_triplets - agreements
        ) * 100 / total_triplets, 1))
    # redirect stdout if output_file is specified
    stdold = None
    if output_file is not None:
        import sys
        stdold = sys.stdout
        sys.stdout = open(output_file,"w")
    print("\t".join(['']+indices))
    for idx_row in indices:
        print("\t".join([idx_row]+[
            val(idxs2agreements[(idx_row,idx_col)]) if (idx_row,idx_col) in idxs2agreements else ''
            for idx_col in indices
        ]))
    # Reset stdout if necessary
    if output_file is not None:
        sys.stdout = stdold

def print_latex_table(idxs2agreements,total_triplets,show_agreements=False,output_file=None,idx2latex=idx2latex):
    print('Writing table for',total_triplets,'triplets to',output_file)
    val = lambda agreements: '$'+str(round((
           agreements if show_agreements else total_triplets - agreements
       ) * 100 / total_triplets, 1))+'$'
    # redirect stdout if output_file is specified
    stdold = None
    if output_file is not None:
        import sys
        stdold = sys.stdout
        sys.stdout = open(output_file, "w")
    print('&'.join(['']+list(idx2latex.values()))+r'\\')
    print(r'\midrule')
    for idx_row,latex in idx2latex.items():
        print('&'.join([latex]+[
            val(idxs2agreements[(idx_row, idx_col)]) if (idx_row, idx_col) in idxs2agreements else ('$0.0$' if idx_row==idx_col else '')
            for idx_col in idx2latex.keys()
        ])+r'\\')
    # Reset stdout if necessary
    if output_file is not None:
        sys.stdout = stdold

def print_table_realworld():
    print_table(
        *totals(*count_agreements(lambda line: line.startswith('artificial'))),
        output_file='disagreements_realworld.txt'
    )


def print_latex_table_realworld():
    print_latex_table(
        *totals(*count_agreements(lambda line: line.startswith('artificial'))),
        output_file='disagreements_realworld_latex.txt'
    )

def print_latex_mini_table_realworld():
    print_latex_table(
        *totals(*count_agreements(lambda line: line.startswith('artificial'))),
        output_file='disagreements_realworld_latex_mini.txt',
        idx2latex=idx2latex_mini
    )