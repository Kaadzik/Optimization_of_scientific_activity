import pandas as pd

default_path = 'Datasets/dataset_1.xlsx'
author_label = 'author_id'
publication_label = 'publ_id'
author_slot_label = 'author_slot'
publication_slot_label = 'publ_slot'
publication_value_label = 'publ_points'


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
    N_value = data[author_label].nunique()
    data.replace("", float("NaN"), inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    return data, N_value


def create_publication_list(data) -> list:
    publication_list = []
    for index, row in data.iterrows():
        publication_list.append(
            Publication(int(row[publication_label]), row[author_label], row[publication_slot_label], row[publication_value_label],
                        False if round(row[publication_value_label]/row[publication_slot_label]) > 100 else True, 0))
    return publication_list


def create_author_list(publication_list: list, data) -> list:
    author_list = []
    current_author = 0
    for index, row in data.iterrows():
        if not author_list or author_list[current_author].author_id != row[author_label]:
            author_list.append(
                Author(row[author_label], [], row[author_slot_label]))
            if not (current_author == 0 and not author_list[current_author].publications):
                current_author += 1
        author_list[current_author].publications.append(publication_list[index])
        publication_list[index].author_order_number = current_author
    return author_list
