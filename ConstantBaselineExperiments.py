from validation_indices import Clustering,NamedIndices
import matplotlib.pyplot as plt
import numpy as np
n=924
sizes=[50, 44, 38, 27, 20, 15, 13, 13, 12, 11, 10, 9, 9, 9, 7, 7, 7, 6, 6, 6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
# Add singleton clusters
sizes+=[1]*(n-sum(sizes))
A=Clustering.FromSizes(sizes)

repeats = 200
ks = [
    2,
    8,
    32,
    128,
    512
]
k2sample = {
    k: [
        Clustering.BalancedClustering(n=n,k=k).random_same_sizes()
        for _ in range(repeats)
    ]
    for k in ks
}
ss=[1,2,8,16,int(n/32)]
s2sample = {
    s:[
        Clustering.FromSizes([s]*31+[n-31*s]).random_same_sizes()
        for _ in range(repeats)
    ]
    for s in ss
}

def analyse_sample(sample):
    p05,p95 = np.percentile(sample,[5,95])
    avg = sum(sample)/len(sample)
    return [avg,p05,p95]

name_I = [
    ('NMI',NamedIndices['NMI']),
    ('NMI$_\\max$',NamedIndices['MaxNMI']),
    ('FNMI',NamedIndices['FNMI']),
    ('AMI',NamedIndices['AMI']),
    ('VI',NamedIndices['VI']),
    ('FMeasure',NamedIndices['FM']),
    ('BCubed',NamedIndices['BCubed']),
    ('R',NamedIndices['Rand']),
    ('AR',NamedIndices['ARI']),
    ('J',NamedIndices['Jaccard']),
    ('W',NamedIndices['Wallace']),
    ('D',NamedIndices['Dice']),
    ('S&S',NamedIndices['S&S1']),
    ('CC',NamedIndices['CC']),
    ('CD',NamedIndices['CD']),
]


def k_experiment(save=False):
    fig, axs = plt.subplots(5, 3, figsize=(15, 25), sharex=True)
    for (name, I), ax in zip(name_I, axs.flatten()):
        k2result = {
            k: analyse_sample([
                I.score(A, B)
                for B in sample
            ])
            for k, sample in k2sample.items()
        }
        ax.plot(ks, [
            k2result[k][0]
            for k in ks
        ], label=name)
        ax.fill_between(
            ks,
            [k2result[k][1] for k in ks],
            [k2result[k][2] for k in ks],
            alpha=0.2)
        ax.legend()
    for ax in axs[4, :]:
        ax.set_xlabel('Number of clusters')
    if save:
        plt.savefig('k_experiment.pdf', bbox_inches='tight')
    return ax


def s_experiment(save=False):
    fig, axs = plt.subplots(5, 3, figsize=(15, 25), sharex=True)
    for (name, I), ax in zip(name_I, axs.flatten()):
        s2result = {
            s: analyse_sample([
                I.score(A, B)
                for B in sample
            ])
            for s, sample in s2sample.items()
        }
        ax.plot(ss, [
            s2result[s][0]
            for s in ss
        ], label=name)
        ax.fill_between(
            ss,
            [s2result[s][1] for s in ss],
            [s2result[s][2] for s in ss],
            alpha=0.2)
        ax.legend()
    for ax in axs[4, :]:
        ax.set_xlabel('Small cluster size')
    if save:
        plt.savefig('s_experiment.pdf', bbox_inches='tight')
    return ax

k_experiment(save=True)
s_experiment(save=True)