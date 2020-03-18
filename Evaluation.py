import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from Preprocessor import fetch_data
from Recommender import get_recommendations

warnings.filterwarnings("ignore", category=RuntimeWarning) 

main_dataframe, user_id_list, item_id_list = fetch_data()
contexts = ['urban', 'mountains', 'countryside', 'coastline']

# calculates the mean absolute error between the recommendations and actual ratings
def MAE(R, N, threshold):

    # split data into train and test sets and sort
    train_set, test_set = train_test_split(main_dataframe, train_size=0.8)
    train_data = train_set.sort_values('UserID')
    test_data = test_set.sort_values('UserID')

    true_ratings = []
    predicted_ratings = []

    # iterate through each user and each context
    for user_id in user_id_list:
        for context in contexts:
            
            # calculate recommendations for each one
            recommendations, user_mean_rating =\
                get_recommendations(user_id, train_data, context, R, N, threshold)

            # compare training data's recommendation predicted ratings to true test set ratings
            for index, row in test_data.iterrows():
                if row['UserID'] == str(user_id) and row['landscape'] == context:
                    item_id = row['ItemID']

                    user_rating_tuple =\
                        [user_rating for user_rating in recommendations if int(item_id) in user_rating]
                    print("tuple:", user_rating_tuple)


MAE(R=10, N=17, threshold=0.1)
