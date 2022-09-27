from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle

ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = ROOT + "/../data/preprocessed_data.csv"
MODEL_PATH = ROOT + "/../data/trained_model"

def train_model(data):
    print("WRITING CLEAN DATA TO FILE")
    data.to_csv(DATA_PATH, index=False)
    print(len(data['id']))

    print("TRAINING THE MODEL")
    count_vec = CountVectorizer(stop_words='english')
    # print("xx")
    count_vec_matrix = count_vec.fit_transform(data['metadata'])
    # print("yy")
    print(count_vec_matrix.shape)
    cosine_sim_matrix = cosine_similarity(count_vec_matrix)
    print(cosine_sim_matrix.shape)
    
    file = open(MODEL_PATH, "wb")
    pickle.dump(cosine_sim_matrix, file)
    file.close()

    print("...DONE!!")

    return len(data['id']), cosine_sim_matrix.shape