from collections import defaultdict, Counter
import random
from validation_indices import Indices
from numpy import sign

# set of rules to describe
rules = (
    ((1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 3, 2, 3, 2, 0, 2), (3, 1, 2, 3, 2, 2, 2, 1), "#rule 1#"),
    ((1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 0, 0, 3, 2, 3, 2), (2, 2, 3, 0, 0, 3, 0, 2), "#rule 2#"),
    ((1, 1, 2, 3, 3, 2, 2, 2), (3, 0, 1, 2, 1, 0, 3, 2), (1, 3, 1, 1, 3, 3, 2, 3), "#rule 3#"),
    ((2, 1, 0, 0, 1, 0, 0, 2, 1), (2, 0, 1, 2, 0, 2, 2, 1, 0), (2, 0, 0, 0, 0, 1, 0, 2, 0), "#rule 4#"),
)

covered = dict()
for r_idx, rule in enumerate(rules):
    gt,p1,p2,r_name = rule

    nn = []
    gtnc = []
    p1nc = []
    p2nc = []
    p1vals = list(sorted(set(p1)))
    p2vals = list(sorted(set(p2)))
    for i in range(len(gt)):
        nn.append('item'+str(i))
        gtnc.append(str(gt[i]))
        p1nc.append(str(p1vals.index(p1[i])))
        p2nc.append(str(p2vals.index(p2[i])))

    print("\n\nRULE "+r_name)

    # print the partitions
    print("\t"+"\t".join(nn))
    print("GT\t"+"\t".join(gtnc))
    print("P1\t"+"\t".join(p1nc))
    print("P2\t"+"\t".join(p2nc))
    print()

    r1 = dict()
    r2 = dict()
    for i in Indices:
        r1[i.__name__] = i.score(gt,p1)
        r2[i.__name__] = i.score(gt,p2)
    r1['CorrelationDistance'] = -r1['CorrelationDistance']
    r2['CorrelationDistance'] = -r2['CorrelationDistance']
    r1['VariationOfInformation'] = -r1['VariationOfInformation']
    r2['VariationOfInformation'] = -r2['VariationOfInformation']

    # print the indices
    print("\t"+"\t".join([idx1 for idx1 in sorted(r1)]))
    print("GT_vs_P1\t"+"\t".join(map(str,[r1[idx1] for idx1 in sorted(r1)])))
    print("GT_vs_P2\t"+"\t".join(map(str,[r2[idx1] for idx1 in sorted(r1)])))
    print("DIFF SGN\t"+"\t".join(map(str,[sign(r1[idx1]-r2[idx1]) for idx1 in sorted(r1)])))
    
