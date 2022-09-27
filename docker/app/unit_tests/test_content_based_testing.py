import pandas as pd
import pickle
import unittest
<<<<<<< HEAD
import os

ROOT = os.getcwd()
DATA_PATH = ROOT + "/data/preprocessed_data.csv"
USER_DATA_PATH = ROOT + "/data/watched_combined.csv"
MODEL_PATH = ROOT + "/data/trained_model"

MODEL_TEST_PATH = ROOT + "/model"
sys.path.insert(1, MODEL_TEST_PATH)
from testing import similar_movies, recommend_user
=======

import os, sys
>>>>>>> e3144ce855d5cc3b8adbaf2f2d4645e161fc91d5

ROOT = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = ROOT + "/../model" 
sys.path.insert(1, LIB_PATH)

from testing import similar_movies, recommend_user

class TestMatrix(unittest.TestCase):
    # Test if recommendations returnec by the movie are in list form and are only 20
    def test_recommendation_format(self):
        userid = 100045
<<<<<<< HEAD
        data = pd.read_csv(DATA_PATH)
        user_data = pd.read_csv(USER_DATA_PATH)
        loaded_model = pickle.load(open(MODEL_PATH, "rb"))
=======
        data = pd.read_csv(ROOT + "/../data/preprocessed_data.csv")
        user_data = pd.read_csv(ROOT + "/../data/watched_combined.csv")
        loaded_model = pickle.load(open(ROOT + "/../data/trained_model", "rb"))
>>>>>>> e3144ce855d5cc3b8adbaf2f2d4645e161fc91d5
        mapping = pd.Series(range(len(data['id'])), index = data['id'])
        recommendations = recommend_user(userid, data, user_data, loaded_model, mapping)
        self.assertEqual(len(recommendations), 20, "20 recommendations needed!")

    # Test if values returned by similar movies is either "MOVIE NOT FOUND" or indices
    def test_similar_movies(self):
        id = 565796
<<<<<<< HEAD
        data = pd.read_csv(DATA_PATH)
        loaded_model = pickle.load(open(MODEL_PATH, "rb"))
=======
        data = pd.read_csv(ROOT + "/../data/preprocessed_data.csv")
        loaded_model = pickle.load(open(ROOT + "/../data/trained_model", "rb"))
>>>>>>> e3144ce855d5cc3b8adbaf2f2d4645e161fc91d5
        mapping = pd.Series(range(len(data['id'])), index = data['id'])
        similar_movie = similar_movies(id, data, loaded_model, mapping)

        if similar_movie != "X":
            for movie in similar_movie:
                if movie not in data['id']:
                    self.assertRaises("Movie ID incorrectly returned!")

    # Test if only 20 similar movies are returned
    def test_similar_movie_count(self):
        id = 565796
<<<<<<< HEAD
        data = pd.read_csv(DATA_PATH)
        loaded_model = pickle.load(open(MODEL_PATH, "rb"))
=======
        data = pd.read_csv(ROOT + "/../data/preprocessed_data.csv")
        loaded_model = pickle.load(open(ROOT + "/../data/trained_model", "rb"))
>>>>>>> e3144ce855d5cc3b8adbaf2f2d4645e161fc91d5
        mapping = pd.Series(range(len(data['id'])), index = data['id'])
        similar_movie = similar_movies(id, data, loaded_model, mapping)

        if similar_movie != "X":
            self.assertEqual(len(similar_movie), 20, "20 similar movies required!")


if __name__ == '__main__':
    unittest.main()