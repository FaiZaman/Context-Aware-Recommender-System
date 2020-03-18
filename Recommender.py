import pandas as pd
import numpy as np
import math
from scipy import spatial
from collections import Counter
from Preprocessor import fetch_data

main_dataframe, user_id_list, item_id_list = fetch_data()


def get_recommendations(user_id, ratings_dataframe, context, R, N, threshold):

     # get cosine similarities between users
    similarity_dict = compute_similarities(user_id, ratings_dataframe)

    # get user's neighbourhood of size N
    neighbourhood = get_user_neighbourhood(similarity_dict, N)

    # get all predicted ratings for this user's unrated items
    predicted_ratings_dict =\
        compute_recommendations(user_id, ratings_dataframe, context, neighbourhood, threshold)

    # get the r highest predicted ratings to display
    r_predicted_ratings = get_r_best_recommendations(predicted_ratings_dict, R)

    # gets the mean rating for thresholding and display recommendations
    user_mean_rating = get_user_mean_rating(user_id, ratings_dataframe)

    return r_predicted_ratings, user_mean_rating


# converts user's letter input to a word that can be searched for
def convert_context(context):

    if context == 'u':
        context = 'urban'
    elif context == 'm':
        context = 'mountains'
    elif context == 'cs':
        context = 'countryside'
    elif context == 'cl':
        context = 'coastline'
    
    return context


# returns the vector of a all specific user's ratings 
def get_user_ratings(user_id, ratings_dataframe):

    user_dataframe = ratings_dataframe[ratings_dataframe['UserID'] == str(user_id)]
    user_ratings = user_dataframe[['ItemID', 'Rating', 'landscape']]

    return user_ratings


# returns user's average rating for an item for thresholding
def get_user_mean_rating(user_id, ratings_dataframe):

    user_ratings = get_user_ratings(user_id, ratings_dataframe)
    ratings_list = user_ratings['Rating']
    user_mean_rating = ratings_list.mean()

    return user_mean_rating


# returns the rating user u gave to item i
def get_item_rating(user_id, ratings_dataframe, item_id, context):

    user_ratings = get_user_ratings(user_id, ratings_dataframe)
    item_rating = user_ratings[user_ratings['ItemID'] == str(item_id)]

    if not item_rating.empty:
        if item_rating['landscape'].iloc[0] == context:
            return item_rating

    return pd.DataFrame()


# returns R items not rated by the user
def get_unrated_items(user_id, ratings_dataframe):

    user_ratings = get_user_ratings(user_id, ratings_dataframe)
    user_item_list = user_ratings['ItemID'].tolist()

    # check item list against user ratings to find unrated items by user
    unrated_items = [item for item in item_id_list if str(item) not in user_item_list]
    unrated_items.sort()

    return unrated_items


# returns the items with a rating by both users for similarity calculation
def get_same_rated_items(user_ratings_i, user_ratings_j):

    item_list_i = user_ratings_i['ItemID'].tolist()
    item_list_j = user_ratings_j['ItemID'].tolist()
    same_rated_items = [item for item in item_list_i if item in item_list_j]

    return same_rated_items


# computes cosine similarity between two datasets
def compute_cosine_similarity(dataset_i, dataset_j):

    cosine = spatial.distance.cosine(dataset_i, dataset_j)
    cosine_similarity = 1 - cosine
    return cosine_similarity


# compares this user against all others
def compute_similarities(user_id, ratings_dataframe):

    similarity_dict = {}
    user_ratings = get_user_ratings(user_id, ratings_dataframe)

    # remove current user so not compared against itself
    filtered_user_id_list = user_id_list.copy()
    filtered_user_id_list.remove(user_id)

    for user_j in filtered_user_id_list:
        
        user_ratings_j = get_user_ratings(user_j, ratings_dataframe)
        same_rated_items = get_same_rated_items(user_ratings, user_ratings_j)

        # only compute for users with items in common
        if same_rated_items == []:
            continue

        # datasets for computing cosine similarity
        user_i_item_vector = []
        user_j_item_vector = []

        for item_id in same_rated_items:

            user_i_item_rating = user_ratings[user_ratings['ItemID'] == item_id]
            user_j_item_rating = user_ratings_j[user_ratings_j['ItemID'] == item_id]

            rating_i = user_i_item_rating['Rating'].iloc[0]
            rating_j = user_j_item_rating['Rating'].iloc[0]

            user_i_item_vector.append(rating_i)
            user_j_item_vector.append(rating_j)
            
        if user_i_item_vector != [0] and user_j_item_vector != [0]: # prevents NaNs
            cosine_similarity = compute_cosine_similarity(user_i_item_vector, user_j_item_vector)
            similarity_dict[user_j] = cosine_similarity
    
    return similarity_dict


# gets the N most similar users where N = neighbourhood size
def get_user_neighbourhood(similarity_dict, N):

    # choose the N entries with highest similarity and return them
    c = Counter(similarity_dict)
    neighbourhood = c.most_common(N)
    neighbourhood = dict(neighbourhood)

    return neighbourhood


# calculate r recommendations for unrated items for a user
def compute_recommendations(user_id, ratings_dataframe, context, neighbourhood, threshold):

    unrated_items = get_unrated_items(user_id, ratings_dataframe)
    predicted_ratings_dict = {}
    N = len(neighbourhood)

    for item_id in unrated_items:

        similarity_rating_sum = 0
        k = 0   # normalisation factor
        num_neighbours_rated = 0

        # apply summation formula by all users
        for neighbour_id, similarity in neighbourhood.items():

            # get rating for same item for current neighbour
            neighbour_item_rating = get_item_rating(neighbour_id, ratings_dataframe, item_id, context)

            if not neighbour_item_rating.empty:     #  if neighbour did rate item in specific context
                
                num_neighbours_rated += 1
                neighbour_item_rating = neighbour_item_rating['Rating'].iloc[0]

                similarity_rating = similarity * neighbour_item_rating
                similarity_rating_sum += similarity_rating
                k += abs(similarity)

        if k != 0:
            k = 1 / k
            predicted_rating = similarity_rating_sum * k
            
            if predicted_rating > 5:    # in case rating goes to 5.00001
                predicted_rating = 5.0

            # postfiltering and assignment
            predicted_rating = filter_pof(predicted_rating, num_neighbours_rated, N, threshold)
            predicted_ratings_dict[item_id] = predicted_rating

        else:
            # what rating to predict if none of neighbours rated this item?
            continue
    
    return predicted_ratings_dict


# sorts predicted ratings dict by item
def sort_dict(predicted_ratings):

    sorted_predicted_ratings = {}

    for key in sorted(predicted_ratings.keys()):
	    sorted_predicted_ratings[key] = predicted_ratings[key]

    return sorted_predicted_ratings


# returns the r items with highest predicted rating
def get_r_best_recommendations(predicted_ratings_dict, R):

    # choose R most similar entries, sort by item ID, and return them
    c = Counter(predicted_ratings_dict)
    r_predicted_ratings = dict(c.most_common(R))
    sorted_predicted_ratings = sort_dict(r_predicted_ratings)

    return sorted_predicted_ratings


# uses postfiltering to incorporate contexts into the recommendations
def filter_pof(predicted_rating, num_neighbours_rated, N, threshold):

    contextual_probability = num_neighbours_rated / N

    if contextual_probability > threshold:
        return predicted_rating
    return np.float64(0.0)
