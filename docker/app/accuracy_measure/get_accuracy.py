import numpy as np
import pandas as pd
import sys, pickle
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
MODEL_TEST_PATH = ROOT + "/../model"
TEST_PATH = ROOT + "/../data/test.csv"
METRICS_PATH = ROOT + "/../data/accuracy.txt"
MODEL_PATH = ROOT + "/../data/trained_model"
DATA_PATH = ROOT + "/../data/preprocessed_data.csv"
USER_DATA_PATH = ROOT + "/../data/watched_combined.csv"

sys.path.insert(1, MODEL_TEST_PATH)
from testing import recommend_user


# test_data format : pd.DataFrame(columns=["user", "movie"])
def load_test_data(path):
    return pd.read_csv(path)

# load model and data
def load_data():
    data = pd.read_csv(DATA_PATH)
    user_data = pd.read_csv(USER_DATA_PATH)
    mapping = pd.Series(range(len(data['id'])), index = data['id'])
    loaded_model = pickle.load(open(MODEL_PATH, "rb"))
    return data,user_data,mapping,loaded_model

# wraps recommender so only takes user id as input
def wrap_recommender(rec_fn, data,user_data,loaded_model, mapping):
    return lambda userid: rec_fn(userid, data, user_data, loaded_model, mapping)

# compute accuracy and precision metrics
def get_metrics(recommend_fn, test_data):
    total_users = len(test_data["user"].unique())
    print("Total users tested:",total_users)
    count = 0
    avg_prec = 0
    top_5_acc = 0
    top_10_acc = 0
    top_20_acc = 0
    for user_id in test_data["user"][:500].unique(): 
        count += 1
        # print iteration count
        if count % 100 == 0:
            print(count)
        if count > 1000:
            break
        top_5 = top_10_prec = top_10 = top_20 = 0
        next_watched = test_data[test_data["user"]==user_id]["movie"]
        rec_movies = recommend_fn(user_id)
        for movie in next_watched:
            if movie in rec_movies[:5]:
                top_20 = top_10 = top_5 = 1
            elif movie in rec_movies[:10]:
                top_20 = top_10 = 1
            elif movie in rec_movies:
                top_20 = 1
        for movie in rec_movies[:5]:
            if movie in next_watched:
                top_10_prec+=1
        top_5_acc += top_5
        top_10_acc += top_10
        top_20_acc += top_20
        avg_prec += top_10_prec
    return np.array([avg_prec, top_5_acc, top_10_acc, top_20_acc]) / total_users

# write accuracy to file
def write_accuracy(METRICS_PATH, accuracy):
    print(f"writing accuracy to: {METRICS_PATH}")
    with open(METRICS_PATH, "w") as f:
        f.write(str(accuracy) + "\n")

def evaluate_model():
    test_data = load_test_data(TEST_PATH)
    data,user_data,mapping, loaded_model  = load_data()
    recommend_user_new = wrap_recommender(recommend_user, data,user_data,loaded_model, mapping)
    metrics = get_metrics(recommend_user_new, test_data)
    write_accuracy(METRICS_PATH, metrics[-1])

if __name__ == '__main__':
    evaluate_model()