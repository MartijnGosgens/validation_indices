import numpy as np

from .Clustering import Clustering
from .ValidationIndices import Contingency, ContingencyScore, Fraction

class FMeasure(ContingencyScore):
    @classmethod
    def contingency_score(cls, contingency, **kwargs):
        recall = sum([
            max([
                contingency[i,j]
                for j in range(len(contingency.sizesB))
            ])
            for i in range(len(contingency.sizesA))
        ]) / contingency.n
        precision = sum([
            max([
                contingency[i,j]
                for i in range(len(contingency.sizesA))
            ])
            for j in range(len(contingency.sizesB))
        ]) / contingency.n
        return 2*Fraction(recall*precision, recall + precision)


