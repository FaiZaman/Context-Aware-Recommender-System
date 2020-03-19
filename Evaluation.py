import random as rand
import pandas as pd
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
        print(user_id)
        for context in contexts:
            
            # calculate recommendations for each one
            recommendations, user_mean_rating =\
                get_recommendations(user_id, train_data, context, R, N, threshold)

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

    test_user_id = select_test_user()
    train_data, test_data = split_data(main_dataframe)

    # for comparison
    test_user_ratings = get_user_ratings(test_user_id, test_data)
    user_item_list = test_user_ratings['ItemID'].tolist()
    user_item_list.sort()

    # initialises
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for context in contexts:

        # predict a set of items user will like/rate
        recommendations, mean = get_recommendations(test_user_id, train_data, context, R, N, threshold)
        print(recommendations)
        print(user_item_list)

        # check test set for each recommendation
        if user_item_list != []:
            
            for item_id, predicted_raing in recommendations.items():
                
                if str(item_id) in user_item_list:  # true positive
                    print(item_id, "True Positive")
                    true_positives += 1

                else:   # false positive
                    print(item_id, "False Positive")
                    false_positives += 1
            
            for item_id in user_item_list:

                if int(item_id) not in recommendations:
                    false_negatives += 1

    if is_precision:
        print(true_positives, false_positives)
        precision = calculate_precision(true_positives, false_positives)
        return precision

    else:
        print(true_positives, false_negatives)
        recall = calculate_recall(true_positives, false_negatives)
        print(recall)
        return recall


# returns precision TP/TP + FP
def calculate_precision(true_positives, false_positives):

    precision = true_positives / (true_positives + false_positives)
    return precision


# returns recall TP/TP + FN
def calculate_recall(true_positives, false_negatives):

    recall = true_positives / (true_positives + false_negatives)
    return recall


precision_recall(dataframe, R=10, N=17, threshold=0.1, is_precision=False)
