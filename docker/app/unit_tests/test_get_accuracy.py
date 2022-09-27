import unittest
import sys
import os

ROOT = os.path.dirname(os.path.realpath(__file__))
LIB_PATH_1 = ROOT + "/../model" 
LIB_PATH_2 = ROOT + "/../accuracy_measure" 
sys.path.insert(1, LIB_PATH_1)
sys.path.insert(1, LIB_PATH_2)
from testing import recommend_user

from get_accuracy import load_test_data,load_data,get_metrics, wrap_recommender, write_accuracy

# this is a test for testing get_accuracy python file. model_quality_matrix.py
# the file includes 4 functions:
# load_test_data, load_data, get_metrics, write_accuracy

class TestMatrix(unittest.TestCase):
    # to test if the test data we get from file is formatted correctly
    def test_load_test_data(self):
        ROOT = os.path.dirname(os.path.realpath(__file__))
        PATH = ROOT + "/../data/test.csv"
        test_data = load_test_data(PATH)
        num_cols = 3
        self.assertEqual(test_data.shape[1], num_cols, "invalid number of features \
            columns, should be %d but are %d"%(num_cols, test_data.shape[1]))
    
    # to test if the input data we get from file is formatted correctly
    def test_load_data(self):
        lm = load_data()[-1]
        model_shape = (13675, 13675)
        self.assertEqual(lm.shape, model_shape, f"model shape incorrect, \
            expected {model_shape} got {lm.shape}", )

    # to test if metrics are formatted correctly
    def test_get_metrics(self):
        ROOT = os.path.dirname(os.path.realpath(__file__))
        PATH = ROOT + "/../data/test.csv"
        test_data = load_test_data(PATH)
        test_data = test_data[:100]
        data,user_data,loaded_model, mapping = load_data()
        recommend_user_new = wrap_recommender(recommend_user, data,user_data,loaded_model, mapping)
        metrics = get_metrics(recommend_user_new, test_data)
        accuracy = metrics[-1]
        self.assertEqual(len(metrics), 4, "invalid metric format")
        # self.assertNotEqual(accuracy, 0, "zero accuracy error!")

    # to test if accuracy value is saved in the correct format
    def test_write_accuracy(self):
        file_name = "dummy.txt"
        accuracy = 100
        write_accuracy(file_name, accuracy)
        with open(file_name, "r") as f:
            val = float(f.read())
        self.assertEqual(accuracy,val, "file write error")

if __name__ == '__main__':
    unittest.main()