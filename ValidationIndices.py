from .Clustering import Clustering
import numpy as np
import networkx as nx
import math

# Resolve division by zero
def Fraction(numerator, denominator):
    if denominator != 0:
        return numerator / denominator
    if numerator == 0:
        return 0
    if numerator > 0:
        return float('inf')
    return -float('inf')

def GeneralizedMean(a, b, r=1):
    if r==float('inf'):
        return max(a,b)
    if r==-float('inf'):
        return min(a,b)
    if r>0 or (r<0 and min(a,b)>0):
        return ((a**r+b**r)/2)**(1/r)
    if r==0:
        return math.sqrt(a*b)
    if r<0 and (a==0 or b==0):
        return 0

class Contingency(dict):
    def __init__(self, A, B):
        self.A = Clustering.FromAnything(A)
        self.B = Clustering.FromAnything(B)
        self.n = len(self.A)
        self.meet = Clustering.Meet(self.A, self.B)
        self.sizesA = [
            len(Ai) for Ai in self.A.partition()
        ]
        self.sizesB = [
            len(Bj) for Bj in self.B.partition()
        ]
        super().__init__({
            key: len(p)
            for key, p in self.meet.items()
        })

class Score:
    isdistance = False

    @classmethod
    def score(cls, A, B):
        pass

class PairCounts(dict):
    def __init__(self, N00, N01, N10, N11):
        self.N00 = N00
        self.N01 = N01
        self.N10 = N10
        self.N11 = N11
        super().__init__({'N00':N00, 'N01':N01, 'N10':N10, 'N11':N11})
        self.N = sum(self.values())
        self.mA = N11 + N10
        self.mB = N11 + N01

    def FromClusterings(A, B):
        A = Clustering.FromAnything(A)
        B = Clustering.FromAnything(B)

        mA = A.intra_pairs()
        mB = B.intra_pairs()
        N11 = (A*B).intra_pairs()
        N10 = mA-N11
        N01 = mB-N11
        n = len(A)
        N = int(n*(n-1)/2)
        N00 = N-N11-N10-N01
        return PairCounts(N00, N01, N10, N11)

    def adjacent_counts(self):
        all_directions = {
            "add disagreeing": PairCounts(
                N11=self.N11,
                N10=self.N10,
                N01=self.N01+1,
                N00=self.N00-1,
            ),
            "rem disagreeing": PairCounts(
                N11=self.N11,
                N10=self.N10,
                N01=self.N01-1,
                N00=self.N00+1,
            ),
            "add agreeing": PairCounts(
                N11=self.N11+1,
                N10=self.N10-1,
                N01=self.N01,
                N00=self.N00,
            ),
            "rem agreeing": PairCounts(
                N11=self.N11-1,
                N10=self.N10+1,
                N01=self.N01,
                N00=self.N00,
            )
        }
        # Remove invalid
        return {
            action: pc
            for action, pc in all_directions.items() if not -1 in pc.values()
        }

    def FromGraphs(A,B):
        mA,mB = (len(G.edges) for G in (A,B))
        N11 = len(set(A.edges).intersection(set(B.edges)))
        N = int(len(A.nodes)*(len(A.nodes)-1)/2)
        return PairCounts(N11=N11, N10=mA-N11, N01=mB-N11, N00=N-mA-mB+N11)

    def FromGraphAndClustering(G,C):
        G = nx.Graph(G)
        C = Clustering.FromAnything(C)
        mA = len(G.edges)
        mB = C.intra_pairs()
        N11 = sum([
            1 for v,w in G.edges if C[v]==C[w]
        ])
        N = int(len(C)*(len(C)-1)/2)
        return PairCounts(N11=N11, N10=mA-N11, N01=mB-N11, N00=N-mA-mB+N11)

    def FromClusteringAndGraph(C,G):
        return PairCounts.FromGraphAndClustering(G,C).interchangeAB()

    def FromAnything(anything):
        if type(anything) == PairCounts:
            return anything
        if type(anything) == Contingency:
            sizes2intra = lambda sizes : int((0.5*sizes*(sizes-1)).sum())
            N11=sizes2intra(np.array(list(anything.values())))
            mA,mB = (
                sizes2intra(np.array(sizes))
                for sizes in [anything.sizesA, anything.sizesB]
            )
            N = int(anything.n * (anything.n-1) / 2)
            return PairCounts(
                N11=N11,
                N10=mA-N11,
                N01=mB-N11,
                N00=N-mA-mB+N11
            )
        if type(anything) == dict:
            return PairCounts(**anything)
        if type(anything) == tuple:
            if type(anything[0]) == Clustering and type(anything[1]) == Clustering:
                return PairCounts.FromClusterings(*anything)
            if type(anything[0]) == Clustering and not type(anything[1]) == Clustering:
                return PairCounts.FromClusteringAndGraph(*anything)
            if not type(anything[0]) == Clustering and type(anything[1]) == Clustering:
                return PairCounts.FromGraphAndClustering(*anything)
            else:
                return PairCounts.FromGraphs(*anything)

    def interchangeAB(self):
        return PairCounts(N00=self.N00, N01=self.N10, N10=self.N01, N11=self.N11)

    def invertA(self):
        return PairCounts(N00=self.N10, N01=self.N11, N10=self.N00, N11=self.N01)

    def invertB(self):
        return PairCounts(N00=self.N01, N01=self.N00, N10=self.N11, N11=self.N10)

    def invertAB(self):
        return PairCounts(N00=self.N11, N01=self.N10, N10=self.N01, N11=self.N00)

class ContingencyScore(Score):
    def contingency_score(**kwargs):
        pass

    @classmethod
    def score(cls, A, B, **kwargs):
        A = Clustering.FromAnything(A)
        B = Clustering.FromAnything(B)
        return cls.score_comparison(Contingency(A,B),**kwargs)

    @classmethod
    def score_comparison(cls, cont,**kwargs):
        # Just pray cont is a Contingency
        return cls.contingency_score(contingency=cont,**kwargs)

class PairCountingScore(Score):
    def paircounting_score(**kwargs):
        pass

    @classmethod
    def score(cls, A, B, **kwargs):
        A = Clustering.FromAnything(A)
        B = Clustering.FromAnything(B)
        return cls.score_comparison(PairCounts.FromClusterings(A, B),**kwargs)

    @classmethod
    def score_comparison(cls, pc,**kwargs):
        if type(pc) != PairCounts:
            pc = PairCounts.FromAnything(pc)
        return cls.paircounting_score(**pc, N = pc.N, paircounts = pc,**kwargs)
