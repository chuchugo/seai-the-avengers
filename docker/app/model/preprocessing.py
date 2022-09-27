from ast import literal_eval
from datetime import datetime
import spacy
import math

def preprocess_data(data):
    print("DATA PREPROCESSING")

    # Modify belongs_to_collection if there is a collection the movie belongs to
    for i in range(len(data['belongs_to_collection'])):
        if data['belongs_to_collection'][i] != "{}":
            #check NaN
            if not isNaN(data['belongs_to_collection'][i]):
                collection = data['belongs_to_collection'][i].split(",")[1].split("'")[-2].replace("Collection", "").strip(" :\"")
                data.at[i, 'belongs_to_collection'] = collection
            else:
                continue
        if data['belongs_to_collection'][i] == "{}":
            data.at[i, 'belongs_to_collection'] = ""

    # Normalize popularity between range of 0 and 1
    for i in range(len(data['popularity'])):
        data.at[i, 'popularity'] = data['popularity'][i] / data['popularity'].max() * 100

    # Named Entity Recognition on overview + POS Tagging
    # NER tags that are not people are kept
    # POS verb VERB + adverb ADV + adjective ADJ only
    # NLP = spacy.load("en_core_web_sm")
    # for i in range(len(data['overview'])):
    #     if isinstance(data['overview'][i], float):
    #         data.at[i, 'overview'] = ""
    #     else:
    #         raw_text = NLP(data['overview'][i])

    #         ner_list = []
    #         for word in raw_text.ents:
    #             if word.label_ != "PERSON":
    #                 ner_list.append(word.text)

    #         pos_list = []
    #         for word in raw_text:
    #             if word.pos_ == "VERB" or word.pos_ == "ADV" or word.pos_ == "ADJ":
    #                 pos_list.append(word.text)

    #         overview_list = list(set(ner_list + pos_list))
    #         overview = ' '.join([word for word in overview_list])

    #         data.at[i, 'overview'] = overview

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

    required_columns = ['id', 'title', 'adult', 'belongs_to_collection', 'genres', 'overview', 'popularity',
                'production_companies', 'production_countries', 'release_date', 'spoken_languages', 'status', 'metadata']

    # data = data.drop(['popularity', 'release_date'], axis=1)
    data['metadata'] = data.apply(lambda x: str(x['title']) + ' ' + str(x['adult']) + ' ' + str(x['belongs_to_collection']) + ' '.join(x['genres']) 
                                            + ' ' + str(x['overview']) + ' ' + str(x['popularity']) + ' ' + ' '.join(x['production_companies']) 
                                            + ' ' + ' '.join(x['production_countries']) + ' ' + str(x['release_date']) + ' ' 
                                            + ' '.join(x['spoken_languages']) + ' ' + str(x['status']), axis = 1)

    return data, required_columns

#check NaN
def isNaN(string):
    return string != string