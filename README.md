# README

All indices that are discussed in the paper (except SMI, which requires a lot of computation and is implemented by its authors in Matlab) can be found in the list `Indices`. It can be obtained via

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



