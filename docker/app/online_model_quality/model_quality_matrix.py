import os
import pandas as pd

# this python script is to calculate the performance of the online model
# To see the percentage of times users have really watched or rated the movie we recommended to them
# Using the csv file of kafka online_testing part as an example.

class Calc_accuracy:
    def __init__(self):
        PATH = os.path.dirname(os.path.realpath(__file__))
        PATH += "/../statuses/online_testing/online_test_data_real.csv"
        df = getdata(PATH)
        #ratios are string format
        rated_ratio,watched_ratio,num_watched,num_rated=\
            cal_rated_and_watched(df)
        num_rate_rec,num_watched_rec,watch_rec_ratio,rate_rec_ratio=\
            cal_rec_accuracy(df,num_watched,num_rated)

# read csv file of online_test_data_real includes 
# user,recommendations,watched movie,rated movie,rating
def getdata(PATH):
    df = pd.read_csv(PATH)
    df.head()
    df.describe()
    return df

# firstly to see how many rating and watching behaviors in total
def cal_rated_and_watched(df):      
    rows = df.shape[0]
    cols = df.shape[1]

    df["watched movie"].head()
    num_nan_rated = df["rating"].isna().sum() 
    num_rated = df["rating"].notna().sum() 
    num_nan_watched = df["watched movie"].isna().sum() 
    num_watched = df["watched movie"].notna().sum() 

    rated_ratio = num_rated/rows
    watched_ratio = num_watched /rows
    rated_ratio = round(rated_ratio, 4)
    watched_ratio = round(watched_ratio, 4)
    # rated_ratio = "{:.4f}".format(rated_ratio)
    # watched_ratio = "{:.4f}".format(watched_ratio)

    print("number of users who rated:  " ,num_rated)
    print("number of users who wachted movie:  " ,num_watched)
    return rated_ratio,watched_ratio,num_watched,num_rated;

# secondly to observe the the percentage of times of users 
# who watched /rated recommendated movie to users who watched/rated movie 
def cal_rec_accuracy(df,num_watched,num_rated):      
    # %%
    type(df["recommendations"])
    # %%
    df["watch_recommended"] =  df["recommendations"].isin([df["watched movie"]])
    #df["watch_recommended"] =  df["recommendations"].str.contains(df["watched movie"],regex=False)

    # %%
    #transfer wachted movie to watched_movie, and also make it into string type
    df["watched_movie"]=df["watched movie"].apply(str)
    df.drop("watched movie",axis=1)

    #apply if user has watched the recommended 
    df['watch_recommended'] = df.apply(lambda x: x.watched_movie in x.recommendations, axis=1)

    #count those who wacthed recommended movie and those who didn't
    num_watched_rec= df['watch_recommended'].value_counts().loc[True]
    num_not_watched_rec =df['watch_recommended'].value_counts().loc[False]

    # %%
    # explore the about movie rating behaviors and recommendations
    df_rated = df[df["rated movie"].notna()]

    # change column name for rated movie to rated_movie
    df["rated_movie"]=df["rated movie"].apply(str)
    df.drop("rated movie",axis=1)

    #check if the movie user rated is the what the system has recommended
    df['rate_recommended'] = df.apply(lambda x: x.rated_movie in x.recommendations, axis=1)

    #%%
    num_rate_rec= df['rate_recommended'].value_counts().loc[True]
    num_not_rate_rec =df['rate_recommended'].value_counts().loc[False]


    #%%
    #model accuracy matrix
    #percentage of user who watched recommended movies /users who watched any movie
    watch_rec_ratio = num_watched_rec /num_watched
    #percentage of user who rated recommended movies / user who rated any movie
    rate_rec_ratio = num_rate_rec/num_rated
    # watch_rec_ratio = "{:.4f}".format(watch_rec_ratio)
    # rate_rec_ratio = "{:.4f}".format(rate_rec_ratio)
    watch_rec_ratio = round(watch_rec_ratio, 4)
    rate_rec_ratio = round(rate_rec_ratio, 4)

    print("percentage of users who requested recommendations and then watched a movie who ended up watching a movie we recommended:\n",watch_rec_ratio)
    print("percentage of users who requested recommendations and then rated a movie who ended up rating a movie we recommended :\n",rate_rec_ratio)
    return num_rate_rec,num_watched_rec,watch_rec_ratio,rate_rec_ratio

calculation = Calc_accuracy()