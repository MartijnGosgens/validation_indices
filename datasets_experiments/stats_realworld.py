# from glob import glob
import json
from collections import defaultdict
from scipy.stats.stats import pearsonr, spearmanr
from numpy import sign

def sgn(a):
	if a>0.: return 1
	elif a<0.: return -1
	return 0

exps = set()
dses = set()
ptes = set()

index_dict = defaultdict(dict)
for line in open('all_datasets_methods_metrics.tsv'):
	if line.startswith('artificial'): continue # skip artificial

	ds, pt, idx, val = line.strip().split("\t")
	val = float(val)
	if idx in ('CorrelationDistance', 'VariationOfInformation'):
		val = -val
	index_dict[idx][(ds,pt)] = val
	exps.add( (ds,pt) )
	dses.add( ds )
	ptes.add( pt )

index_vector = defaultdict(list)
for idx, dct in index_dict.items():
	index_vector[idx] = [ item[1] for item in sorted(dct.items()) ]

print('Pearson')
print("\t"+"\t".join([idx1 for idx1 in sorted(index_vector)]))

for idx1 in sorted(index_vector):
	r = [idx1,]
	for idx2 in sorted(index_vector):
		r.append(pearsonr(index_vector[idx1],index_vector[idx2])[0])
	print("\t".join(map(str,r)).replace(".",","))

print('\nSpearman')
print("\t"+"\t".join([idx1 for idx1 in sorted(index_vector)]))

for idx1 in sorted(index_vector):
	r = [idx1,]
	for idx2 in sorted(index_vector):
		r.append(spearmanr(index_vector[idx1],index_vector[idx2])[0])
	print("\t".join(map(str,r)).replace(".",","))

cases = len(exps)*(len(exps)-1)//2
print("\nInconsistency cases, from XXX total")
print("\t"+"\t".join([idx1 for idx1 in sorted(index_vector)]))

index_method = defaultdict(int)

for idx1 in sorted(index_vector):
	r = [idx1,]
	for idx2 in sorted(index_vector):
		cnt = 0
		ttl = 0
		for ds in dses:
			for i1, pt1 in enumerate(sorted(ptes)):
				for i2, pt2 in enumerate(sorted(ptes)):
					if (ds,pt1) not in index_dict[idx1]: continue
					if (ds,pt1) not in index_dict[idx2]: continue
					if (ds,pt2) not in index_dict[idx1]: continue
					if (ds,pt2) not in index_dict[idx2]: continue
					if i1<i2:
						if sign(index_dict[idx1][(ds,pt1)]-index_dict[idx1][(ds,pt2)]) != sign(index_dict[idx2][(ds,pt1)]-index_dict[idx2][(ds,pt2)]):
							cnt += 1
						ttl += 1
		r.append(cnt)
	print("\t".join(map(str,r)).replace(".",","))

print('XXX = {}'.format(ttl))
