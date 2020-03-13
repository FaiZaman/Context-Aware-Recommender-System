import pandas as pd
import numpy as np

# reading in data
main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
music_category_dataframe = pd.read_csv("dataset/music_category.csv", index_col=False, delimiter=",", encoding="utf-8-sig")

# get user IDs as list
user_column = main_dataframe['UserID'].tolist()
user_id_list = list(dict.fromkeys(user_column))

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
