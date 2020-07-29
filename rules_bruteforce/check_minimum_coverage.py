from collections import defaultdict, Counter
import random
from validation_indices import Indices
from numpy import sign

# number of pairs to separate
target = 178

# set of rules to check
rules = (
    ((1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 3, 2, 3, 2, 0, 2), (3, 1, 2, 3, 2, 2, 2, 1), "#rule 1#"),
    ((1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 0, 0, 3, 2, 3, 2), (2, 2, 3, 0, 0, 3, 0, 2), "#rule 2#"),
    ((1, 1, 2, 3, 3, 2, 2, 2), (3, 0, 1, 2, 1, 0, 3, 2), (1, 3, 1, 1, 3, 3, 2, 3), "#rule 3#"),
    ((2, 1, 0, 0, 1, 0, 0, 2, 1), (2, 0, 1, 2, 0, 2, 2, 1, 0), (2, 0, 0, 0, 0, 1, 0, 2, 0), "#rule 4#"),

)

covered = dict()
for r_idx, rule in enumerate(rules):
    gt,p1,p2,r_name = rule

    r1 = dict()
    r2 = dict()
    for i in Indices:
        r1[i.__name__] = i.score(gt,p1)
        r2[i.__name__] = i.score(gt,p2)
    r1['CorrelationDistance'] = -r1['CorrelationDistance']
    r2['CorrelationDistance'] = -r2['CorrelationDistance']
    r1['VariationOfInformation'] = -r1['VariationOfInformation']
    r2['VariationOfInformation'] = -r2['VariationOfInformation']

    for _i1, idx1 in enumerate(sorted(r1)):
        for _i2, idx2 in enumerate(sorted(r2)):
            if (idx1,idx2) in covered: continue # already covered
            if sign(r1[idx1]-r2[idx1])!=sign(r1[idx2]-r2[idx2]) and sign(r1[idx1]-r2[idx1])!=0 and sign(r1[idx2]-r2[idx2])!=0:
                covered[(idx1,idx2)] = r_name

print('Covered {} from {}, coverage: {}\n\n'.format(len(covered)==target,len(covered),target))
print("\t"+"\t".join([idx1 for idx1 in sorted(r1)]))

# print matrix of coverage rules
for idx1 in sorted(r1):
    r = [idx1,] + [covered.get((idx1,idx2),'') for idx2 in sorted(r1)]
    print("\t".join(map(str,r)))
