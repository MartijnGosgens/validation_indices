from glob import glob
import numpy as np

from sklearn.cluster import KMeans, AffinityPropagation, MeanShift, estimate_bandwidth, AgglomerativeClustering
from sklearn.cluster import DBSCAN, OPTICS, cluster_optics_dbscan, Birch
from sklearn.mixture import GaussianMixture

DIR = 'datasets_parsed'

np.random.seed(0)

def do_kmeans(ft,nc,ni=10):
	k_means = KMeans(init='k-means++', n_clusters=nc, n_init=ni)
	k_means.fit(ft)
	return k_means.labels_

def do_afp(ft):
	return AffinityPropagation().fit(ft).labels_

def do_ms(ft):
	bandwidth = estimate_bandwidth(ft, quantile=0.2, n_samples=500)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=True)
	ms.fit(ft)
	return ms.labels_	

def do_ac(ft, nc, linkage):
    return AgglomerativeClustering(linkage=linkage, n_clusters=nc).fit(ft).labels_

def do_dbs(ft):
	return DBSCAN(eps=0.3, min_samples=10).fit(ft).labels_

def do_opt(ft):
	return OPTICS(xi=.05, min_cluster_size=.05).fit(ft).labels_

def do_gmm(ft, nc, cov):
    return GaussianMixture(n_components=nc, covariance_type=cov, max_iter=20, random_state=0).fit(ft).predict(ft)

def do_birch(ft, nc):
    return Birch(n_clusters=nc).fit(ft).labels_

def save_res(r,fn,label):
	if len(set(r))>1:
		with open(fn[:-3].replace('datasets_parsed','datasets_clusterized')+"."+label,'w') as ofh:
			for item in r:
				print(item, file=ofh)

for fn in glob(DIR+'/*.gt'):
	print(fn)
	gt = np.array([int(line.strip()) for line in open(fn)])
	ft = np.array([ list(map(float,line.strip().split('\t'))) for line in open(fn.replace('.gt','.features'))])
	gt_cn = len(set(gt))
	print('classes', gt_cn)
	cn_options = { 'gt' : gt_cn, }
	if gt_cn>2:	cn_options['2'] = 2
	if int(gt_cn)//2>2: cn_options['gt_half'] = int(gt_cn)//2
	if 2*gt_cn < len(gt): cn_options['gt_double'] = gt_cn*2

	try:
		save_res(do_afp(ft),fn,"cl_affprop")
	except:
		pass
	try:
		save_res(do_ms(ft),fn,"cl_meanshift")
	except:
		pass
	try:
		save_res(do_dbs(ft),fn,"cl_dbscan")
	except:
		pass
	try:
		save_res(do_opt(ft),fn,"cl_optics")
	except:
		pass

	for cnk,cnv in cn_options.items():
		try:
			save_res(do_kmeans(ft,cnv),fn,"cl_kmeans_"+cnk)
		except:
			pass
		try:
			save_res(do_birch(ft,cnv),fn,"cl_birch_"+cnk)
		except:
			pass
		for linkage in ('ward', 'average', 'complete', 'single'):
			try:
				save_res(do_ac(ft,cnv,linkage),fn,"cl_aggcl_"+linkage+"_"+cnk)
			except:
				pass
		for cov_type in ['spherical', 'diag', 'tied', 'full']:
			try:
				save_res(do_gmm(ft,cnv,cov_type),fn,"cl_gmm_"+cov_type+"_"+cnk)
			except:
				pass
