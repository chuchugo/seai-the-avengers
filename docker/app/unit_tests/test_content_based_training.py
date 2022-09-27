import os, sys

ROOT = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = ROOT + "/../model" 
sys.path.insert(1, LIB_PATH)

import unittest
<<<<<<< HEAD
from model.data import get_data
from model.preprocessing import preprocess_data
from model.training import train_model

=======
from data import get_data
from preprocessing import preprocess_data
from training import train_model
>>>>>>> e3144ce855d5cc3b8adbaf2f2d4645e161fc91d5
class TestMatrix(unittest.TestCase):
    # Test if data returned has 24 columns and has all te same columns as required
    def test_data_size(self):
        raw_data, data_columns = get_data()
        return raw_data, data_columns
    # Test if data has only 13 columns after precprossing and also has a column called METADATA
    def test_preprocessed_data(self):
        raw_data, data_columns = self.test_data_size()
        self.assertEqual(list(raw_data), data_columns, "Inconsistency in data columns!")
        self.assertEqual(len(list(raw_data)), len(data_columns), "24 columns needed!")
        preprocessed_data, required_columns = preprocess_data(raw_data)
      
        return preprocessed_data, required_columns
    # Test if model gets trained with consistent data
    def test_model_training(self):
        preprocessed_data, required_columns = self.test_preprocessed_data()
        self.assertEqual(list(preprocessed_data), required_columns, "All the necessary columns are not present!")
        self.assertEqual(len(preprocessed_data.columns), 13, "Processed data needs 13 columns!")
        self.assertIn('metadata', preprocessed_data.columns, "Metadata not found for the model!")
        length, matrix_shape = train_model(preprocessed_data)
        self.assertEqual(length, 13675, "Length of data not equal to 13675!")
        self.assertEqual(matrix_shape, (13675, 13675), "Shape of cosine matrix is not (13675, 13675)!")
if __name__ == '__main__':
    unittest.main()