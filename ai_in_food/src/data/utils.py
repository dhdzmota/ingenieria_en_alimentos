import pandas as pd
import unidecode
import pickle
import os


def get_general_path():
    """
    Function to get the general path of this repo.
    """
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    return general_path


def join_paths(*p1):
    """
    Helper function to join paths
    """
    return os.path.join(*p1)


def read_data(path, **additional_kwargs):
    """
    Helper function to read data
    """
    if path.endswith('.csv'):
        data = pd.read_csv(path, **additional_kwargs)
    elif path.endswith('.parquet'):
        data = pd.read_parquet(path)
    elif path.endswith('.xlsx'):
        data = pd.read_excel(path, **additional_kwargs)
    elif path.endswith('.pkl'):
        with open(path, 'rb') as f:
            data = pickle.load(f)
    else:
        data = pd.read_csv(path)
    return data


def process_food_element(fe):
    """
    Function that takes a food element (short for fe, which is an index for the
    fdc_id), assumes a transformation to string, finally it cleans it.
    """
    fe = str(fe)
    fe = int(
        fe.replace('[', '')
        .replace(']', '')
        .split('.')[0]
        .strip()
    )
    return fe


def treat_text(text):
    """
    Custom function to clean text
    """
    text = text.replace(' ', '_')
    text = text.replace(',', '')
    text = text.replace('/', '_')
    text = text.replace('-', '_')
    text = text.replace(':', '_')
    text = text.lower()
    text = text.split('(')[0]
    text = unidecode.unidecode(text)
    return text


def save_as_pickle(what, where):
    """
    Helper function to save a file `what` into the path `where` as a pickle.
    """
    with open(where, 'wb') as file:
        pickle.dump(what, file)


def get_response_dataframe_from_dict_with_categs(
    dict_w_categs, not_consider_key=None
):
    dict_with_categs = dict_w_categs.copy()
    if not_consider_key:
        dict_with_categs.pop(not_consider_key)
    response_dataframes = []
    for key1 in dict_with_categs.keys():
        for key2 in dict_with_categs.keys():
            similarity = 0
            if key1 == key2:
                similarity = 1
            response_df = pd.DataFrame()
            initial_list = dict_with_categs[key1]
            comparison_list = dict_with_categs[key2]
            response_df['fdc_id'] = initial_list
            response_df['fdc_id_to'] = [comparison_list]*len(initial_list)
            response_df = response_df.explode('fdc_id_to')
            response_df['similar'] = similarity
            response_dataframes.append(response_df)
    response = pd.concat(response_dataframes).drop_duplicates()
    return response
