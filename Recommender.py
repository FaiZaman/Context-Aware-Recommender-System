import pandas as pd
import numpy as np
import itertools
from Preprocessor import fetch_data

main_dataframe, user_id_list = fetch_data()

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
