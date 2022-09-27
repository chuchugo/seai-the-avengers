'''
Kafka consumer listens and creates a file for all user request response 
messages, a file for the user, status, time response, a file with user, 
recommendations given, next movie watched, next movie rated, and the rating for 
online testing. There is also a file for user and recommendations given when 
that user does not subsequently watch or rate a movie.
'''

# importing libraries
# pip install kafka-python
from kafka import KafkaConsumer
import csv
import os
import requests
import time
import pandas as pd
import sys
import signal


  


def collect_data(index):
    # Create a list of requests
    rec_messages = []
    # collecting movies
    # time parameter is used for now to control the amount of data written to csv file.
    print("Collecting movies...")
    start_time = time.time()
    for message in consumer:
        current_time = time.time()
        elapsed_time = current_time - start_time
        #TODO try except
        try:
            message_list = message.value.decode("utf-8").split(' ')   
            type = message.value.decode("utf-8").split(' ')[0].split(',')[2]   
            if len(message_list[0].split(',')) < 3:
                print('bad server request format')   
        except:
            continue
        
        # <time>,<userid>,recommendation request <server>, status <200 for success>, result: <recommendations>, <responsetime>
        # two types of movie types: "data" and "rate"
        # 2022-02-23T19:40:32,302398,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg
        # "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms"
        # process data after a user requests recommendations
        if type == "recommendation":
            rec_messages.append(message.value.decode("utf-8"))
            # print(message)
            #TODO additional info... no needed //try except and signal handler. indexes for filename
        
        # control the time of running 
        if elapsed_time > SECONDS:
            print(f"Done run {SECONDS} SECONDS")
            break
    write_to_file(rec_messages,index)

def write_to_file(rec_messages,index):
    # writing the recommendation request messages to a csv file
    print("Writing recommendation request messages to file...")
    messages_pd = pd.DataFrame(rec_messages, columns=['messages'])
    filename = index // 120 + 1
    messages_pd.to_csv(f'{PATH}/rec_messages_{filename}.csv', mode='a', header=False, index=False)


if __name__ == '__main__':
    folder_name = sys.argv[1]
    
    PATH = os.getcwd()
    PATH += "/app/statuses/"
    PATH += folder_name
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    
    SECONDS = 30
    PULL = 1 #maybe the # for file name

    # create consumer object
    consumer = KafkaConsumer(
        'movielog17',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        group_id = folder_name,
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )
    # trail with only 30 seconds
    index = 0 #every index is equal to 30s
    while True:
        index += 1
        collect_data(index)

