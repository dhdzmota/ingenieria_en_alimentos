"""This scripts reads information that was analyzed `with scientist experience`
and process it into obtaining dictionaries with the corresponding information
"""
import pandas as pd
import numpy as np
import os

from src.data.utils import (
    read_data, treat_text, process_food_element, save_as_pickle
)


def r_to_dict(path):
    additional_info = {
        'sheet_name': 'Rev Daniel',
        'header': None,
    }
    raquel_info = read_data(path, **additional_info)
    raquel_info.loc[raquel_info.isna().sum(axis=1) != 4, 0] = np.nan
    raquel_info.loc[raquel_info.isna().sum(axis=1) == 4, 0] = \
        raquel_info[raquel_info.isna().sum(axis=1) == 4][1]
    raquel_info[0] = raquel_info[0].fillna(method='ffill')
    raquel_info = raquel_info[~(raquel_info.isna().sum(axis=1) > 2)]
    raquel_info[2] = raquel_info[2].apply(process_food_element)
    raquel_info = raquel_info.groupby(0)[2].apply(lambda x: list(x))
    raquel_info.index = pd.Series(raquel_info.index).apply(treat_text)
    raquel_dict = raquel_info.to_dict()
    return raquel_dict


def x_to_dict(path):
    additional_info = {'skiprows': 2}
    xiadeny_info = read_data(path, **additional_info)
    xiadeny_info = xiadeny_info.drop('Nombre categoría', axis=1)
    prev_col = None
    cols = []
    for col in xiadeny_info.columns:
        if 'Unnamed:' in col:
            col_dict = {
                prev_col: treat_text(prev_col) + '_', col: treat_text(prev_col)
            }
            xiadeny_info.rename(columns=col_dict, inplace=True)
            cols.append(treat_text(prev_col))
        prev_col = col
    xiadeny_dict = {}
    for col in cols:
        xiadeny_dict[col] = xiadeny_info[col].dropna().apply(
            process_food_element).tolist()
    return xiadeny_dict


def s_to_dict(path):
    additional_info = {'encoding': 'latin-1'}
    sam_info = read_data(path, **additional_info)
    sam_info.drop('Unnamed: 1', axis=1, inplace=True)
    column_dict = {
        col: treat_text(col) for col in sam_info.columns
        if 'Unnamed' not in col
    }
    sam_info.rename(columns=column_dict, inplace=True)
    sam_info = sam_info.drop(0).iloc[:-9]
    sam_info['categora_nueva'] = sam_info['categora_nueva'].fillna(
        method='ffill'
    )
    sam_info = sam_info[sam_info.isna().sum(axis=1) < 6]
    sam_info['fdc_ids'] = sam_info.fdc_ids.apply(
        lambda x: list(
            map(int, x.replace('[', '').replace(']', '').split(','))
        )
    )
    sam_info = sam_info.groupby('categora_nueva').fdc_ids.sum()
    sam_info.index = pd.Series(sam_info.index).apply(treat_text)
    sam_dict = sam_info.to_dict()
    return sam_dict


def statistics_of_response_var(response):
    results = {
        'target_proportion': response.similar.mean(),
        'instances_number': response.shape[0],
        'nunique_foods_considered': response.fdc_id.nunique(),
        'unique_food_considered': response.fdc_id.unique()
    }
    return results


if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_external_path = os.path.join(general_path, 'data', 'external')
    data_created_by_members = os.path.join(
        data_external_path, 'created_by_members'
    )
    path_r = os.path.join(
        data_created_by_members, 'Base de datos FAI RZR.xlsx'
    )
    path_x = os.path.join(
        data_created_by_members, 'Base de datos FAI XVR.xlsx'
    )
    path_s = os.path.join(
        data_created_by_members, 'depuración.csv'
    )

    data_dict_path = os.path.join(general_path, 'data', 'data_dict')
    r_dict_path = os.path.join(data_dict_path, 'r_dict.pkl')
    x_dict_path = os.path.join(data_dict_path, 'x_dict.pkl')
    s_dict_path = os.path.join(data_dict_path, 's_dict.pkl')

    r_dict = r_to_dict(path_r)
    x_dict = x_to_dict(path_x)
    s_dict = s_to_dict(path_s)

    save_as_pickle(r_dict, r_dict_path)
    save_as_pickle(x_dict, x_dict_path)
    save_as_pickle(s_dict, s_dict_path)
