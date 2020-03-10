import pandas as pd
import numpy as np

# generate random moods - sad/happy/lazy/active

main_dataframe = pd.read_csv("dataset/in_car_music.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
song_dataframe = pd.read_csv("dataset/song_data.csv", index_col=False, delimiter=",", encoding="utf-8-sig")
music_category_dataframe = pd.read_csv("dataset/music_category.csv", index_col=False, delimiter=",", encoding="utf-8-sig")

mood_types = ['sad', 'happy', 'lazy', 'active']

moods = main_dataframe.loc[:, 'mood']
for i in range(0, len(moods)):
    mood = moods[i]
    if type(mood) == float:
        main_dataframe.at[i, 'mood'] = np.random.choice(mood_types)

del main_dataframe['DrivingStyle']
del main_dataframe['landscape']
del main_dataframe['naturalphenomena ']
del main_dataframe['RoadType']
del main_dataframe['sleepiness']
del main_dataframe['trafficConditions']
del main_dataframe['weather']


main_dataframe.to_csv("dataset/in_car_music.csv")
print(main_dataframe.head(20))