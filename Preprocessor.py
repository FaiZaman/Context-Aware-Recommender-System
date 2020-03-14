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

    return main_dataframe, user_id_list


# returns the vector of a all specific user's ratings 
def get_user_ratings(user_id):

    user_dataframe = main_dataframe[main_dataframe['UserID'] == 1001]   # change to userID
    user_ratings = user_dataframe[['ItemID', 'Rating', 'mood']]

    return user_ratings


# preprocesses data
# if user has multiple ratings for one item, average them
def preprocess():

    processed_main_dataframe = pd.DataFrame(columns=['UserID', 'ItemID', 'Rating', 'mood'])

    # for each user's each item ratings, check if they rated that item multiple times
    for user_id in range(0, len(user_id_list)):

        user_ratings = get_user_ratings(user_id)
        duplicate_rows = user_ratings[user_ratings.duplicated(['ItemID'])]
        
        duplicate_items = duplicate_rows[duplicate_rows['ItemID'] == 674]
        mood_list = duplicate_items['mood']
        mood = mood_list.iloc[0]

        # choosing the first mood we see
        for mood_i in mood_list:
            if type(mood_i) != float:
                mood = mood_i
                break;

        duplicate_indices = duplicate_items.index.values
        replace_index = duplicate_indices[0]
        
        average_rating = duplicate_items['Rating'].mean()

        user_ratings = user_ratings.drop(user_ratings.index[duplicate_indices])

        processed_item_row = {
            'UserID': str(1001),
            'ItemID': str(674),
            'Rating': average_rating,
            'mood': mood
        }
        processed_main_dataframe = processed_main_dataframe.append(processed_item_row, ignore_index=True)
        print(processed_main_dataframe)
        break;

preprocess()
