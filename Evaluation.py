from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from Preprocessor import fetch_data


main_dataframe, user_id_list, item_id_list = fetch_data()
contexts = ['urban', 'mountains', 'countryside', 'coastline']

# calculates the mean absolute error between the recommendations and actual ratings
def MAE():

    train_set, test_set = train_test_split(main_dataframe, train_size=0.8)
    train_data = train_set.sort_values('UserID')
    test_data = test_set.sort_values('UserID')

    print(train_data)
    print(test_data)


MAE()