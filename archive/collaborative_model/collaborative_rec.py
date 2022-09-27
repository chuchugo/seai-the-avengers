import pandas as pd
import pandas as pd
from surprise import Reader
from surprise import KNNWithMeans

from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split

from collaborative_algo import formatting_result
from collaborative_algo import algo
from collaborative_algo import getDf

#2. Get movie list
def getMovieFile():
    # read all the movie ids
    import pandas as pd
    df_movies = pd.read_csv("../kafka-consumer/data/clean_data_combined.csv")
    df_movies.shape

    # df_movies.head()
    ser_movies = df_movies["id"] 
    df_movies.head(5)
    return ser_movies

ser_movies = getMovieFile()

#3. Recommendation
#For the recmmoendation for a user, create userTestSet for prediction
    # list of tuples
    #[('469629', 'casino+1995', 5.0),
    # ('871227', 'bedknobs+and+broomsticks+1971', 3.0)]

def makeSet(userid): # input should be a number instead of str
    userid = str(userid)
    userTestSet = list()
    for movie in ser_movies:
        tuple = (userid, movie, 0)
        userTestSet.append(tuple)
    return userTestSet


#choose top 20 ratings of movies for one user
def chooseTop20(userid,df_result):
    is_user = df_result["userId"]== str(userid)
    df_user = df_result[is_user]
    df_user = df_user.sort_values(["rank"], ascending=True)
    # print(df_user)
    if (df_user.shape[0]>20):
        df_user  = df_user[:20]
    return df_user

# For cold start users/ users who didnt occur in the rating file
# give them the most popular movies 
def Top20inAllMovie(df):
    # the movie occured the most in the movie rating file
    df_top20inAll = df["movieId"][:20]
    return df_top20inAll

def predictAndRecommend(userId):
    userId = str(userId)
    # check if the user didn't rate before, return top most popular movie directly
    df = getDf()
    if userId not in df["userId"].values:
        # print(Top20inAllMovie(df).tolist())
        return Top20inAllMovie(df).tolist()
    # if the user has rated before, predict her Top 20 rated movies 
    userTestSet = makeSet(userId)
    predictions2 = algo.test(userTestSet)
    df_result = formatting_result(predictions2)
    df_user = chooseTop20(userId,df_result)
    #df.to_csv('model1_data/out.csv')
    user_movieList = df_user['movieId'].tolist()
    # print(type(user_movieList),user_movieList)
    return user_movieList

#test with user 
# RecmovieList = predictAndRecommend(468282)# user is 468282
