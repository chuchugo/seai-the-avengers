# 1. Train KNN model using Cosine similarity with user rating data

# We want to choose the similar user to every user.
# Find the similar user by all user ratings.(calculate by cosine similarity of person A's rating to person B's ratings)
# If the ratings are similar, these two people have similar taste.

import pandas as pd
columns = ["userId","movieId","rating"]
df = pd.read_csv("kafka-consumer/data/rated_combined.csv",names=columns, skiprows=1)


df = df.drop_duplicates(subset="userId")
df.head()
df = df[:15000]
 

def getDf():
    return df

import pandas as pd3
from surprise import Reader
from surprise import KNNWithMeans

from surprise import Dataset

# Loads rating data for training 
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[["userId", "movieId", "rating"]], reader)

# To use user-based cosine similarity
sim_options = {
    "name": "cosine",
    "user_based": True,
}

# Training algorithm using KNNwithMeans, to find the closest users to user A
algo = KNNWithMeans(k=2, sim_options=sim_options) #(k=40, min_k=1, sim_options={}, verbose=True, **kwargs)

#split training, validation dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
trainset, validationset = train_test_split(data, test_size=.20)
trainset

algo.fit(trainset)
#predictions = algo.test(validationset)
#accuracy.rmse(predictions)
def getAlgo():
    return algo

import pickle
file = open("collaborative_model/saved_model_combined_collaborative", "ab")
pickle.dump(algo, file)
file.close()

#formatting result
def formatting_result(predictions): 
    columns = ["userId", "movieId","rating","est","details"]
    df_result = pd.DataFrame(predictions,columns = columns)
    df_result = df_result[["userId", "movieId","rating","est"]]
    # add rank
    # each user, we rank the rightest ratings for website recommendations
    df_result["rank"] = df_result.groupby("userId")["est"].rank("dense", ascending=False)
    return df_result

