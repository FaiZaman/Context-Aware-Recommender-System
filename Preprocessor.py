import pandas as pd
import numpy as np

#main_dataframe.to_csv("dataset/in_car_music.csv")

# reading in data
main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")


def fetch_data():

    processed_main_dataframe, user_id_list = preprocess()
    item_id_list = get_item_id_list(processed_main_dataframe)

    return processed_main_dataframe, user_id_list, item_id_list


def get_user_id_list(dataframe):

    # get user IDs as list
    user_column = dataframe['UserID'].tolist()
    user_id_list = list(dict.fromkeys(user_column))

    return user_id_list


def get_item_id_list(dataframe):

    # get item IDs as list
    item_id_list = song_dataframe['ItemID'].tolist()

    return item_id_list


# returns the vector of a all specific user's ratings 
def get_user_ratings_preprocessing(user_id, filtered_main_dataframe):

    user_dataframe = filtered_main_dataframe[filtered_main_dataframe['UserID'] == user_id]
    user_ratings = user_dataframe[['UserID', 'ItemID', 'Rating', 'landscape']]

    return user_ratings


# preprocesses data
# if user has multiple ratings for one item, average them
def preprocess():

    #landscaped_main_dataframe = generate_random_contexts()
    user_id_list = get_user_id_list(main_dataframe)

    processed_main_dataframe = pd.DataFrame(columns=['UserID', 'ItemID', 'Rating', 'landscape'])

    # for each user's each item ratings, check if they rated that item multiple times
    for user_id in user_id_list:

        user_ratings = get_user_ratings_preprocessing(user_id, main_dataframe)

        unique_rows = user_ratings.drop_duplicates('ItemID', keep=False)
        duplicate_rows = user_ratings[user_ratings.duplicated(['ItemID'])]
        processed_main_dataframe = processed_main_dataframe.append(unique_rows)

        user_item_column = duplicate_rows['ItemID'].tolist()
        user_item_id_list = list(dict.fromkeys(user_item_column))

        for item_id in user_item_id_list:

            duplicate_items = duplicate_rows[duplicate_rows['ItemID'] == item_id]
            
            rating_list = duplicate_items['Rating']
            landscape_list = duplicate_items['landscape']

            # take first rating and landscape we see
            rating = rating_list.iloc[0]
            landscape = landscape_list.iloc[0]

            processed_item_row = {
                'UserID': str(user_id),
                'ItemID': str(item_id),
                'Rating': rating,
                'landscape': landscape
            }
            
            processed_main_dataframe = processed_main_dataframe.append(processed_item_row, ignore_index=True)

    return processed_main_dataframe, user_id_list


# generate a random landscape context for those that do not have one
def generate_random_contexts():

    landscaped_main_dataframe = main_dataframe
    landscape_types = ['urban', 'mountains', 'countryside', 'coastline']
    landscapes = main_dataframe.loc[:, 'landscape']

    for i in range(0, len(landscapes)):

        landscape = landscapes[i]
        if type(landscape) == float:
            landscaped_main_dataframe.at[i, 'landscape'] = np.random.choice(landscape_types)
    
    del landscaped_main_dataframe['DrivingStyle']
    del landscaped_main_dataframe['mood']
    del landscaped_main_dataframe['naturalphenomena ']
    del landscaped_main_dataframe['RoadType']
    del landscaped_main_dataframe['sleepiness']
    del landscaped_main_dataframe['trafficConditions']
    del landscaped_main_dataframe['weather']

    landscaped_main_dataframe.to_csv("dataset/in_car_music.csv")

    return landscaped_main_dataframe
