import pandas as pd
import numpy as np

from src.data.utils import (
    get_general_path,
    join_paths,
    read_data,
    get_response_dataframe_from_dict_with_categs,
)

from src.data.read_human_processed_information import \
    statistics_of_response_var


def get_food_information(test_food):
    global food_survey_food, input_food, nutrient_info
    global fndds_ingredient_nutrient_value, food

    # Check the corresponding food survey food with the index
    food_description = food_survey_food[
        food_survey_food.fdc_id == test_food
        ].description.values[0]

    # Get the associated ingredients from the relation of the test food
    # in the input_food table
    ingredients = input_food[input_food.fdc_id == test_food].sort_values(
        'seq_num')

    # Keep the ingredients codes
    codes = ingredients.sr_code.unique()

    # Get the nutrient information (units and nutrient numbers)
    nutrient_info_reduced = nutrient_info[
        nutrient_info.nutrient_nbr_int.notna()
    ][['name', 'unit_name', 'nutrient_nbr_int']]

    # Get the nutrients values for each ingredient.
    specific_nutrient_val = fndds_ingredient_nutrient_value[
        fndds_ingredient_nutrient_value['ingredient code'].isin(codes)
    ].drop_duplicates(
        ['ingredient code', 'Nutrient code']
    ).merge(
        nutrient_info_reduced,
        left_on='Nutrient code',
        right_on='nutrient_nbr_int'
    )[
        ['ingredient code',
         'Nutrient code',
         'Nutrient value',
         'name',
         'unit_name'
         ]
    ]
    specific_nutrient_val = specific_nutrient_val[
        specific_nutrient_val['Nutrient value'] != 0
        ].sort_values(
        ['Nutrient code', 'Nutrient value']
    ).reset_index(
        drop=True
    ).drop_duplicates(
        ['ingredient code', 'Nutrient code']
    )
    missing_codes = list(
        set(codes) - set(specific_nutrient_val['ingredient code'].unique())
    )

    missing_ingredients = ingredients[
        ingredients.sr_code.isin(missing_codes)
    ]

    nutrient_info_reduced = \
        nutrient_info[nutrient_info.nutrient_nbr_int.notna()][
            ['name', 'unit_name', 'nutrient_nbr_int']]
    specific_nutrient_val = fndds_ingredient_nutrient_value[
        fndds_ingredient_nutrient_value['ingredient code'].isin(codes)
    ].drop_duplicates(
        ['ingredient code', 'Nutrient code']
    ).merge(
        nutrient_info_reduced,
        left_on='Nutrient code',
        right_on='nutrient_nbr_int'
    )[
        ['ingredient code',
         'Nutrient code',
         'Nutrient value',
         'name',
         'unit_name']
    ]
    specific_nutrient_val = specific_nutrient_val[
        specific_nutrient_val['Nutrient value'] != 0
    ].sort_values(
        ['ingredient code', 'Nutrient code', 'Nutrient value']
    ).reset_index(
        drop=True
    ).drop_duplicates(
        ['ingredient code', 'Nutrient code']
    )

    ingredients.index = ingredients.index.map(str)
    missing_ingredients.index = missing_ingredients.index.map(str)
    specific_nutrient_val.index = specific_nutrient_val.index.map(str)

    result_tuple = (
        ingredients,
        missing_ingredients,
        specific_nutrient_val,
        food_description
    )
    return result_tuple


def get_unique_nutrition_names(info):
    info = pd.DataFrame(info)
    return list(info.name.unique())


