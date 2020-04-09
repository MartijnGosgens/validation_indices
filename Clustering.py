import numpy as np
import itertools as iter

class Clustering(list):
    def __init__(self, clustering_list):
        super().__init__(clustering_list)
        self.clusters = {}
        for i, c in enumerate(clustering_list):
            if not c in self.clusters:
                self.clusters[c] = set()
            self.clusters[c]=self.clusters[c].union({i})

    # Override
    def __setitem__(self, key, value):
        self.clusters[self[key]]-={key}
        if not value in self.clusters:
            self.clusters[value] = set()
        self.clusters[value] = self.clusters[value].union({key})
        if len(self.clusters[self[key]]) == 0:
            del self.clusters[self[key]]
        super(Clustering, self).__setitem__(key, value)

    # Override
    def copy(self):
        return Clustering(super().copy())

    def labels(self):
        return set(self)

    def append(self, value):
        self.clusters[value] = self.clusters[value].union({len(self)})
        super(Clustering, self).append(value)

    def swap(self, i, j):
        self[i], self[j] = self[j], self[i]

    def merge(self, c1, c2):
        for i, c in enumerate(self):
            if c==c2:
                self[i] = c1
        del self.clusters[c2]

    def newlabel(self):
        labels = self.clusters.keys()
        label = len(labels)
        while label in labels:
            label = (label+1) % len(labels)
        return label

    def splitoff(self, newset):
        label = self.newlabel()
        for i in newset:
            self[i] = label

    def intra_pairs(self):
        return sum([
            int(size*(size-1)/2)
            for size in self.sizes()
        ])

    def intra_pairs_iter(self):
        for c in self.clusters.values():
            for i,j in iter.combinations(c,2):
                yield (i,j)

    def density(self):
        return self.intra_pairs() / ((len(self)*(len(self)-1))/2)

    def partition(self):
        return list(self.clusters.values())

    def sizes(self):
        return [
            len(cluster) for cluster in self.clusters.values()
        ]

    def Meet(A, B):
        return {
            (i,j): Ai.intersection(Bj)
            for i,Ai in enumerate(A.partition())
            for j,Bj in enumerate(B.partition())
        }

    # Operator overload of A*B will return the meet of the clusterings.
    def __mul__(self,other):
        return Clustering.FromPartition(Clustering.Meet(self,other).values())

    def FromSizes(sizes):
        return Clustering(sum([
            [c]*size
            for c, size in enumerate(sizes)
        ],[]))

    def FromPartition(partition):
        # Assume that partition contains all integers in [0..n-1]
        n = sum([len(p) for p in partition])
        clustering = list(range(n))
        for c,p in enumerate(partition):
            for i in p:
                clustering[i] = c
        return Clustering(clustering)

    def FromAnything(A):
        # Check if not already a clustering.
        if type(A) == Clustering:
            return A
        # If its a dict, we assume its just a labeled partition.
        if isinstance(A, dict):
            return Clustering.FromPartition(A.values())
        # See whether it is iterable.
        if hasattr(A, '__iter__'):
            A = list(A)
            # If the first item is an integer, we assume it's a list
            # of clusterlabels so that we can call the constructor.
            if type(A[0])==int:
                return Clustering(A)
            elif type(A[0]) in {set, list}:
                # If the first item is a set or list, we consider it a partition.
                return Clustering.FromPartition(A)
        print('Clustering.FromAnything was unable to cast {}'.format(A))

    def BalancedSizes(n, k):
        smallSize = int(n/k)
        n_larger = n - k * smallSize
        return [smallSize + 1] * n_larger + [smallSize] * (k - n_larger)

    def BalancedClustering(n, k):
        return Clustering.FromSizes(Clustering.BalancedSizes(n, k))

    def random_same_sizes(self, rand=None):
        if rand == None:
            rand = np.random
        c = list(self).copy()
        rand.shuffle(c)
        return Clustering(c)

    def UniformRandom(n, k, rand=None):
        if rand == None:
            rand = np.random
        return Clustering(rand.randint(k, size=n))

class HierarchicalClustering(Clustering):
    # Clustering but with additional list with sets of vertices that are represented by the aggregate-vertex.
    def __init__(self, clustering_list,previouslevel=None):
        super().__init__(clustering_list)
        self.clusters = {}
        for i, c in enumerate(clustering_list):
            if not c in self.clusters:
                self.clusters[c] = set()
            self.clusters[c]=self.clusters[c].union({i})
        self.previouslevel = previouslevel

    # Override
    def copy(self):
        c = super().copy()
        previous = self.previouslevel
        if previous != None:
            previous = previous.copy()
        return HierarchicalClustering(c,previous)

    # Override
    def partition(self):
        return Clustering(self).partition()

    def nextlevel(self):
        partition = self.partition()
        return HierarchicalClustering(list(range(len(partition))),self)

    def level(self, lvl):
        if self.previouslevel == None:
            return self
        if lvl <= 0:
            return self.flatClustering()
        return self.previouslevel.level(lvl-1)

    def flatClustering(self):
        if self.previouslevel == None:
            return self
        subpartition = self.previouslevel.flatClustering().partition()
        return Clustering.FromPartition([
            set().union(*[
                subpartition[i]
                for i in p
            ])
            for p in self.partition()
        ])

    # Returns the Clusterings corresponding to each level of the hierarchy
    def getlevels(self, flat=True):
        levels = []
        lvl = self
        while not lvl==None:
            if flat:
                levels.append(lvl.flatClustering())
            else:
                levels.append(lvl)
            lvl = lvl.previouslevel
        return levels

    # Returns all intra_pairs that are not in the previous level
    def new_intra_pairs(self):
        if self.previouslevel == None:
            return set().union(*[{
                    (min(e),max(e))
                    for e in iter.combinations(p,2)
                }
                for p in self.partition()
            ])
        previouspartition = self.previouslevel.partition()
        return set().union(*[{
                (min(e),max(e))
                for e in iter.product(previouspartition[i],previouspartition[j])
            }
            for c in self.clusters.values()
            for i,j in iter.combinations(c,2)
        ])

    def flatitems(self, topitems):
        if self.previouslevel == None:
            return topitems
        P = self.previouslevel.partition()
        return set().union(*[
            self.previouslevel.flatitems(P[i])
            for i in topitems
        ])
