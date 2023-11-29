import pandas as pd
import numpy as np
import os

from src.data.utils import (
    read_data,
    treat_text,
    process_food_element,
    save_as_pickle,
    get_response_dataframe_from_dict_with_categs
)

from src.data.read_human_processed_information import \
    statistics_of_response_var

def get_food_information(test_food):
    global food_survey_food, input_food, nutrient_info,\
        fndds_ingredient_nutrient_value, food
    food_survey_food[food_survey_food.fdc_id == test_food]

    ingredients = input_food[input_food.fdc_id == test_food].sort_values(
        'seq_num')
    codes = ingredients.sr_code.unique()

    nutrient_info_reduced = \
    nutrient_info[nutrient_info.nutrient_nbr_int.notna()][
        ['name', 'unit_name', 'nutrient_nbr_int']]
    specific_nutrient_val = fndds_ingredient_nutrient_value \
        [fndds_ingredient_nutrient_value['ingredient code'].isin(codes)] \
        .drop_duplicates(['ingredient code', 'Nutrient code']) \
        .merge(
        nutrient_info_reduced,
        left_on='Nutrient code',
        right_on='nutrient_nbr_int') \
        [['ingredient code', 'Nutrient code', 'Nutrient value', 'name',
          'unit_name']]
    specific_nutrient_val = specific_nutrient_val[
        specific_nutrient_val['Nutrient value'] != 0] \
        .sort_values(['Nutrient code', 'Nutrient value']).reset_index(
        drop=True) \
        .drop_duplicates(['ingredient code', 'Nutrient code'])

    missing_codes = list(
        set(codes) - set(specific_nutrient_val['ingredient code'].unique()))

    missing_ingredients = ingredients[ingredients.sr_code.isin(missing_codes)]

    nutrient_info_reduced = \
    nutrient_info[nutrient_info.nutrient_nbr_int.notna()][
        ['name', 'unit_name', 'nutrient_nbr_int']]
    specific_nutrient_val = fndds_ingredient_nutrient_value \
        [fndds_ingredient_nutrient_value['ingredient code'].isin(codes)] \
        .drop_duplicates(['ingredient code', 'Nutrient code']) \
        .merge(
        nutrient_info_reduced,
        left_on='Nutrient code',
        right_on='nutrient_nbr_int') \
        [['ingredient code', 'Nutrient code', 'Nutrient value', 'name',
          'unit_name']]
    specific_nutrient_val = specific_nutrient_val[
        specific_nutrient_val['Nutrient value'] != 0] \
        .sort_values(['ingredient code', 'Nutrient code', 'Nutrient value']) \
        .reset_index(drop=True) \
        .drop_duplicates(['ingredient code', 'Nutrient code'])

    ingredients.index = ingredients.index.map(str)
    missing_ingredients.index = missing_ingredients.index.map(str)
    specific_nutrient_val.index = specific_nutrient_val.index.map(str)

    return ingredients, missing_ingredients, specific_nutrient_val


def get_unique_nutrition_names(info):
    info = pd.DataFrame(info)
    return list(info.name.unique())

if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__))
    general_path = os.path.join(file_path, '..', '../')
    data_raw_path = os.path.join(general_path, 'data', 'raw')
    data_interim_path = os.path.join(general_path, 'data', 'interim')
    data_interim_filename = os.path.join(data_interim_path, 'interim.csv')


    data_path = os.path.join(data_raw_path, 'FoodData_Central_csv_2023-04-20')
    data_dict_path = os.path.join(general_path, 'data', 'data_dict')
    r_dict_path = os.path.join(data_dict_path, 'r_dict.pkl')
    x_dict_path = os.path.join(data_dict_path, 'x_dict.pkl')
    s_dict_path = os.path.join(data_dict_path, 's_dict.pkl')

    # Raw data
    food = read_data(f'{data_path}/food.csv')
    survey_fndds_food = read_data(f'{data_path}/survey_fndds_food.csv')
    nutrient_data = read_data(f'{data_path}/food_nutrient.csv')
    nutrient_info = read_data(f'{data_path}/nutrient.csv')
    input_food = read_data(f'{data_path}/input_food.csv')
    component = read_data(f'{data_path}/food_component.csv')
    category = read_data(f'{data_path}/wweia_food_category.csv')
    fndds_derivation = read_data(f'{data_path}/fndds_derivation.csv')
    fndds_ingredient_nutrient_value = read_data(
        f'{data_path}/fndds_ingredient_nutrient_value.csv'
    )

    # Processed data (target dataset)
    response_r = read_data(r_dict_path)
    response_r = get_response_dataframe_from_dict_with_categs(response_r)
    #response_s = read_data(s_dict_path)
    nutrient_info.loc[
        nutrient_info.nutrient_nbr.notna(), 'nutrient_nbr_int'
    ] = nutrient_info.loc[
        nutrient_info.nutrient_nbr.notna()
    ].nutrient_nbr.astype('int')

    fndss_dt = food.data_type == 'survey_fndds_food'
    relevant_list = ['description', 'fdc_id', 'food_category_id', 'publication_date']
    food_survey_food = survey_fndds_food.merge(food[fndss_dt][relevant_list], on='fdc_id', how='left')
    food_survey_food = food_survey_food \
        .merge(category, how='left', left_on='wweia_category_code', right_on='wweia_food_category') \
        .drop(['wweia_category_code', 'food_category_id', 'start_date', 'end_date', 'publication_date'], axis=1)

    relevant_indexes = statistics_of_response_var(response_r)['unique_food_considered']
    food_ingredient_nutrition_info = {}
    for food in relevant_indexes:
        food_ingredient_nutrition_info[food] = {}
        ingredients, missing_ingredients, nutrition = get_food_information(food)
        food_ingredient_nutrition_info[food]['ingredients'] = ingredients[['sr_code', 'sr_description']].to_dict()
        food_ingredient_nutrition_info[food]['missing_ingredients'] = missing_ingredients.sr_code.to_dict()
        food_ingredient_nutrition_info[food]['nutrition'] = nutrition.to_dict()
        food_ingredient_nutrition_info[food]['unique_ingredients_code'] = ingredients.sr_code.unique()
        food_ingredient_nutrition_info[food]['unique_ingredients'] = ingredients.sr_description.unique()
    food_ingredient_nutrition_info_processed = pd.DataFrame(food_ingredient_nutrition_info).T

    all_available_nutrients = sorted(
        list(
            set(
                food_ingredient_nutrition_info_processed.nutrition.apply(get_unique_nutrition_names).sum())
        )
    )
    saving_all_info = []
    for i in range(food_ingredient_nutrition_info_processed.shape[0]):
        test = pd.DataFrame(
            food_ingredient_nutrition_info_processed.nutrition.iloc[i])
        test_idx = food_ingredient_nutrition_info_processed.iloc[i].name
        missing_nutrients = set(all_available_nutrients) - set(
            test.name.to_list())
        test_n = test.groupby(['name'])[['Nutrient value']].sum()
        test_mn = pd.DataFrame(missing_nutrients, columns=['name'])
        test_mn['Nutrient value'] = np.nan
        test_mn.set_index('name', inplace=True)
        test = pd.concat([test_n, test_mn]).sort_index().T
        test.index = [test_idx]
        saving_all_info.append(test)
    saving_all_info_df = pd.concat(saving_all_info).reset_index().rename(
        columns={'index': 'fdc_id'})
    final_dataset = response_r.merge(
        saving_all_info_df, on='fdc_id', how='inner').merge(
        saving_all_info_df, left_on='fdc_id_to', right_on='fdc_id', how='inner'
    )
    final_dataset.to_csv(data_interim_filename)
