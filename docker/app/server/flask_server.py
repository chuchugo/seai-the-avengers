from flask import Flask, jsonify, request

import os
import pandas as pd
import pickle
import random
import sys

# to kill this for real when it says 'in use':
# kill -9 $(ps -A | grep python | awk '{print $1}')

ROOT = os.path.dirname(os.path.realpath(__file__))
TEST_FILE_PATH = ROOT + "/../model"
USER_DATA_PATH = ROOT + "/../data/watched_combined.csv"
DATA_PATH = ROOT + "/../data/preprocessed_data.csv"
MODEL_PATH = ROOT + "/../data/trained_model"

sys.path.insert(1, TEST_FILE_PATH)
from testing import recommend_user

# Data loading necessary for both models
print("GATHERING DATA")
user_data = pd.read_csv(USER_DATA_PATH)
# length = len(user_data)
# print('file length =',length)
# SKIP = length - 2000000
# print(f'skipping {SKIP} lines')
# user_data = user_data[SKIP:]
# print('user data len = ', len(user_data))
user_set = set(user_data["user"])

# Data loading that is only necessary for the content model
data = pd.read_csv(DATA_PATH)

print("LOADING DATA")
loaded_model = pickle.load(open(MODEL_PATH, "rb"))

# Movies index mapping
print("MAPPING DATA")
mapping = pd.Series(range(len(data['id'])), index = data['id'])

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({'message' : 'It works!'})

# decorator controlling what actually serves the recommendations
print("RECOMMENDING...")
@app.route('/recommend/<int:userid>', methods=['GET'])
def recommend(userid):
    ver_b = False
    if userid%4==0:
        ver_b = True
    if userid not in user_set:
        index = random.randrange(0, len(user_set))
        userid = list(user_set)[index]
        
    # Run content model
    rcmd_res = recommend_user(userid, data, user_data, loaded_model, mapping, ver_b )

    return ','.join(rcmd_res)
    # return ','.join(["shrek+2001", "shrek+2+2004", "shrek+the+third+2007", "shrek+forever+after+2010"]*5)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8081, debug=True)