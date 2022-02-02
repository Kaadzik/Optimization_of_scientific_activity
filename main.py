import dataset_import as data
import genetic_algorithm as gen
import linear_programming as lin

# path = 'Datasets/dataset_1.xlsx'
path = 'Datasets/dataset_2.xlsx'

dataset, N_value = data.read_datasheet(path)
publications_list = data.create_publication_list(dataset)
authors_list = data.create_author_list(publications_list, dataset)

print(gen.genetic_algorithm(N_value, publications_list, authors_list).get_value())
print(lin.linear_programming(N_value, publications_list, authors_list).get_value())
