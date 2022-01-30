import pandas as pd

# constants
default_path = 'Datasets/dataset_1.xlsx'


class Publication(object):
    def __init__(self, publ_id, author_id, unit_slot, point_value, is_less_than_100, author_order_number):
        self.publ_id = publ_id
        self.author_id = author_id
        self.unit_slot = unit_slot
        self.point_value = point_value
        self.is_less_than_100 = is_less_than_100
        self.author_order_number = author_order_number


class Author(object):
    def __init__(self, author_id, publications, overall_slot):
        self.author_id = author_id
        self.publications = publications
        self.overall_slot = overall_slot


def read_datasheet(source: str = default_path):
    data = pd.read_excel(source, usecols=[0, 1, 2, 3, 4])
    N_value = data['author_id'].nunique()
    data.replace("", float("NaN"), inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data, N_value


def create_publication_list(data) -> list:
    publication_list = []
    for index, row in data.iterrows():
        publication_list.append(
            Publication(int(row['publ_id']), row['author_id'], row['publ_slot'], row['publ_points'],
                        False if round(row['publ_points']/row['publ_slot']) > 100 else True, 0))
    return publication_list


def create_author_list(publication_list: list, data) -> list:
    author_list = []
    current_author = 0
    for index, row in data.iterrows():
        if not author_list or author_list[current_author].author_id != row['author_id']:
            author_list.append(
                Author(row['author_id'], [], row['author_slot']))
            if not (current_author == 0 and not author_list[current_author].publications):
                current_author += 1
        author_list[current_author].publications.append(publication_list[index])
        publication_list[index].author_order_number = current_author
    return author_list
