from collections import defaultdict, Counter
import random
from validation_indices import Indices
from itertools import combinations
from numpy import sign

random.seed(0xBEEFF00D)
RETRIES = 2000
INDICES = 14

def get_random_partition(gt_cl, gt_npc):
    return tuple([random.randint(0,gt_cl-1) for _ in range(gt_cl*gt_npc)])

# The found triplets, stored in a dictionary.
# The keys give the preferences for each of the indices, it is represented by
# a vector x\in{-1,1}^|Indices| with with x[i]=1 if Indices[i] prefers
# candidate 1 and x[i]=-1 if it prefers candidate 2.


# 1. first, we will collect a lot of different triplets
def generate_rules():
    rules = dict()
    # for ground truth number of items per cluster
    for gt_npc in range(2,5):
        # for ground truth number of clusters
        for gt_cl in range(2,5):
            # generate ground truth partition
            gt = get_random_partition(gt_cl, gt_npc)
            for _ in range(RETRIES):
                p1 = get_random_partition(gt_cl, gt_npc)
                p2 = get_random_partition(gt_cl, gt_npc)
                # Make sure they aren't identical
                while p2 == p1:
                    p2 = get_random_partition(gt_cl, gt_npc)

                r1 = dict()
                r2 = dict()
                # calc all indices
                for i in Indices:
                    r1[i.__name__] = i.score(gt,p1)
                    r2[i.__name__] = i.score(gt,p2)
                # flip signs of opposite directed indices
                r1['VariationOfInformation'] = -r1['VariationOfInformation']
                r2['VariationOfInformation'] = -r2['VariationOfInformation']
                r1['CorrelationDistance'] = -r1['CorrelationDistance']
                r2['CorrelationDistance'] = -r2['CorrelationDistance']

                # collect signs of diffs btw gt_vs_p1 and gt_vs_p2
                signs = []
                for idx1 in sorted(r1):
                    signs.append( sign(r1[idx1]-r2[idx1]) )

                # now this signs vector is a signature which determines separable indices
                signs = tuple(signs)
                c_signs = Counter(signs)
                if c_signs[1]>=4 and c_signs[-1]>=4 and not c_signs[0]:
                    # we don't want to use rules with less than 4 indices in one of the groups --
                    # because such rule is too weak to form a basis
                    if signs not in rules:
                        rules[signs] = ((gt_cl,gt_npc),signs,gt,p1,p2,c_signs)
    return rules
rules = generate_rules()
print('collected',len(rules),'rules in total')

# 2. count the maximum number of pairs we need to separate and collect each separated pair for given rule
separated = defaultdict(set)
for rule in rules:
    limit = 0
    for i1 in range(INDICES):
        for i2 in range(INDICES):
            if rule[i1] != rule[i2]:
                separated[rule].add((i1,i2))
            if i1 != i2:
                limit += 1
limit -= 4 # cause we can't separate CD from PC and JI from DI
print('we need to separate {} different pairs'.format(limit))

# 3. now we'll bruteforce through all possiblie cominations of 4 rules until we find the full coverage
def find4rules():
    rules_keys = list(rules.keys())
    best = -1
    for combo in combinations(range(len(rules_keys)),4):
        current = set()
        for rule_idx in combo:
            current |= separated[rules_keys[rule_idx]]
        if len(current)>best:
            best = len(current)
            if best == limit:
                print('A minimal number of rules has been found.')
                return [rules[rules_keys[rule_idx]] for rule_idx in combo]
best_rules = find4rules()
for i,rule in enumerate(best_rules):
    print('Rule{}:'.format(i+1),rule[2:5])
