from scipy.stats import chisquare
import numpy as np
import pandas as pd
import os, sys
ROOT = os.path.dirname(os.path.realpath(__file__))

DATA_PATH = ROOT + "/../statuses/online_testing/online_test_data_real.csv"
ONLINE_TEST_PATH = ROOT + "/../online_model_quality"

sys.path.insert(1, ONLINE_TEST_PATH)

import model_quality_matrix

if __name__=="__main__":
    data = pd.read_csv(DATA_PATH)
    data = data[data["user"]!="user"]
    data["user"] = data["user"].map(int)
    data_a = data[data["user"]%2!=0]
    data_b = data[data["user"]%2==0]
    
    max_freq = min(len(data_a), len(data_b))
    
    data_a = data_a.iloc[:max_freq]
    data_b = data_b.iloc[:max_freq]

    metrics_a = model_quality_matrix.Calc_accuracy(data_a) # attr: num_rate_rec,num_watched_rec,watch_rec_ratio,rate_rec_ratio
    metrics_b = model_quality_matrix.Calc_accuracy(data_b)

    watched_a = metrics_a.watch_rec_ratio
    watched_b = metrics_b.watch_rec_ratio

    num_watched_rec_a = int(watched_a*metrics_a.num_watched)
    num_watched_rec_b = int(watched_b*metrics_b.num_watched)
    
    data_a = [num_watched_rec_a, metrics_a.num_watched-num_watched_rec_a]
    data_b = [num_watched_rec_b, metrics_b.num_watched-num_watched_rec_b]
    # print(watched_ab, not_watched_ab)
    # print(watched_ab[0]+ not_watched_ab[0])
    # print(watched_ab[1] +not_watched_ab[1])
    with open("experimentation.txt","w") as f:
        statistic, pvalue = chisquare(data_a, data_b)
        f.write(f"Model A average accuracy: {watched_a}\n")
        f.write(f"Model B average accuracy: {watched_b}\n")
        f.write(f"Statistic: {statistic}\n")
        f.write(f"Pvalue: {pvalue}\n")
        if pvalue > 0.05: 
            f.write("The model performance differences are statistically insignificant.\n")
        elif watched_a> watched_b:
            f.write("Model A is better than Model B")
        else:
            f.write("Model B is better than Model A")