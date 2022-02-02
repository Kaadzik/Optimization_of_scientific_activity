#Code by: Kamil Adamczyk
import dataset_import as data
import genetic_algorithm as gen
from time import time

path = '../Datasets/dataset_1.xlsx'
# path = '../Datasets/dataset_2.xlsx'

dataset, N_value = data.read_datasheet(path)
publications_list = data.create_publication_list(dataset)
authors_list = data.create_author_list(publications_list, dataset)

calculation_times = []
solution_values = []
repeats = 1000

for k in range(repeats):
    timer_start = time()
    solution_values.append(gen.genetic_algorithm(N_value, publications_list, authors_list).get_value())
    calculation_times.append(time() - timer_start)

print("Maximum value: ", max(solution_values))
print("Average value: ", sum(solution_values)/repeats)
print("Minimum value: ", min(solution_values))

print("Maximum calculation time: ", max(calculation_times))
print("Average calculation time: ", sum(calculation_times)/repeats)
print("Minimum calculation time: ", min(calculation_times))
