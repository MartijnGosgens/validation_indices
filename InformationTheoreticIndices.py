import numpy as np

from .Clustering import Clustering
from .ValidationIndices import Contingency, ContingencyScore, Fraction, Score

# Tsallis generalized q-entropy. Regular Shannon entropy for q in the limit to 1 (q=1, works here)
# For q=2, the VI induced by this entropy is equal to the adjusted Mirkin metric.
def Entropy(dist, q=1):
    # Make sure dist is a distribution
    dist = np.array(dist)
    dist = dist / dist.sum()
    nonzero = dist[dist.nonzero()]
    if q==1:
        return -(nonzero * np.log(nonzero)).sum()
    else:
        return ( 1 / (q-1) ) * ( 1 - ( nonzero ** 2 ).sum())

class InformationTheoreticScore(ContingencyScore):
    @classmethod
    def score_comparison(cls, cont,**kwargs):
        # Just pray cont is a Contingency
        # Add entropy values if abscent.
        entropyA = Entropy(cont.sizesA)
        entropyB = Entropy(cont.sizesB)
        entropyJoint = Entropy(list(cont.values()))
        return cls.contingency_score(entropyA=entropyA, entropyB=entropyB, entropyJoint=entropyJoint, contingency=cont, **kwargs)

class VariationOfInformation(InformationTheoreticScore):
    isdistance = True
    @classmethod
    def contingency_score(cls, entropyA, entropyB, entropyJoint, **kwargs):
        return 2*entropyJoint - entropyA - entropyB

class NormalizedMutualInformation(InformationTheoreticScore):
    @classmethod
    def normalization(cls, **kwargs):
        pass

    @classmethod
    def contingency_score(cls, entropyA, entropyB, entropyJoint, **kwargs):
        return Fraction(
            (entropyA + entropyB - entropyJoint),
            cls.normalization(
                entropyA=entropyA,
                entropyB=entropyB,
                entropyJoint=entropyJoint,
                **kwargs
        ))

class MaxNMI(NormalizedMutualInformation):
    @classmethod
    def normalization(cls, entropyA, entropyB, **kwargs):
        return max(entropyA, entropyB)

class MinNMI(NormalizedMutualInformation):
    @classmethod
    def normalization(cls, entropyA, entropyB, **kwargs):
        return min(entropyA, entropyB)

class AvgNMI(NormalizedMutualInformation):
    @classmethod
    def normalization(cls, entropyA, entropyB, **kwargs):
        return (entropyA + entropyB) / 2

class GeoNMI(NormalizedMutualInformation):
    @classmethod
    def normalization(cls, entropyA, entropyB, **kwargs):
        return np.sqrt(entropyA * entropyB)

class FairNMI(NormalizedMutualInformation):
    @classmethod
    def normalization(cls, entropyA, entropyB, contingency, **kwargs):
        R = len(contingency.sizesA)
        S = len(contingency.sizesB)
        return np.exp(abs(R-S)/R)*(entropyA + entropyB) / 2

from sklearn.metrics import adjusted_mutual_info_score
class AdjustedMutualInformation(Score):
    @classmethod
    def score(cls, A, B):
        A, B = (Clustering.FromAnything(C) for C in [A,B])
        return adjusted_mutual_info_score(A,B)