import numpy as np

from .Clustering import Clustering
from .ValidationIndices import Contingency, ContingencyScore, Fraction

class FMeasure(ContingencyScore):
    @classmethod
    def contingency_score(cls, contingency, **kwargs):
        recall = sum([
            max([
                contingency[i,j]
                for j in contingency.B.labels()
                if (i,j) in contingency
            ])
            for i in contingency.A.labels()
        ]) / contingency.n
        precision = sum([
            max([
                contingency[i,j]
                for i in contingency.A.labels()
                if (i,j) in contingency
            ])
            for j in contingency.B.labels()
        ]) / contingency.n
        return 2*Fraction(recall*precision, recall + precision)


