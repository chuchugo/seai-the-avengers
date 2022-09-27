### IMPORTING LIBRARIES AND DATA
import numpy as np
import pandas as pd
import pickle
import spacy
from ast import literal_eval
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

'''
This file trains the content based model and stores it for use by the testing file
'''

### USER-DEFINED EXCEPTIONS
class IncorrectInputError(Exception):
    pass

class IncorrectProcessedDataError(Exception):
    pass

class InsufficientDataError(Exception):
    pass

class CosineMatrixShapeError(Exception):
    pass


print("GATHERING DATA")
try:
    data = pd.read_csv("../group-project-s22-the-avengers/kafka-consumer/data/movie_data_combined.csv")
    columns = ['id', 'tmdb_id', 'imdb_id', 'title', 'original_title', 'adult', 'belongs_to_collection', 'budget', 'genres', 'homepage',
                    'original_language', 'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries', 
                    'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'vote_average', 'vote_count', 'message']
    if list(data) != columns or np.any((data.columns == columns)) == False:
        raise IncorrectInputError
except IncorrectInputError:
    print("Movie data needs 24 columns!")

### DATA PREPROCESSING
print("DATA PREPROCESSING")

# Modify belongs_to_collection if there is a collection the movie belongs to
for i in range(len(data['belongs_to_collection'])):
    if data['belongs_to_collection'][i] != "{}":
        collection = data['belongs_to_collection'][i].split(",")[1].split("'")[-2].replace("Collection", "").strip(" :\"")
        data.at[i, 'belongs_to_collection'] = collection
    if data['belongs_to_collection'][i] == "{}":
        data.at[i, 'belongs_to_collection'] = ""

# Normalize popularity between range of 0 and 1
for i in range(len(data['popularity'])):
    data.at[i, 'popularity'] = data['popularity'][i] / data['popularity'].max() * 100

# Named Entity Recognition on overview + POS Tagging
# NER tags that are not people are kept
# POS verb VERB + adverb ADV + adjective ADJ only
NLP = spacy.load("en_core_web_sm")
for i in range(len(data['overview'])):
    if isinstance(data['overview'][i], float):
        data.at[i, 'overview'] = ""
    else:
        raw_text = NLP(data['overview'][i])

        ner_list = []
        for word in raw_text.ents:
            if word.label_ != "PERSON":
                ner_list.append(word.text)

        pos_list = []
        for word in raw_text:
            if word.pos_ == "VERB" or word.pos_ == "ADV" or word.pos_ == "ADJ":
                pos_list.append(word.text)

        overview_list = list(set(ner_list + pos_list))
        overview = ' '.join([word for word in overview_list])

        data.at[i, 'overview'] = overview

# Convert date form to year
for i in range(len(data['release_date'])):
    if isinstance(data['release_date'][i], float):
        data.at[i, 'release_date'] = ""
    else:
        row = data['release_date'][i].split('-')
        year, month, date = row[0], datetime.strptime(row[1], "%m").strftime("%B"), row[2]
        data.at[i, 'release_date'] = month + " " + date + ", " + year
data = data[data['release_date'] != ""]

# Delete rows where message = "movie not found"
data = data[data.message != "movie not found"]

# Delete rows where status = "Rumored" or nan
data = data[data.status != "Rumored"]
data = data.dropna(subset=['status'], inplace=False)

# Grabbing the names of all the genres attached to each movie
data['genres'] = data['genres'].apply(literal_eval)
data['genres'] = data['genres'].apply(lambda x: [i['name'].lower() for i in x])
data['genres'] = data['genres'].apply(lambda x: [i.replace(' ','') for i in x])

# Grabbing the names of all the production_companies attached to each movie
data['production_companies'] = data['production_companies'].apply(literal_eval)
data['production_companies'] = data['production_companies'].apply(lambda x: [i['name'].lower() for i in x])
data['production_companies'] = data['production_companies'].apply(lambda x: [i.replace(' ','') for i in x])

# Grabbing the names of all the production_countries attached to each movie
data['production_countries'] = data['production_countries'].apply(literal_eval)
data['production_countries'] = data['production_countries'].apply(lambda x: [i['name'].lower() for i in x])
data['production_countries'] = data['production_countries'].apply(lambda x: [i.replace(' ','') for i in x])

# Grabbing the names of all the spoken_languages attached to each movie
data['spoken_languages'] = data['spoken_languages'].apply(literal_eval)
data['spoken_languages'] = data['spoken_languages'].apply(lambda x: [i['name'].lower() for i in x])
data['spoken_languages'] = data['spoken_languages'].apply(lambda x: [i.replace(' ','') for i in x])

# Keep necessary columns
data = data[['id', 'title', 'adult', 'belongs_to_collection', 'genres', 'overview', 'popularity',
            'production_companies', 'production_countries', 'release_date', 'spoken_languages', 'status']]

# data = data.drop(['popularity', 'release_date'], axis=1)
data['metadata'] = data.apply(lambda x: str(x['title']) + ' ' + str(x['adult']) + ' ' + str(x['belongs_to_collection']) + ' '.join(x['genres']) 
                                        + ' ' + str(x['overview']) + ' ' + str(x['popularity']) + ' ' + ' '.join(x['production_companies']) 
                                        + ' ' + ' '.join(x['production_countries']) + ' ' + str(x['release_date']) + ' ' 
                                        + ' '.join(x['spoken_languages']) + ' ' + str(x['status']), axis = 1)

try:
    if len(data.columns) != 13:
        raise IncorrectProcessedDataError
except IncorrectProcessedDataError:
    print("Processed data needs 14 columns!")

### TRAINING THE MODEL
print("WRITING CLEAN DATA TO FILE")
data.to_csv("../group-project-s22-the-avengers/kafka-consumer/data/2_clean_data.csv", index=False)

# LENGTH OF DATA['ID']
try:
    if len(data['id']) != 13675:
        raise InsufficientDataError
except InsufficientDataError:
    print("Length of data not equal to 13675!")
# print(len(data['id']))

print("TRAINING THE MODEL")

count_vec = CountVectorizer(stop_words='english')
count_vec_matrix = count_vec.fit_transform(data['metadata'])
cosine_sim_matrix = cosine_similarity(count_vec_matrix, count_vec_matrix)

# SHAPE OF COSINE MATRIX
try:
    if cosine_sim_matrix.shape != (13675, 13675):
        raise CosineMatrixShapeError
except CosineMatrixShapeError:
    print("Shape of cosine matrix is not (13675, 13675)!")
# print(cosine_sim_matrix.shape)

file = open("../group-project-s22-the-avengers/kafka-consumer/model/2_saved_model", "ab")
pickle.dump(cosine_sim_matrix, file)
file.close()

print("...DONE!!")