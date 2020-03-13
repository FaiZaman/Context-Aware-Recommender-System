import pandas as pd
import numpy as np
import itertools

# reading in data
main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
music_category_dataframe = pd.read_csv("dataset/music_category.csv", index_col=False, delimiter=",", encoding="utf-8-sig")

# get user IDs as list
user_column = main_dataframe['UserID'].tolist()
user_id_list = list(dict.fromkeys(user_column))


# returns the vector of a all specific user's ratings 
def get_user_ratings(user_id):

    user_dataframe = main_dataframe[main_dataframe['UserID'] == 1001]
    user_ratings = user_dataframe[['ItemID', 'Rating']]

    return user_ratings


# returns the items with a rating by both users for similarity calculation
def get_same_rated_items(user_ratings_1, user_ratings_2):

    same_rated_items = []

    return same_rated_items


# compares all users to each other
def compute_similarities():

    for user_i, user_j in itertools.combinations(user_id_list, 2):
        
        print(user_i, user_j)
        user_ratings_i = get_user_ratings(user_i)
        user_ratings_j = get_user_ratings(user_j)

        same_rated_items = get_same_rated_items(user_ratings_i, user_ratings_j)
        print(user_ratings_i)
        print(user_ratings_j)   # the same? todo
        break;
