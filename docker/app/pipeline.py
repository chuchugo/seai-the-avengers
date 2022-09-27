from model.data import get_data
from model.preprocessing import preprocess_data
from model.training import train_model
from accuracy_measure.get_accuracy import evaluate_model

# training the model
raw_data, data_columns = get_data()

train_dataframe, required_columns = preprocess_data(raw_data)

data_length, matrix_shape = train_model(train_dataframe)

# offline evaluation
evaluate_model()