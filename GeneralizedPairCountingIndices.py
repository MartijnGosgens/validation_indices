import itertools as iter
from .ValidationIndices import PairCounts
from .PairCountingIndices import PearsonCoefficient
import networkx as nx
from .Clustering import Clustering

def DiceSimilarity(i,j,G):
    Ni,Nj = (set(G[i]).union({i}),set(G[j]).union({j}))
    return 2*len(Ni.intersection(Nj))/(len(Ni)+len(Nj))


def GeneralizedJaccardSimilarity(i,j,G,alpha=0,exponent=1):
    Ni,Nj = (set(G[i]).union({i}),set(G[j]).union({j}))
    intersection = len(Ni.intersection(Nj))
    union = len(Ni.union(Nj))
    return ((alpha+1)*intersection / (union + alpha*intersection)) ** exponent

class GeneralizedPairCounts(PairCounts):
    def FromGraphAndClustering(G,C,similarity=None):
        G = nx.Graph(G)
        C = Clustering.FromAnything(C)
        if similarity == None:
            similarity = lambda i,j,G: 1 if i in G[j] else 0
        mA = sum([
            similarity(i,j,G)
            for i,j in iter.combinations(G.nodes,2)
        ])
        mB = C.intra_pairs()
        N11 = sum([
            similarity(v,w,G) for v,w in C.intra_pairs_iter()
        ])
        N = int(len(C)*(len(C)-1)/2)
        return PairCounts(N11=N11, N10=mA-N11, N01=mB-N11, N00=N-mA-mB+N11)

def GeneralizedPairCountingQuality(G,C,similarity=None, paircountingscore=PearsonCoefficient):
    return paircountingscore.score_comparison(
        pc = GeneralizedPairCounts.FromGraphAndClustering(G,C,similarity=similarity)
    )

def DiceCorrelation(G,C):
    return GeneralizedPairCountingQuality(G,C,similarity=DiceSimilarity, paircountingscore=PearsonCoefficient)
