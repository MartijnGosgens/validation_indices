from . import Clustering
from .ValidationIndices import Contingency
from scipy.stats import chisquare, f_oneway
import numpy as np
from collections import Counter

def bias_chisquare(I, gt, sizes2compare, repeats=100, rand=None):
    '''
    Uses chisquare to test the hypothesis that a random clustering from each of
    the sizes will have the same probability of achieving the maximum score
    (among the sizes).

    Parameters
    -------
    I : Score
        The validation index that is tested
    gt : Clusterings
        The ground truth partition
    sizes2compare : list
        A list containing the clustersizes that we want to compare. Each
        clustersizes should be represented by a list of integers summing len(gt).
    repeats : int
        The number of clusterings generated from each clustersizes distribution.
    rand : numpy.random.RandomState
        Used for making the generation of clusterings reproducable.
    '''
    appendCounter = lambda c: [
        0 if not i in c else c[i]
        for i in range(len(sizes2compare))
    ]

    score_evaluations = [
        [
            I.score(gt, Clustering.FromSizes(sizes).random_same_sizes(rand))
            for sizes in sizes2compare
        ]
        for _ in range(repeats)
    ]
    # For each repeat, check which sizes achieved the highest score
    winners = appendCounter(Counter([
        sample.index(max(sample))
        for sample in score_evaluations
    ]))
    # return the p value and the sizes that 'won' most often
    return {
        'p': chisquare(winners).pvalue,
        'bestsizes': sizes2compare[winners.index(max(winners))]
    }

def bias_anova(I, gt, sizes2compare, repeats=100, rand=None):
    '''
    Uses one-way ANOVA for the null-hypothesis that for all of the sizes give
    the same expected score of the index.

    Parameters
    -------
    I : Score
        The validation index that is tested
    gt : Clusterings
        The ground truth partition
    sizes2compare : list
        A list containing the clustersizes that we want to compare. Each
        clustersizes should be represented by a list of integers summing len(gt).
    repeats : int
        The number of clusterings generated from each clustersizes distribution.
    rand : numpy.random.RandomState
        Used for making the generation of clusterings reproducable.
    '''
    score_evaluations = [
        [
            I.score(gt, Clustering.FromSizes(sizes).random_same_sizes(rand))
            for _ in range(repeats)
        ]
        for sizes in sizes2compare
    ]
    avgs = {
        i: sum(evals)/len(evals)
        for i, evals in enumerate(score_evaluations)
    }

    # return the p value and the sizes that has the highest average.
    return {
        'p': f_oneway(*score_evaluations).pvalue,
        'bestsizes': sizes2compare[max(avgs, key=avgs.get)]
    }

def check_constant_baseline(I, repeats=100, ns=None, rand=None):
    '''
    Uses one-way ANOVA to statistally test the hypothesis of a constant baseline.
    For each value n:ns we compare balanced clusterings with n^0.25,n^0.5 and
    n^0.75 equal-sized clusters.

    Parameters
    -------
    I : Score
        The validation index that is tested
    repeats : int
        The number of clusterings generated from each clustersizes distribution.
    ns: list
        A list containing the numbers of vertices for which the test is performed.
    rand : numpy.random.RandomState
        Used for making the generation of clusterings reproducable.

    Returns
    -------
    dict
        Keys represent the values for n and the values correspond the confidence
        at which the constant baseline hypothesis is rejected by the ANOVA test.
    '''
    if ns == None:
        ns = range(50, 1001, 50)

    n2ks = {
        n: [int(n**0.25),int(n**0.5),int(n**0.75)]
        for n in ns
    }
    n2sizes = {
        n: [
            Clustering.BalancedSizes(n, k)
            for k in ks
        ]
        for n,ks in n2ks.items()
    }
    n2gt = {
        n: Clustering.BalancedClustering(n, int(n**0.5))
        for n in ns
    }

    return {
        n: bias_anova(I, n2gt[n], n2sizes[n], repeats, rand)['p']
        for n in ns
    }
