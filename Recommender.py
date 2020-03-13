import pandas as pd
import numpy as np

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

    pass


# compares all users to each other
def compute_similarities():

    for user_index in range(0, len(user_id_list)):
        
        user_1 = user_id_list[user_index]
        user_ratings_1 = get_user_ratings(user_1)

        for i in range(1, len(user_id_list)):

            user_i = user_id_list[user_index + i]
            user_ratings_i = get_user_ratings[user_i]

