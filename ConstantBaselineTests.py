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
    gt : list or Clustering
        The ground truth clustering
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
            I.score(gt, Clustering.FromSizes(sizes).random_same_sizes(rand)) * (-1 if I.isdistance else 1)
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
        The ground truth clustering
    sizes2compare : list of lists
        A list containing the clustersizes that we want to compare. Each
        clustersizes should be represented by a list of integers summing len(gt).
    repeats : int
        The number of clusterings generated from each clustersizes distribution.
    rand : numpy.random.RandomState
        Used for making the generation of clusterings reproducable.
    '''
    score_evaluations = [
        [
            I.score(gt, Clustering.FromSizes(sizes).random_same_sizes(rand)) * (-1 if I.isdistance else 1)
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
        'bestsizes_index': max(avgs, key=avgs.get),
        'bestsizes': sizes2compare[max(avgs, key=avgs.get)]
    }

def check_constant_baseline(I, repeats=500, aggregate=True, n2gtk=None, n2ks=None, rand=None):
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
    aggregate : bool
        If True, we combine the results for the various n into one statistical
        test using Fisher's method.
    n2gtk: dict
        A dictionary from n to the number of ground truth clusters
    n2ks: dict
        A dictionary from n to a list of the number of clusters for each of the candidates.
    rand : numpy.random.RandomState
        Used for making the generation of clusterings reproducable.

    Returns
    -------
    dict
        If aggregate==True, we return a dictionary with the keys "constant baseline p"
        and "best candidate index". Otherwise, that maps n to the result of the
        statistical test for that n (also represented as a dictionary with these two keys).
        The p-values correspond to the condidence level at which the constant
        baseline hypothesis is rejected by the ANOVA test.
    '''
    if aggregate:
        # Better get the import error before performing the whole experiment
        from scipy.stats import combine_pvalues

    if n2gtk == None and n2ks == None:
        # Choose n=50,100,150,...,1000
        ns = range(50, 1001, 50)
        # For each n, we consider balanced cluster sizes with k=sqrt(n) clusters.
        n2gtk = {
            n: int(n**0.5)
            for n in ns
        }
        # For each n, we consider candidates with balanced cluster sizes with
        # k1=n^0.25, k2=n^0.5, k3=n^0.75.
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
        n: Clustering.BalancedClustering(n, k)
        for n,k in n2gtk.items()
    }

    n2results = {
        n: bias_anova(I, n2gt[n], n2sizes[n], repeats, rand)
        for n in n2gtk.keys()
    }
    if not aggregate:
        return {
            n: {
                'constant baseline p': results['p'],
                'best candidate index': results['bestsizes_index']
            }
            for n, results in n2results.items()
        }
    else:
        # Use Fisher's method to combine the p-values.
        counts = {}
        ps = []
        for n,result in n2results.items():
            ps.append(result['p'])
            best = result['bestsizes_index']
            if not best in counts:
                counts[best] = 0
            counts[best] += 1
        return {
            'constant baseline p': combine_pvalues(ps)[1],
            'best candidate index': max(counts, key=counts.get)
        }
