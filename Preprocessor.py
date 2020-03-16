import pandas as pd
import numpy as np

#main_dataframe.to_csv("dataset/in_car_music.csv")

# reading in data
main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
#music_category_dataframe = pd.read_csv("dataset/music_category.csv", index_col=False, delimiter=",", encoding="utf-8-sig")


def fetch_data():

    processed_main_dataframe, user_id_list = preprocess()
    item_id_list = get_item_id_list(processed_main_dataframe)

    return processed_main_dataframe, user_id_list, item_id_list


def get_user_id_list(dataframe):

    # get user IDs as list
    user_column = dataframe['UserID'].tolist()
    user_id_list = list(dict.fromkeys(user_column))

    return user_id_list


def get_item_id_list(dataframe):

    # get item IDs as list
    item_id_list = song_dataframe['id'].tolist()

    return item_id_list


# returns the vector of a all specific user's ratings 
def get_user_ratings_preprocessing(user_id):

    user_dataframe = main_dataframe[main_dataframe['UserID'] == user_id]
    user_ratings = user_dataframe[['UserID', 'ItemID', 'Rating', 'landscape']]

    return user_ratings


# preprocesses data
# if user has multiple ratings for one item, average them
def preprocess():

    filtered_main_dataframe = filter_context_info()
    user_id_list = get_user_id_list(filtered_main_dataframe)

    processed_main_dataframe = pd.DataFrame(columns=['UserID', 'ItemID', 'Rating', 'landscape'])

    # for each user's each item ratings, check if they rated that item multiple times
    for user_id in user_id_list:

        user_ratings = get_user_ratings_preprocessing(user_id)

        unique_rows = user_ratings.drop_duplicates('ItemID', keep=False)
        duplicate_rows = user_ratings[user_ratings.duplicated(['ItemID'])]
    
        user_item_column = duplicate_rows['ItemID'].tolist()
        user_item_id_list = list(dict.fromkeys(user_item_column))

        for item_id in user_item_id_list:

            duplicate_items = duplicate_rows[duplicate_rows['ItemID'] == item_id]
            
            landscape_list = duplicate_items['landscape']
            landscape = landscape_list.iloc[0]

            # choosing the first landscape we see
            for landscape_i in landscape_list:
                if type(landscape_i) != float:
                    landscape = landscape_i
                    break;

            average_rating = duplicate_items['Rating'].mean()

            processed_item_row = {
                'UserID': str(user_id),
                'ItemID': str(item_id),
                'Rating': average_rating,
                'landscape': landscape
            }

            processed_main_dataframe = processed_main_dataframe.append(unique_rows)
            processed_main_dataframe = processed_main_dataframe.append(processed_item_row, ignore_index=True)
    
    return processed_main_dataframe, user_id_list


def filter_context_info():

    filtered_dataframe = main_dataframe[main_dataframe['landscape'].apply(lambda x: isinstance(x, str))]

    return filtered_dataframe
