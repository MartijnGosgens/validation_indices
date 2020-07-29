from .Clustering import Clustering
import shapely
from shapely.geometry import Polygon,Point,MultiPoint
import itertools as it
from matplotlib import pyplot as plt
import networkx as nx

# Inconsistency triplets
# (1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 3, 2, 3, 2, 0, 2), (3, 1, 2, 3, 2, 2, 2, 1)
rule1 = {
    "gt": Clustering([1, 1, 2, 3, 3, 2, 2, 2]),
    "L": Clustering([1, 1, 3, 2, 3, 2, 0, 2]),
    "R": Clustering([3, 1, 2, 3, 2, 2, 2, 1])
}
# (1, 1, 2, 3, 3, 2, 2, 2), (1, 1, 0, 0, 3, 2, 3, 2), (2, 2, 3, 0, 0, 3, 0, 2)
rule2 = {
    "gt": Clustering([1, 1, 2, 3, 3, 2, 2, 2]),
    "L": Clustering([1, 1, 0, 0, 3, 2, 3, 2]),
    "R": Clustering([2, 2, 3, 0, 0, 3, 0, 2])
}
# (1, 1, 2, 3, 3, 2, 2, 2), (3, 0, 1, 2, 1, 0, 3, 2), (1, 3, 1, 1, 3, 3, 2, 3)
rule3 = {
    "gt": Clustering([1, 1, 2, 3, 3, 2, 2, 2]),
    "L": Clustering([3, 0, 1, 2, 1, 0, 3, 2]),
    "R": Clustering([1, 3, 1, 1, 3, 3, 2, 3])
}
# (2, 1, 0, 0, 1, 0, 0, 2, 1), (2, 0, 1, 2, 0, 2, 2, 1, 0), (2, 0, 0, 0, 0, 1, 0, 2, 0)
rule4 = {
    "gt": Clustering([2, 1, 0, 0, 1, 0, 0, 2, 1]),
    "L": Clustering([2, 0, 1, 2, 0, 2, 2, 1, 0]),
    "R": Clustering([2, 0, 0, 0, 0, 1, 0, 2, 0])
}
rules = [rule1,rule2,rule3,rule4]
markers = ["o","s","v","D"]
colors = ['red','green','blue','purple']

# Plot a pair of ground truth and candidate. The markers denote the ground truth
# clustering while the colored regions denote the candidate clustering.
# layout is a placement of the points. Ideally, this layout places the point so
# that the regions don't overlap.
def plot_clusterings(gt,candidate,layout,ax=None,buffer=0.16):
    if ax==None:
        fig = plt.figure(1, figsize=(10,10))
        ax = fig.add_subplot()
        ax.axis('off')
    for p in candidate.partition():
        ax.fill(*MultiPoint([layout[i] for i in p]).convex_hull.buffer(buffer).exterior.xy, alpha=0.5, ec='none',fc='orange')
    for c,p in gt.clusters.items():
        xs = [layout[i].x for i in p]
        ys = [layout[i].y for i in p]
        ax.plot(xs,ys,marker=markers[c],markersize=15,linestyle='none',markerfacecolor=colors[c],markeredgecolor='black')

# We construct overlapping partition and compute its graph layout to find a
# reasonable placement of the items such that the regions of don't overlap.
def graph_layout(L,R):
    G = nx.Graph()
    G.add_edges_from(L.intra_pairs_iter())
    G.add_edges_from(R.intra_pairs_iter())
    return {i: Point(*p) for i,p in nx.layout.spring_layout(G,seed=0,k=0.1).items()}

# Generate the figures
for i,rule in zip(range(1,5),rules):
    figL,axL=plt.subplots(1,1,figsize=(5,5))
    figR,axR=plt.subplots(1,1,figsize=(5,5))
    axL.axis('off')
    axR.axis('off')

    G = nx.Graph()
    G.add_edges_from(rule['L'].intra_pairs_iter())
    G.add_edges_from(rule['R'].intra_pairs_iter())
    graph_layout={i: Point(*p) for i,p in nx.layout.spring_layout(G,seed=0,k=0.1).items()}

    plot_clusterings(rule['gt'],rule['L'],layout=graph_layout,ax=axL,buffer=0.16)
    plot_clusterings(rule['gt'],rule['R'],layout=graph_layout,ax=axR,buffer=0.16)
    figL.savefig('rule{}L.pdf'.format(i))
    figR.savefig('rule{}R.pdf'.format(i))
