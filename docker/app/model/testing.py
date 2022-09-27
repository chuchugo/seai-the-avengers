'''
Data collection and loading is done in the flask server
This file contains functions for recommending movies based on similarity of 
new movies to mvoies a user has already watched
'''

# Recommender function to recommend movies based on metadata
def similar_movies(id, data, mapping, loaded_model):
    # If movie is not found in the mapping, return MOVIE NOT FOUND which is removed from the list later on
    # print(mapping)
    if id not in mapping:
        return ['zebrahead+1992', 'the+myth+of+the+american+sleepover+2010', 'the+love+letter+1999', 'the+incredibly+true+adventure+of+two+girls+in+love+1995', 
        'the+fountain+2006', 'ten+inch+hero+2007', 'shrek+the+third+2007', 'shrek+forever+after+2010', 'shrek+2001', 'shrek+2+2004', 'quiet+city+2007', 
        'mozart+and+the+whale+2005', 'modern+romance+1981', 'lucas+1986', 'love+me+tender+1956', 'its+my+party+1996', 'its+all+about+love+2003', 'feast+of+love+2007',
        'down+with+love+2003', 'dedication+2007']
    
    index = mapping[id]

    # Get similarity values with other movies
    try:
        similarity_score = list(enumerate(loaded_model[index]))
    except IndexError:
        return "X"
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    # Get the scores of the 20 most similar movies. Ignore the first movie.
    similarity_score = similarity_score[1:21]
    indices = [i[0] for i in similarity_score]
    return data['id'].iloc[indices]

def recommend_user(userid, data, user_data, loaded_model, mapping, ver_b):
    # Get the movies watched by the user
    watched = set(user_data[user_data["user"] == userid]['movie'].tolist())
    watchlist = set()
    # watchlist = list()

    #model difference
    sim_movies = 3 if ver_b else 5

    # Get similar recommendations to the movies watched
    for id in list(watched)[-sim_movies::-1]:
        movie_id = data.loc[data['id'] == id]['id'].tolist()
        if len(movie_id) > 0:
            id = movie_id[0]

        # Recommendations list is the difference between similar movies and movies already watched
        # Return all movies similar to the movie passed which might include movies already seen by the user
        watchlist = watchlist.union(set(similar_movies(id, data, mapping, loaded_model)))
    # Rank the recommendations by similarity score and return the top 20
    # Find the difference between watched movies and all similar movies and store that as a list of recommendations
    recommendations = list(watchlist.difference(watched))
    recommendations = [i for i in recommendations if i != "X"]
    recommendations = sorted(recommendations, reverse=True)[:20]

    return recommendations