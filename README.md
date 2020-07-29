# README
All indices that are discussed in [the paper](https://arxiv.org/abs/1911.04773) (except SMI, which requires a lot of computation and is implemented by its original authors in Matlab) can be found in the list `Indices`. It can be obtained via

```python
from validation_indices import Indices
```

Other indices (e.g. other pair-counting indices and other normalizations of NMI) are also implemented. These can be found in the files `PairCountingIndices`,`InformationTheoreticIndices` respectively. Each index is a class that has (among others) a static function `score` that takes as input two clusterings. Clusterings can be provided in two forms

* either as a list where the i-th entry corresponds to the cluster-label (integer) of the i-th item,
* or as a list of lists where each inner-list contains the indices of all items in that cluster.

Hence, the clustering where the first two items are assigned to the first cluster and the third is assigned to another cluster can be represented as either `[0,0,1]` or `[[0,1],[2]]`.

In short, the following sample code computes the values of all indices for the two clusterings on three items, each with 2 clusters where the clusters of size 2 are not identical:

```python
from validation_indices import Indices
A = [0,0,1]
B = [[0,2],[1]]
{
    i.__name__: i.score(A,B)
    for i in Indices
}
```

The statistical test as described in the Appendix of [our paper](https://arxiv.org/abs/1911.04773) can be applied to an index (e.g. NMI in the example) in the following way:
```python
from validation_indices import NamedIndices
from validation_indices.ConstantBaselineTests import check_constant_baseline

# We apply the test to the Normalized Mutual Information index.
I = NamedIndices["NMI"]

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

check_constant_baseline(
    I        = I,
    n2ks     = n2ks,
    n2gtk    = n2gtk,
    repeats  = 500,
    aggregate= True)
```

To generate the figures showing the inconsistencies between the indices, simply run the file `InconsistencyVisualizations.py`. This can be done in the following way:
```python
from validation_indices.InconsistencyVisualizations import *
```

## Experiments with synthetic datasets

The module `rules_bruteforce` computes the minimal set of inconsistency triplets ('rules') that is shown in Figure 1 of the Supplementary material.

The inconsistency triplets can be found by running the file `bruteforce_minimal_basis.py`.

By running `check_minimum_coverage.py` we obtain a table that shows for each pair of indices, for which triplet this pair is inconsistent.

## Experiments with datasets

The module `datasets_experiments` performs the clustering experiments on datasets to show the inconsistencies among the validation indices.

The experiment is done in two steps:

* In the first step, we use the selected algorithms to cluster the selected datasets and compute the validation score for each validation index.

* In the second step, we compute the inconsistencies between the validation indices on these results.

More specifically, in the first step:

`parse_datasets.py` retrieves the datasets from [this repository](https://github.com/deric/clustering-benchmark/tree/master/src/main/resources/datasets/real-world). `clusterize.py` performs runs the clustering algorithms and `full_compare.py` computes the score for each validation index.

The remaining 3 files process these scores to summarize inconsistencies:

* `stats_realworld.py` computes the inconsistencies of the indices on the results of real-world data.
* `stats_realworld_iris.py` computes the inconsistencies of the indices on the iris dataset alone.
* `stats.py` computes the inconsistencies among all datasets.
