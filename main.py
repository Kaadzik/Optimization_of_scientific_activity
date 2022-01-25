import dataset_import as data
import genetic_algorithm as gen

dataset, N_value = data.read_datasheet()
publications_list = data.create_publication_list(dataset)
authors_list = data.create_author_list(publications_list, dataset)

for i in range (20):
    print(gen.genetic_algorithm(N_value, publications_list, authors_list).get_value())
