import pandas as pd
import numpy as np
from Recommender import get_user_ratings

#main_dataframe.to_csv("dataset/in_car_music.csv")

def fetch_data():

    # reading in data
    main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
    #song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
    #music_category_dataframe = pd.read_csv("dataset/music_category.csv", index_col=False, delimiter=",", encoding="utf-8-sig")

    # get user IDs as list
    user_column = main_dataframe['UserID'].tolist()
    user_id_list = list(dict.fromkeys(user_column))

    return main_dataframe, user_id_list


# preprocesses data
# if user has multiple ratings for one item, average them
def preprocess():

    # for each user's each item ratings, check if they rated that item multiple times
    pass
