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

def minimize(C):
    mapping = {}
    minimized = []
    for c in C:
        if c not in mapping:
            mapping[c] = len(mapping)
        minimized.append(mapping[c])
    return minimized
from .rules_bruteforce.check_minimum_coverage import rules as checked_rules
rules = [
    {
        "gt": Clustering(minimize(gt)),
        "L": Clustering(minimize(L)),
        "R": Clustering(minimize(R))
    }
    for (gt,L,R,_) in checked_rules
]
markers = ["o","s","v","D","P",'*']
colors = ['red','green','blue','purple','yellow','orange']

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
def graph_layout(L,R,k=0.1,seed=0,weightL=1,weightR=1):
    G = nx.Graph()
    G.add_nodes_from(range(len(L)))
    G.add_weighted_edges_from([
        (i,j,3.0)
        for i,j in (L*R).intra_pairs_iter()
    ])
    G.add_weighted_edges_from([
        (i,j,weightL)
        for i,j in L.intra_pairs_iter()
    ])
    G.add_weighted_edges_from([
        (i,j,weightR)
        for i,j in R.intra_pairs_iter()
    ])
    return {i: Point(*p) for i,p in nx.layout.spring_layout(G,seed=seed,k=k,weight='weight').items()}

# Tweak these to get the desired layout
layout_argss = [
    {},
    {'k': 1.6, 'seed': 3},
    {},
    {'k': 0.08, 'seed': 4, 'weightL': 4.1, 'weightR': 1.5}
]

def show_rule(rule,rule_nr,**layout_args):
    figL, axL = plt.subplots(1, 1, figsize=(5, 5))
    figR, axR = plt.subplots(1, 1, figsize=(5, 5))
    axL.axis('off')
    axR.axis('off')

    layout = graph_layout(rule['L'], rule['R'], **layout_args)

    plot_clusterings(rule['gt'], rule['L'], layout=layout, ax=axL, buffer=0.16)
    plot_clusterings(rule['gt'], rule['R'], layout=layout, ax=axR, buffer=0.16)
    figL.savefig('rule{}L.pdf'.format(rule_nr))
    figR.savefig('rule{}R.pdf'.format(rule_nr))

# Generate the figures
for rule,i,layout_args in zip(rules,range(1,5),layout_argss):
    show_rule(rule,i,**layout_args)
