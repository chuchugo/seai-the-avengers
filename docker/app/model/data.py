import pandas as pd
import os
from datetime import date
import time
import subprocess

# getting today's date: https://www.programiz.com/python-programming/datetime/current-datetime
# getting git revion code: https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script


ROOT = os.path.dirname(os.path.realpath(__file__))
MOVIE_DATA_PATH = ROOT + "/../data/movie_data_combined.csv"
PROV_PATH = ROOT + "/../data/provenance.txt"
USER_DATA_PATH = ROOT + "/../data/watched_combined.csv"

def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

def get_data():
    print("GATHERING DATA")
    movie_data = pd.read_csv(MOVIE_DATA_PATH)
    user_len = len(pd.read_csv(USER_DATA_PATH)) + 1
    movie_len = len(movie_data) + 1
    date_today = date.today()
    time_now = time.time()
    time_now = time.ctime(time_now)
    git_code = get_git_revision_short_hash()
    with open(PROV_PATH, 'a') as file:
        file.write(f"date: {date_today} time: {time_now} git commit code: {git_code} movie data file length: {movie_len} user data file length: {user_len}\n")

    movie_columns = ['id', 'tmdb_id', 'imdb_id', 'title', 'original_title', 'adult', 'belongs_to_collection', 'budget', 'genres', 'homepage',
                    'original_language', 'overview', 'popularity', 'poster_path', 'production_companies', 'production_countries', 
                    'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'vote_average', 'vote_count', 'message']
    
    return movie_data, movie_columns