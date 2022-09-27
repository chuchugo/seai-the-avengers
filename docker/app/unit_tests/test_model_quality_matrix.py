import os, sys

ROOT = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = ROOT + "/../online_model_quality" 
sys.path.insert(1, LIB_PATH)

import unittest
from model_quality_matrix import getdata,cal_rated_and_watched,cal_rec_accuracy

# this is a test for testing online model accuracy perfoamce python file. model_quality_matrix.py
# the file includes 3 function. 
# Including getdata, get watched and rated number of movies, and get the precision ratio of user watched/ rated recommended movie

class TestMatrix(unittest.TestCase):
    # to test if the data we get from file is format into dataframe in the right way
    def test_getdata(self):
        PATH =ROOT + '/../data/online_model_data_testing.csv'
        df = getdata(PATH)
        shape =(6,5)
        self.assertEqual(df.shape, shape, "the data frame shape Should be (7,5)")

    # to test the calcuation of number of rated movie and number of watched movie
    def test_cal_rated_and_watched(self):
        PATH =ROOT + '/../data/online_model_data_testing.csv'
        df=getdata(PATH)
        rated_ratio,watched_ratio,num_watched,num_rated=cal_rated_and_watched(df)

        self.assertEqual(rated_ratio, 0.5000, "rated_ratio error")
        self.assertEqual(watched_ratio, 0.8333, "watched_ratio error")
        self.assertEqual(num_watched, 5, "num_watched error")
        self.assertEqual(num_rated, 3, "num_rated error")
    
    # to test 4 numbers related to the calculation of the number of times user watched or rated the movie we recommended.
    def test_cal_rec_accuracy(self):
        PATH = ROOT + '/../data/online_model_data_testing.csv'
        df = getdata(PATH)
        rated_ratio,watched_ratio,num_watched,num_rated=\
            cal_rated_and_watched(df)
        num_rate_rec,num_watched_rec,watch_rec_ratio,rate_rec_ratio=\
            cal_rec_accuracy(df,num_watched,num_rated)

        self.assertEqual(num_rate_rec, 1, "num_rate_rec error")
        self.assertEqual(num_watched_rec, 2, "num_watched_rec error")
        self.assertEqual(watch_rec_ratio, 0.4000, "watch_rec_ratio error")
        self.assertEqual(rate_rec_ratio, 0.3333, "rate_rec_ratio error")

if __name__ == '__main__':
    unittest.main()