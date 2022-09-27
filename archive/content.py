# %% [markdown]
# ### IMPORTING LIBRARIES AND DATA

# %%
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer

# %%
data = pd.read_csv("kafka-consumer/data/clean_data_1.csv")
# user_data = pd.read_csv("kafka-consumer/data/user_watched_256.csv")
user_data = pd.read_csv("kafka-consumer/data/uniq_huge.csv")

# %% [markdown]
# ### DATA PREPROCESSING

# %%
# Convert date form to year
# for i in range(len(data['release_date'])):
#   if isinstance(data['release_date'][i], float):
#     data.at[i, 'release_date'] = ""
#   else:
#     row = data['release_date'][i].split('-')[0]
#     data.at[i, 'release_date'] = row
# data = data[data['release_date'] != ""]

# %%
# Grabbing the names of all the belongs_to_collection attached to each movie
# for i in range(len(data['belongs_to_collection'])):
#   if isinstance(data['belongs_to_collection'][i], float):
#     data.at[i, 'belongs_to_collection'] = ""
#   else:
#     row = data['belongs_to_collection'][i]
#     row = ast.literal_eval(row)
#     if not row == {}:
#       row = row['name']
#     else:
#       row = ""
#     data.at[i, 'belongs_to_collection'] = row

# %%
# Delete rows where message = "movie not found"
# data = data[data.message != "movie not found"]
# # Delete rows where status = "Rumored" or nan
# data = data[data.status != "Rumored"]
# data = data.dropna(subset=['status'], inplace=False)

# # %%
# # Delete unnecessary columns
# data = data.drop(['tmdb_id', 'imdb_id', 'original_title', 'belongs_to_collection', 'budget', 'homepage', 'original_language', 'overview', 'poster_path', 'production_countries', 'revenue', 'runtime', 'status', 'vote_average', 'vote_count', 'message'], axis=1)
# print(data.columns)
# print(data.shape)

# # %%
# # Grabbing the names of all the genres attached to each movie
# data['genres'] = data['genres'].apply(literal_eval)
# data['genres'] = data['genres'].apply(lambda x: [i['name'].lower() for i in x])
# data['genres'] = data['genres'].apply(lambda x: [i.replace(' ','') for i in x])

# %%
# Grabbing the names of all the production_companies attached to each movie
# data['production_companies'] = data['production_companies'].apply(literal_eval)
# data['production_companies'] = data['production_companies'].apply(lambda x: [i['name'].lower() for i in x])
# data['production_companies'] = data['production_companies'].apply(lambda x: [i.replace(' ','') for i in x])

# # %%
# # Grabbing the names of all the production_countries attached to each movie
# # data['production_countries'] = data['production_countries'].apply(literal_eval)
# # data['production_countries'] = data['production_countries'].apply(lambda x: [i['name'].lower() for i in x])

# # %%
# # Grabbing the names of all the spoken_languages attached to each movie
# data['spoken_languages'] = data['spoken_languages'].apply(literal_eval)
# data['spoken_languages'] = data['spoken_languages'].apply(lambda x: [i['name'].lower() for i in x])
# data['spoken_languages'] = data['spoken_languages'].apply(lambda x: [i.replace(' ','') for i in x])

# # %%
# data.head()

# # %%
# data = data.drop(['popularity', 'release_date'], axis=1)

# # %% [markdown]
# # ### MERGING ALL THE FEATURES

# # %%
# data['metadata'] = data.apply(lambda x : x['title'] + ' ' + str(x['adult']) + ' ' + ' '.join(x['genres']) + ' ' + ' '.join(x['production_companies']) + ' ' + ' ' + ' '.join(x['spoken_languages']), axis = 1)

# # %%
# data[['id', 'metadata']]

# %% [markdown]
# ### WRITING CLEAN DATA TO FILE

# %%
# data.to_csv("kafka-consumer/data/clean_data_1.csv", index=False)

# %% [markdown]
# ### MODEL TRAINING

# %%
count_vec = CountVectorizer(stop_words='english')
count_vec_matrix = count_vec.fit_transform(data['metadata'])
cosine_sim_matrix = pd.DataFrame(cosine_similarity(count_vec_matrix, count_vec_matrix))
cosine_sim_matrix.to_csv("model_matrix.csv")
cosine_sim_matrix = pd.read_csv("model_matrix.csv")
# Movies index mapping
mapping = pd.Series(data.index,index = data['id'])

# %%
# Recommender function to recommend movies based on metadata
def similar_movies(input):
  index = mapping[input]
  # Get similarity values with other movies
  similarity_score = list(enumerate(cosine_sim_matrix[index]))
  similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
  # Get the scores of the 20 most similar movies. Ignore the first movie.
  similarity_score = similarity_score[1:20]
  indices = [i[0] for i in similarity_score]
  return (data['id'].iloc[indices])

# %%
# set(similar_movies('Live Free or Die Hard'))
# user_data[user_data["user_id"]==775307]
# data.loc[data['id']=='live+free+or+die+hard+2007']['title'].tolist()[0]

# %% [markdown]
# ### MODEL PREDICTION

# %%
def recommend(userid):
  # return ["test"]*20
  watched = set(user_data[user_data["user"] == userid]['movie'].tolist())
  # print(watched)
  if len(watched) == 0:
    return "jurassic+park+1993, pulp+fiction+1994, life+is+rosy+1987, speed+1994, the+shawshank+redemption+1994, forrest+gump+1994, taken+2008, nurse+betty+2000, hamlet+1996, mission+impossible+1996, the+producers+1967, big+1988, the+last+castle+2001, ace+ventura+pet+detective+1994, interview+with+the+vampire+1994, the+break-up+2006, executive+decision+1996, the+godfather+part+iii+1990, the+silence+of+the+lambs+1991, the+freshman+1990"
  watchlist = set()
  # print("Movies watched by user " + str(userid) + ": ")
  for movie in watched:
    title = data.loc[data['id'] == movie]['id'].tolist()[0]
    # print(title)
    watchlist = watchlist.union(set(similar_movies(title)))
  return list(watchlist.difference(watched))[:20]

# recommendations = recommend(-1)
# print("\nRecommended movie list:\n", recommendations)

# %%
# UPDATE 1
# user watches multiple movies. he might rate multiple movies too. now when you receive the recommendations, 
# we need to make sure that the movie that user has rated the highest, is the one whose recommendations are given 
# first and then it goes on in a decreasing order. and once we collect all these movies, then we can sort them 
# according to the popularity and supply the top 20 movies.

# UPDATE 2
# we can also use a correlation matrix to see how features affect each other.


