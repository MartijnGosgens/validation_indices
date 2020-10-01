import os
from parse_realworld_datasets import parse_datasets
from apply_clustering_algorithms import apply_clustering_algorithms
from compute_indices import compute_indices
from count_agreements import print_latex_table_realworld,print_latex_mini_table_realworld,print_kmeans_preferences

parsed_dir = os.path.join(os.path.dirname(__file__), 'parsed/')
candidates_dir = os.path.join(os.path.dirname(__file__), 'candidates/')

for dir in [parsed_dir,candidates_dir]:
    if not os.path.isdir(dir):
        os.mkdir(dir)

# Obtain data
parse_datasets()
apply_clustering_algorithms()
compute_indices()

# Output the latex tables
print_latex_table_realworld()
print_latex_mini_table_realworld()
print_kmeans_preferences()
