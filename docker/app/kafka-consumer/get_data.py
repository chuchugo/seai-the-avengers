# importing libraries
# pip install kafka-python
from kafka import KafkaConsumer
import csv
import os
import requests
import time
import pandas as pd
import signal
import sys
import subprocess

# create set for movies and 
# lists for storing tuples of user/movie

'''
SSH Tunneling
-- SERVER --
ssh -L 9092:localhost:9092 tunnel@128.2.204.215 -NTf
password: seaitunnel
'''



def write_files(new_movies, user_watched, movie_path, watched_path):
    # IP addresses
    # local_ip = "128.2.205.118"
    server_ip = "128.2.204.215"
    # writing the user watched table to a csv file
    # a version of to_csv is below the current one for when we are "ammending" instead of writing to the file
    print("Writing user watched table to file...")
    user_watched_pd = pd.DataFrame(user_watched, columns=['user', 'movie'])
    user_watched_pd.to_csv(watched_path, mode='a', header=False, index=False)

    # collecting movie data
    print("Collecting movie data...")
    movie_headers = ['id', 'tmdb_id', 'imdb_id', 'title', 'original_title', 'adult', 'belongs_to_collection',
            'budget', 'genres', 'homepage', 'original_language', 'overview', 'popularity', 'poster_path',
            'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 
            'spoken_languages', 'status', 'vote_average', 'vote_count', 'message']

    # writing movie data to a csv file
    print("Writing movie data to file...")
    with open(movie_path, 'a', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=movie_headers)
        # every movie is added as a new line to the file
        for movie in new_movies:
            # access a stream from server
            try:
                request = requests.get("http://" + server_ip + ":8080/movie/" + movie)
                features = request.json()
                # write features to file
                csvwriter.writerow(features)
            except:
                continue

def collect_data(MOVIE_PATH, WATCHED_PATH, SECONDS):
    # collecting movies
    # time parameter is used for now to control the amount of data written to csv file.
    print("Collecting movies...")
    start_time = time.time()
    new_movies = set()
    user_watched = []
    for message in consumer:
        current_time = time.time()
        elapsed_time = current_time - start_time
        # data quality checks    
        try:
            user = message.value.decode("utf-8").split(' ')[0].split(',')[1]
            _ = int(user)
        except:
            continue
        try:
            data = message.value.decode("utf-8").split(' ')[1].split('/')
        except:
            continue
        if len(data) < 4:
            continue

        # two types of movie types: "data" and "rate"
        if data[1] == "data":
            movie = data[3]
            if len(user_watched) < 100000:
                user_watched.append((user, movie))

        # creating a list of users, the movies they watched, and ratings given
        # rating is set to None when no rating was provided
        if movie not in MOVIE_SET and movie not in new_movies:
            if (len(new_movies) < 300):
                new_movies.add(movie)
            MOVIE_SET.add(movie)
        
        if elapsed_time > SECONDS:
            write_files(new_movies, user_watched, MOVIE_PATH, WATCHED_PATH)
            return

    


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.realpath(__file__))
    MOVIE_PATH = PATH + "/../data/movie_data_combined.csv"
    WATCHED_PATH = PATH + "/../data/watched_combined.csv"


    # create consumer object
    consumer = KafkaConsumer(
        'movielog17',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        group_id='the-avengers-m3-provenance',
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )

    movie_data = pd.read_csv(MOVIE_PATH)
    MOVIE_SET = set(movie_data['id'])
    SECONDS = 15
    collect_data(MOVIE_PATH, WATCHED_PATH, SECONDS)
   

