import pandas as pd
import numpy as np
import sys
from os import system
from Preprocessor import fetch_data
from Recommender import get_same_rated_items, compute_similarities, get_user_ratings, \
                        get_user_neighbourhood, compute_recommendations, get_r_best_recommendations

# reading in data
song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")

N = 17  # neighbourhood size
R = 10  # number of recommendations to output
threshold = 0.1     # threshold for Filter PoF

main_dataframe, user_id_list, item_id_list = fetch_data()
system('cls')
print("Welcome to the Music Recommender System! Please enter your user ID:")


# displays menu when user signs in
def main_menu(user_id):

    print("====== Music Recommender System ======")
    print("Welcome, User " + str(user_id) + "!\n")
    print("Press G to generate recommendations")
    print("Press X to sign out of your account")
    print("Press Q to quit the Music Recommender System")
    
    while True:
        command = str(input())
        command = command.upper()
        if command == 'G' or command == 'X' or command == 'Q':
            break;
        else:
            print("Invalid command. Please try again.")
    
    if command == 'G':
        get_recommendations()
    elif command == 'X':
        sign_in()
    else:
        sys.exit()


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


# display specificed user's personalised recommendations
def display_recommendations(user_id, predicted_ratings):

    print("Your recommendations are:\n")

    # combine to display song titles and artists
    recommendation_template = pd.DataFrame(predicted_ratings, columns=['ItemID', 'Predicted Rating'])
    recommendations = pd.merge(song_dataframe, recommendation_template, on='ItemID', how='right')

    # remove unnecessary data
    recommendations = recommendations.drop('imageurl', 1); 
    recommendations = recommendations.drop('description', 1)
    recommendations = recommendations.drop('mp3url', 1); 
    recommendations = recommendations.drop('album', 1)
    recommendations = recommendations.drop('category_id', 1)

    # reorder columns and sort from most to least recommended
    recommendations = recommendations[['ItemID', 'title', 'artist', 'Predicted Rating']]
    recommendations = recommendations.sort_values(by=['Predicted Rating'], ascending=False)
    recommendations = recommendations.reset_index(drop=True)

    print(recommendations)


is_valid_id = False

while not is_valid_id:

    user_id = sign_in()
    is_valid_id = validate_user(user_id)

    if not is_valid_id:
        print("The user " + str(user_id) + " does not exist. Please try again:")


def get_recommendations():

     # get cosine similarities between users
    similarity_dict = compute_similarities(user_id)

    # get user's neighbourhood of size N
    neighbourhood = get_user_neighbourhood(similarity_dict, N)

    # get all predicted ratings for this user's unrated items
    predicted_ratings_dict = compute_recommendations(user_id, neighbourhood, threshold)

    # get the r highest predicted ratings to display
    r_predicted_ratings = get_r_best_recommendations(predicted_ratings_dict, R)

    display_recommendations(user_id, r_predicted_ratings)

main_menu(user_id)
#get_recommendations()
