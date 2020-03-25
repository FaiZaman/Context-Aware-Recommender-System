import random as rand
import pandas as pd
import math
import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from Preprocessor import fetch_data
from Recommender import get_recommendations, get_user_ratings

warnings.filterwarnings("ignore", category=RuntimeWarning) 

dataframe, user_id_list, item_id_list = fetch_data()
contexts = ['urban', 'mountains', 'countryside', 'coastline']


# calculates the mean absolute error between the recommendations and actual ratings
def MAE(main_dataframe, R, N, threshold):

    train_data, test_data = split_data(main_dataframe)

    predicted_ratings = []
    true_ratings = []

    # iterate through each user and each context
    for user_id in user_id_list:
        for context in contexts:
            
            # calculate recommendations for each one
            original_recommendations, filtered_recommendations, user_mean_rating =\
                get_recommendations(user_id, train_data, context, R, N, threshold)
            recommendations = filter_nan(original_recommendations)

            # compare training data's recommendation predicted ratings to true test set ratings
            for index, row in test_data.iterrows():
                if row['UserID'] == str(user_id) and row['landscape'] == context:
                    
                    item_id = int(row['ItemID'])
                    if item_id in recommendations:
                        predicted_rating = recommendations[item_id]
                        true_rating = row['Rating']

                        predicted_ratings.append(predicted_rating)
                        true_ratings.append(true_rating)

    error = mean_absolute_error(predicted_ratings, true_ratings)

    return error


# splits the data into training and testing sets
def split_data(main_dataframe):

    train_test_size = 0.8   # ratio of data to be training data

    train_set, test_set = train_test_split(main_dataframe, train_size=train_test_size)
    train_data = train_set.sort_values('UserID')
    test_data = test_set.sort_values('UserID')
    
    return train_data, test_data


# chooses a random test user
def select_test_user():

    random_user_id = rand.choice(user_id_list)
    return random_user_id


# evaluates whether the RS accurately predicted whether the recommendations would be used
def precision_recall(main_dataframe, R, N, threshold, is_precision):

    train_data, test_data = split_data(main_dataframe)
    user_item_list = []

    while user_item_list == []: # at least one rating in test set by test user

        test_user_id = select_test_user()
        test_user_ratings = get_user_ratings(test_user_id, test_data)
        user_item_list = test_user_ratings['ItemID'].tolist()
        user_item_list.sort()
    
    # initialises
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for context in contexts:

        # predict a set of items user will like/rate
        original_recommendations, filtered_recommendations, mean =\
            get_recommendations(test_user_id, train_data, context, R, N, threshold)
        recommendations = filter_nan(original_recommendations)

        # check test set for each recommendation    
        for item_id, predicted_rating in recommendations.items():
            if str(item_id) in user_item_list:

                predicted_binary_rating = convert_rating_to_binary(mean, predicted_rating)
                true_rating_row = test_user_ratings[test_user_ratings['ItemID'] == str(item_id)]
                true_rating = true_rating_row['Rating'].iloc[0]

                true_binary_rating = convert_rating_to_binary(mean, true_rating)
                true_positives, false_positives, false_negatives =\
                    assign_outcomes(predicted_binary_rating, true_binary_rating,\
                                    true_positives, false_positives, false_negatives)

    if is_precision:

        precision = calculate_precision(true_positives, false_positives)
        return precision

    else:
        
        recall = calculate_recall(true_positives, false_negatives)
        return recall


# returns precision TP/TP + FP
def calculate_precision(true_positives, false_positives):

    if true_positives == 0 and false_positives == 0:
        return 0
    precision = true_positives / (true_positives + false_positives)
    return precision


# returns recall TP/TP + FN
def calculate_recall(true_positives, false_negatives):

    if true_positives == 0 and false_negatives == 0:
        return 0
    recall = true_positives / (true_positives + false_negatives)
    return recall


# converts 1-5 rating to positive or negative for precision and recall
def convert_rating_to_binary(user_mean_rating, rating):

    if rating < user_mean_rating:
        return 0
    else:
        return 1


# assign true positives, false positives, and false negatives based on predicted & true binary ratings
def assign_outcomes(predicted_binary_rating, true_binary_rating, TPs, FPs, FNs):

    if predicted_binary_rating == 1 and true_binary_rating == 1:
        TPs += 1
    elif predicted_binary_rating == 1 and true_binary_rating == 0:
        FPs += 1
    elif predicted_binary_rating == 0 and true_binary_rating == 1:
        FNs += 1
    
    return TPs, FPs, FNs


def filter_nan(recommendations):

    recommendations_copy = recommendations.copy()
    for item_id, predicted_rating in recommendations_copy.items():
        if math.isnan(predicted_rating):
            del recommendations[item_id]

    return recommendations
