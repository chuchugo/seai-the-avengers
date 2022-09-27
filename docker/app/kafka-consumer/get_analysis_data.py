'''
Kafka consumer listens and creates a file for all user request response 
messages, a file for the user, status, time response, a file with user, 
recommendations given, next movie watched, next movie rated, and the rating for 
online testing. There is also a file for user and recommendations given when 
that user does not subsequently watch or rate a movie.
'''

# File used to collect online telemetry data

# importing libraries
# pip install kafka-python
from kafka import KafkaConsumer, TopicPartition
import csv
import os
import requests
import time
import pandas as pd
from os.path import exists

# IP address
# server_ip = "128.2.204.215"

# create consumer object
# topic = 'movielog17' for production system
def create_test_data_consumer(topic):
    print('create test data consumer')
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest'
    )
    consumer.subscribe([topic])
    return consumer

# collect messages from consumer
def collect_messages(consumer, duration):
    print('collect messages')
    start_time = time.time()
    messages=[]
    for message in consumer:
        if time.time() > start_time + duration:
            return messages
        messages.append(message.value)
            

# gather data from messages
def process_messages(messages):
    print('process_messages')
    # create lists
    rec_messages = []
    recommendations = {}
    user_watch = set()
    user_rate = set()
    user_watched_results = {}
    user_rated_results = {}
    errors = []

    # process messages
    for message in messages:  
        message_list = message.decode("utf-8").split(' ')
        if len(message_list[0].split(',')) < 3:
            errors.append('bad server request format')
            continue

        type = message.decode("utf-8").split(' ')[0].split(',')[2]
        user = message.decode("utf-8").split(' ')[0].split(',')[1]

        # process data after a user requests recommendations
        # "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms"
        if type == "recommendation":
            rec_messages.append(message.decode("utf-8"))
            # ensure good recommendation status message
            if len(message_list) < 7:
                errors.append('bad recommendation request format')
                continue
            # split message up by : to get recommendation list
            rec_split = message.decode("utf-8").split(':')
            if len(rec_split) != 5:
                errors.append('bad recommendation request')
                continue
            # get data from message
            recommendation = rec_split[4].split(',')[:-1]
            recommendation = [movie.strip() for movie in recommendation]
            if (len(recommendation) == 20):
                recommendations[user] = recommendation
            else:
                errors.append('insufficient recommendations')
                continue
            # add data to lists
            user_watch.add(user)
            user_rate.add(user)

        # process data from user watched and rated movies if the user has 
        #     previously requested movie recommendations
        # 2022-02-23T19:40:32,302398,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg
        elif type == "GET":
            # split off data and ensure minimum length
            data = message_list[1].split('/')
            if len(data) < 2:
                errors.append('GET data formatting bad < 2')
                continue
            # get user movie watched data
            if user in user_watch and data[1] == "data":
                # ensure correct length first
                if len(data) < 4:
                    errors.append('GET data formatting bad < 4')
                    continue
                movie = data[3]
                user_watched_results[user] = movie
                user_watch.remove(user)
            # get user rated movie data
            elif user in user_rate and data[1] == "rate":
                # ensure correct data lengths first
                if len(data) < 3:
                    errors.append('GET rate formatting bad < 3')
                    continue
                data_split = data[2].split("=")
                if len(data_split) < 2:
                    errors.append('GET rate split bad')
                    continue
                movie = data_split[0]
                rating = data_split[1]
                user_rated_results[user] = (movie, rating)
                user_rate.remove(user)
        else:
            errors.append('skipping invalid request type')
    return recommendations, user_watched_results, user_rated_results, errors



# create the list of online test data from the recommendations, 
#    watched results, and ratings results dicts
# when a user either watches or rates a movie but not both, they are still
#    added to the online test data list but with None in the missing data fields
# create a separate list of user and recommendation list when no watched or 
#    rated movie occurs for that user during the time period monitored
def create_test_data(recommendations, user_watched_results, user_rated_results):
    print('create test data')
    # create return lists
    online_test_data = []
    other_recommendations = []
    for user in recommendations.keys():
        recs = recommendations[user]
        if user in user_watched_results:
            watched_movie = user_watched_results[user]
        else:
            watched_movie = None
        if user in user_rated_results:
            rated_movie, rating = user_rated_results[user]
        else:
            rated_movie = None
            rating = None
        if watched_movie or rated_movie:
            online_test_data.append((user, recs, watched_movie, rated_movie, rating))
        else:
            other_recommendations.append((user, recs))
    return online_test_data, other_recommendations

def write_online_test_files(online_test_data, other_recommendations, filename, mode):
    # make the path for the data
    PATH = os.path.dirname(os.path.realpath(__file__))
    PATH += "/../statuses/online_testing"
    
    # writing the online testing data to a csv file
    print("Writing online testing data to a csv file")
    online_test_data_pd = pd.DataFrame(online_test_data, columns=['user','recommendations','watched movie', 'rated movie', 'rating'])
    online_test_data_pd.to_csv(f'{PATH}/online_test_data_{filename}.csv', index=False, mode=mode, header=None)

    # writing other recommendations to a csv file
    print("Writing other to a csv file")
    other_recommendations_pd = pd.DataFrame(other_recommendations, columns=['user','recommendations'])
    other_recommendations_pd.to_csv(f'{PATH}/other_recommendations_{filename}.csv', index=False, mode=mode, header=None)

    return PATH

if __name__ == '__main__':
    topic = 'movielog17'
    duration = 300
    consumer = create_test_data_consumer(topic)
    messages = collect_messages(consumer, duration)
    print('messages collected: ', len(messages))

    recommendations, user_watched_results, user_rated_results, _ = \
        process_messages(messages)
    print('recommendations served: ', len(recommendations))

    online_test_data, other_recommendations = create_test_data(recommendations, \
        user_watched_results, user_rated_results)
    print('number of online test data results: ', len(online_test_data))
    print('number of other recommendations', len(other_recommendations))

    write_online_test_files(online_test_data, other_recommendations, 'exp', 'a')
