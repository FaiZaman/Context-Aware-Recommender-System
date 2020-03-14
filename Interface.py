import pandas as pd
import numpy as np
from Preprocessor import fetch_data
from Recommender import get_same_rated_items, compute_similarities, get_user_ratings, \
                        get_user_neighbourhood, compute_recommendations

N = 17  # neighbourhood size
R = 10  # number of recommendations to output

main_dataframe, user_id_list, item_id_list = fetch_data()
print("Welcome to the Music Recommender System! Please enter your user ID:")

def sign_in():

    # takes user ID as input explicitly and logs them in
    while True:
        try:
            user_id = int(input())
            break;
        except ValueError:
            print("Invalid format. Please enter an integer and try again.")
    
    return user_id


def validate_user(user_id):
    
    # verifies that given user ID is a valid user
    if user_id in user_id_list:
        return True
    return False


def display_recommendations(user_id):

    # display specificed user's personalised recommendations
    print("Welcome, User " + str(user_id) + "! Your recommendations are:\n")
    print(main_dataframe.head(10))

is_valid_id = False

while not is_valid_id:

    user_id = sign_in()
    is_valid_id = validate_user(user_id)

    if not is_valid_id:
        print("The user " + str(user_id) + " does not exist. Please try again:")

display_recommendations(user_id)
similarity_dict = compute_similarities(user_id)
neighbourhood = get_user_neighbourhood(similarity_dict, N)
compute_recommendations(user_id, neighbourhood, R)