if __name__ == "__main__":
    general_path = get_general_path()
    data_raw_path = join_paths(general_path, 'data', 'raw')
    data_interim_path = join_paths(general_path, 'data', 'interim')
    data_interim_food_ingredients = join_paths(
        data_interim_path, 'interim_food_ingredients.csv'
    )
    nutrient_unit_dict_path = join_paths(
        data_interim_path, 'nutrient_unit_dict.csv'
    )
    data_interim_filename = join_paths(data_interim_path, 'interim.csv')
    data_interim_filename_p = join_paths(data_interim_path, 'interim.parquet')

    data_path = join_paths(data_raw_path, 'FoodData_Central_csv_2023-04-20')
    data_dict_path = join_paths(general_path, 'data', 'data_dict')
    r_dict_path = join_paths(data_dict_path, 'r_dict.pkl')
    x_dict_path = join_paths(data_dict_path, 'x_dict.pkl')
    s_dict_path = join_paths(data_dict_path, 's_dict.pkl')

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
    # response_s = read_data(s_dict_path)

    # Make a simple clean-up
    nutrient_info.loc[
        nutrient_info.nutrient_nbr.notna(), 'nutrient_nbr_int'
    ] = nutrient_info.loc[
        nutrient_info.nutrient_nbr.notna()
    ].nutrient_nbr.astype('int')

    # Select only the survey_fndds_food category and the relevant columns
    # We want to know to which category they really belong to.
    fndss_dt = food.data_type == 'survey_fndds_food'
    relevant_list = [
        'description',
        'fdc_id',
        'food_category_id',
        'publication_date'
    ]
    food_survey_food = survey_fndds_food.merge(
        food[fndss_dt][relevant_list], on='fdc_id', how='left'
    )
    drop_cols = [
        'wweia_category_code',
        'food_category_id',
        'start_date',
        'end_date',
        'publication_date'
    ]

    food_survey_food = food_survey_food.merge(
        category,
        how='left',
        left_on='wweia_category_code',
        right_on='wweia_food_category'
    ).drop(drop_cols, axis=1)

    # Each food dictionary made by the team has already considered a quite
    # large sample of foods considered, we will use that to obtain the property
    # of each food

    relevant_indexes = statistics_of_response_var(
        response_r
    )['unique_food_considered']

    food_ingredient_nutrition_info = {}
    # Now we get the ingredient list for each food, and the nutritional
    # information as well!
    for food in relevant_indexes:
        food_ingredient_nutrition_info[food] = {}
        ingr, miss_ingr, nutrition, descr = get_food_information(food)
        food_ingredient_nutrition_info[food]['ingredients'] = ingr[
            ['sr_code', 'sr_description']
        ].to_dict()
        food_ingredient_nutrition_info[food]['missing_ingredients'] = (
            miss_ingr.sr_code.to_dict()
        )
        food_ingredient_nutrition_info[food]['nutrition'] = nutrition.to_dict()
        food_ingredient_nutrition_info[food]['unique_ingredients_code'] = (
            ingr.sr_code.unique()
        )
        food_ingredient_nutrition_info[food]['unique_ingredients'] = (
            ingr.sr_description.unique()
        )
        food_ingredient_nutrition_info[food]['description'] = descr

    food_ingredient_nutrition_info_processed = pd.DataFrame(
        food_ingredient_nutrition_info
    ).T

    all_available_nutrients = sorted(
        list(
            set(
                food_ingredient_nutrition_info_processed.nutrition.apply(
                    get_unique_nutrition_names
                ).sum()
            )
        )
    )
    product_all_info = []
    unit_dictionary_list = []
    # Now each for each food in each ingredient we find, we are make the union
    # (by adding) the nutrient value name.
    for i in range(food_ingredient_nutrition_info_processed.shape[0]):
        nutrients_from_ingredients = pd.DataFrame(
            food_ingredient_nutrition_info_processed.nutrition.iloc[i])
        # Save the information to make the unit dictonary
        unit_dictionary_list.append(
            nutrients_from_ingredients[['name', 'unit_name']]
        )
        # Get the index of food product
        food_index = food_ingredient_nutrition_info_processed.iloc[i].name

        # Get the missing nutrients
        missing_nutrients = set(all_available_nutrients) - set(
            nutrients_from_ingredients.name.to_list())

        # Sum the nutrients of each ingredient to get the complete sum.
        nutrient_addition = nutrients_from_ingredients.groupby(['name'])[
            ['Nutrient value']].sum()

        missing_nutrients_df = pd.DataFrame(missing_nutrients,
                                            columns=['name'])
        missing_nutrients_df['Nutrient value'] = np.nan
        missing_nutrients_df.set_index('name', inplace=True)

        # Concat missing and available nutrients.
        all_nutrients_food = pd.concat(
            [nutrient_addition, missing_nutrients_df]
        ).sort_index().T

        all_nutrients_food.index = [food_index]

        # Get the list of ingredients corresponding to the food product.
        ind_finip = food_ingredient_nutrition_info_processed.iloc[i]
        # Obtain the ingredients
        food_ingredients = list(ind_finip.unique_ingredients)

        # Get the product description and the ingredients
        all_nutrients_food['product_description'] = ind_finip.description
        all_nutrients_food['ingredients'] = [food_ingredients]
        # Append the dataframe row
        product_all_info.append(all_nutrients_food)

    # Obtain the information of all the products.
    product_all_info_df = pd.concat(product_all_info).reset_index().rename(
        columns={'index': 'fdc_id'})
    product_all_info_df.to_csv(data_interim_food_ingredients)

    # Generate the unit_dictionary
    unit_dictionary = pd.concat(unit_dictionary_list).groupby(
        "name"
    ).unit_name.apply(lambda x: list(set(x)))

    nutrient_unit_dictionary = pd.DataFrame(unit_dictionary)
    nutrient_unit_dictionary.to_csv(nutrient_unit_dict_path)

    final_dataset = response_r\
        .merge(product_all_info_df,
               on='fdc_id',
               how='inner')\
        .merge(product_all_info_df,
               left_on='fdc_id_to',
               right_on='fdc_id',
               how='inner')

    final_dataset.to_csv(data_interim_filename)
    final_dataset.to_parquet(data_interim_filename_p)
