import numpy as np
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer

print("GATHERING DATA")
data = pd.read_csv("kafka-consumer/data/movie_data_combined.csv")
# user_data = pd.read_csv("kafka-consumer/data/user_watched_256.csv")
# user_data = pd.read_csv("kafka-consumer/data/user_watched_ongoing.csv")

print("PREPROCESSING")
# Convert date form to year
for i in range(len(data['release_date'])):
  if isinstance(data['release_date'][i], float):
    data.at[i, 'release_date'] = ""
  else:
    row = data['release_date'][i].split('-')[0]
    data.at[i, 'release_date'] = row
data = data[data['release_date'] != ""]

# Delete rows where message = "movie not found"
data = data[data.message != "movie not found"]
# Delete rows where status = "Rumored" or nan
data = data[data.status != "Rumored"]
data = data.dropna(subset=['status'], inplace=False)

# Delete unnecessary columns
data = data.drop(['tmdb_id', 'imdb_id', 'original_title', 'belongs_to_collection', 'budget', 'homepage', 'original_language', 'overview', 'poster_path', 'production_countries', 'revenue', 'runtime', 'status', 'vote_average', 'vote_count', 'message'], axis=1)
print(data.columns)
print(data.shape)

# Grabbing the names of all the genres attached to each movie
data['genres'] = data['genres'].apply(literal_eval)
data['genres'] = data['genres'].apply(lambda x: [i['name'].lower() for i in x])
data['genres'] = data['genres'].apply(lambda x: [i.replace(' ','') for i in x])

# Grabbing the names of all the production_companies attached to each movie
data['production_companies'] = data['production_companies'].apply(literal_eval)
data['production_companies'] = data['production_companies'].apply(lambda x: [i['name'].lower() for i in x])
data['production_companies'] = data['production_companies'].apply(lambda x: [i.replace(' ','') for i in x])

# Grabbing the names of all the spoken_languages attached to each movie
data['spoken_languages'] = data['spoken_languages'].apply(literal_eval)
data['spoken_languages'] = data['spoken_languages'].apply(lambda x: [i['name'].lower() for i in x])
data['spoken_languages'] = data['spoken_languages'].apply(lambda x: [i.replace(' ','') for i in x])

data = data.drop(['popularity', 'release_date'], axis=1)

print("FEATURE MERGING")
data['metadata'] = data.apply(lambda x : x['title'] + ' ' + str(x['adult']) + ' ' + ' '.join(x['genres']) + ' ' + ' '.join(x['production_companies']) + ' ' + ' ' + ' '.join(x['spoken_languages']), axis = 1)

print("MODEL TRAINING")
data.to_csv("kafka-consumer/data/clean_data_m2.csv", index=False)

count_vec = CountVectorizer(stop_words='english')
count_vec_matrix = count_vec.fit_transform(data['metadata'])
cosine_sim_matrix = cosine_similarity(count_vec_matrix, count_vec_matrix)
# Movies index mapping
mapping = pd.Series(data.index,index = data['id'])

file = open("../group-project-s22-the-avengers/kafka-consumer/model/2_saved_model_m1", "ab")
pickle.dump(cosine_sim_matrix, file)
file.close()
