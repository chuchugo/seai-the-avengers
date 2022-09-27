
class RecommendationModel:
    def __init__(self, model_path):
        self.model = None

    def predict_recommendation(self, userid):
        recommend_list = "03819,12345,79879,03819,12345,79879,03819,12345,79879,03819,12345,79879,03819,12345,79879,03819,12345,79879,03819,12345"
        return recommend_list