import numpy as np

from .Clustering import Clustering
from .ValidationIndices import Contingency, ContingencyScore, Fraction

class BCubed(ContingencyScore):
    @classmethod
    def contingency_score(cls, contingency, **kwargs):
        recall = sum([
            sum(
                contingency[i,j]**2
                for j in range(len(contingency.sizesB))
            ) / contingency.sizesA[i]
            for i in range(len(contingency.sizesA))
        ])/contingency.n
        precision = sum([
            sum(
                contingency[i,j]**2
                for i in range(len(contingency.sizesA))
            ) / contingency.sizesB[j]
            for j in range(len(contingency.sizesB))
        ])/contingency.n
        return 2*Fraction(recall*precision, recall + precision)

