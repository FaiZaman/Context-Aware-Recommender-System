import pandas as pd
import numpy as np

#main_dataframe.to_csv("dataset/in_car_music.csv")

# reading in data
main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
#song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
#music_category_dataframe = pd.read_csv("dataset/music_category.csv", index_col=False, delimiter=",", encoding="utf-8-sig")

# get user IDs as list
user_column = main_dataframe['UserID'].tolist()
user_id_list = list(dict.fromkeys(user_column))


def fetch_data():

    processed_main_dataframe = preprocess()
    return processed_main_dataframe, user_id_list


# returns the vector of a all specific user's ratings 
def get_user_ratings_preprocessing(user_id):

    user_dataframe = main_dataframe[main_dataframe['UserID'] == user_id]
    user_ratings = user_dataframe[['UserID', 'ItemID', 'Rating', 'mood']]

    return user_ratings


# preprocesses data
# if user has multiple ratings for one item, average them
def preprocess():

    processed_main_dataframe = pd.DataFrame(columns=['UserID', 'ItemID', 'Rating', 'mood'])

    # for each user's each item ratings, check if they rated that item multiple times
    for user_id in user_id_list:

        user_ratings = get_user_ratings_preprocessing(user_id)

        unique_rows = user_ratings.drop_duplicates('ItemID', keep=False)
        duplicate_rows = user_ratings[user_ratings.duplicated(['ItemID'])]
    
        item_column = duplicate_rows['ItemID'].tolist()
        item_id_list = list(dict.fromkeys(item_column))

        for item_id in item_id_list:

            duplicate_items = duplicate_rows[duplicate_rows['ItemID'] == item_id]
            
            mood_list = duplicate_items['mood']
            mood = mood_list.iloc[0]

            # choosing the first mood we see
            for mood_i in mood_list:
                if type(mood_i) != float:
                    mood = mood_i
                    break;

            average_rating = duplicate_items['Rating'].mean()

            processed_item_row = {
                'UserID': str(user_id),
                'ItemID': str(item_id),
                'Rating': average_rating,
                'mood': mood
            }

            processed_main_dataframe = processed_main_dataframe.append(unique_rows)
            processed_main_dataframe = processed_main_dataframe.append(processed_item_row, ignore_index=True)
    
    return processed_main_dataframe
