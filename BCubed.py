import numpy as np

from .Clustering import Clustering
from .ValidationIndices import Contingency, ContingencyScore, Fraction
from collections import Counter

class BCubed(ContingencyScore):
    @classmethod
    def contingency_score(cls, contingency, **kwargs):
        recall = sum([
            sum(
                contingency[i,j]**2
                for j in contingency.B.labels()
                if (i,j) in contingency
            ) / s
            for i,s in Counter(contingency.A).items()
        ])/contingency.n
        precision = sum([
            sum(
                contingency[i,j]**2
                for i in contingency.A.labels()
                if (i,j) in contingency
            ) / s
            for j,s in Counter(contingency.B).items()
        ])/contingency.n
        return 2*Fraction(recall*precision, recall + precision)

