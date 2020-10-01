from glob import glob
import numpy as np
import os

from sklearn.cluster import KMeans, AffinityPropagation, MeanShift, estimate_bandwidth, AgglomerativeClustering
from sklearn.cluster import DBSCAN, OPTICS, cluster_optics_dbscan, Birch
from sklearn.mixture import GaussianMixture

np.random.seed(0)

def do_kmeans(ft,nc,ni=10):
	k_means = KMeans(init='k-means++', n_clusters=nc, n_init=ni)
	k_means.fit(ft)
	return k_means.labels_

def do_affinitypropagation(ft):
	return AffinityPropagation(random_state=0).fit(ft).labels_

def do_meanshift(ft):
	bandwidth = estimate_bandwidth(ft, quantile=0.2, n_samples=500)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=True)
	ms.fit(ft)
	return ms.labels_

def do_agglomerativeclustering(ft, nc, linkage):
    return AgglomerativeClustering(linkage=linkage, n_clusters=nc).fit(ft).labels_

def do_dbscan(ft):
	return DBSCAN(eps=0.3, min_samples=10).fit(ft).labels_

def do_optics(ft):
	return OPTICS(xi=.05, min_cluster_size=.05).fit(ft).labels_

def do_gausianmixture(ft, nc, cov):
    return GaussianMixture(n_components=nc, covariance_type=cov, max_iter=20, random_state=0).fit(ft).predict(ft)

def do_birch(ft, nc):
    return Birch(n_clusters=nc).fit(ft).labels_

algorithms_no_args = {
    'cl_affprop': do_affinitypropagation,
    'cl_meanshift': do_meanshift,
    'cl_dbscan': do_dbscan,
    'cl_optics': do_optics,
}

def algorithms_gtk(gtk,n):
	ks = {'gt': gtk}
	if gtk>2:
		ks['2'] = 2
	if gtk // 2 > 2:
		ks['gt_half'] = gtk//2
	if 2*gtk < n:
		ks['gt_double'] = 2*gtk
	algorithms = {}
	algorithms.update(algorithms_no_args)
	algorithms.update({
		'cl_kmeans_'+k: lambda features: do_kmeans(features,nc=k)
		for k in ks
	})
	algorithms.update({
		'cl_birch_'+k: lambda features: do_birch(features,nc=k)
		for k in ks
	})
	for linkage in ('ward', 'average', 'complete', 'single'):
		algorithms.update({
			"cl_aggcl_{}_{}".format(linkage,k_name): lambda features: do_agglomerativeclustering(features,nc=k,linkage=linkage)
			for k_name,k in ks.items()
		})
	for cov in ['spherical', 'diag', 'tied', 'full']:
		algorithms.update({
			"cl_gmm_{}_{}".format(cov, k_name): lambda features: do_gausianmixture(features, nc=k, cov=cov)
			for k_name,k in ks.items()
		})
	return algorithms

def apply_clustering_algorithms():
	for fn in glob('parsed/*.gt'):
		gt = np.array([int(line.strip()) for line in open(fn)])
		features = np.array([ list(map(float,line.strip().split('\t'))) for line in open(fn.replace('.gt','.features'))])
		gtk = len(set(gt))
		print(fn,'gtk =', gtk)
		algorithms = algorithms_gtk(gtk,len(gt))
		for name,algorithm in algorithms.items():
			result_fn = fn.replace('parsed','candidates')[:-2]+name
			# See whether result has already been computed
			if os.path.isfile(result_fn):
				print(name,'already exists')
				continue
			try:
				result = algorithm(features)
				candidate_k = len(set(result))
				# Disregard results if one cluster is returned
				if candidate_k <= 1:
					continue
				print(name,'resulted in',candidate_k,'classes')
				with open(result_fn,'w') as file:
					for item in result:
						print(item,file=file)
			except:
				print(name,'did not succeed')
