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

    train_set, test_set = train_test_split(main_dataframe, train_size=0.8)
    train_data = train_set.sort_values('UserID')
    test_data = test_set.sort_values('UserID')

    true_ratings = []
    predicted_ratings = []

    for user_id in user_id_list:
        for context in contexts:
            recommendations = get_recommendations(user_id, context, R, N, threshold)

            for index, row in test_data.iterrows():
                if row['UserID'] == str(user_id) and row['landscape'] == context:
                    print(user_id, context)


MAE(R=10, N=17, threshold=0.1)
