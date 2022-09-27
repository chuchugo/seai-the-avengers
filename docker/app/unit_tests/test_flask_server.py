import unittest
from flask_server import recommend


class TestMatrix(unittest.TestCase):
    # Test if the format of the output is a string
    def test_recommendation_format(self):
        recommendations = recommend(182733)
        self.assertEqual(type(recommendations), str, "Recommendations are not strings!")

    # Test if only 20 movies are recommended
    def test_recommendation_list(self):
        recommendations = recommend(425204)
        recommendations_list = recommendations.split(",")
        self.assertEqual(len(recommendations_list), 20, "20 recommendations needed!")


if __name__ == '__main__':
    unittest.main()