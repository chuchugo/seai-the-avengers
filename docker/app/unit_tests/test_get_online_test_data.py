import os, sys

ROOT = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = ROOT + "/../kafka-consumer" 
sys.path.insert(1, LIB_PATH)

import unittest
from unittest import mock
from get_online_test_data import create_test_data_consumer, collect_messages, \
                    process_messages, create_test_data, write_online_test_files
from os.path import exists

''' 
Tests all functions of get_online_test_data.py 
Coverage report shows all lines of code are tested except for the
if __name__ == '__main__': section of the code

Coverage Report

Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
get_online_test_data.py          114      7    94%   176-184
test_get_online_test_data.py      43      0   100%
------------------------------------------------------------
TOTAL                           154      7    95%
'''


class TestLoadData(unittest.TestCase):

    # Test create_test_data_consumer
    @mock.patch('get_online_test_data.KafkaConsumer', autospec=True)  # Arrange
    def test_create_test_data_consumer(self, kafka_consumer_mock):
        kafka_consumer_instance = create_test_data_consumer('movielog17')  # Act

        kafka_consumer_mock.assert_called_once_with(  # assert
            'movielog17',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='latest'
        )

    # Test collect_messages
    def test_collect_messages(self):
        try:
            kafka_consumer_instance = create_test_data_consumer('movielog17')
        except:
            print('unable to connect to kafka, skipping collect messages test\n')
            return

        kafka_messages = collect_messages(kafka_consumer_instance, 5)
        assert (kafka_messages is not None)

    # Test process_messages on live data
    def test_process_messages(self):
        try:
            kafka_consumer_instance = create_test_data_consumer('movielog17')
        except:
            print('unable to connect to kafka, skipping test process messages test\n')
            return

        kafka_messages = collect_messages(kafka_consumer_instance, 120)
        recommendations, user_watched_results, user_rated_results, _ = \
            process_messages(kafka_messages)
        assert (recommendations is not None)
        assert (user_watched_results is not None)
        assert (user_rated_results is not None)

    # Test processes_messages data quality code
    def test_process_messages_data_quality(self):
        correct_errors = [
            'bad server request format',
            'bad recommendation request format',
            'bad recommendation request',
            'bad recommendation request',
            'insufficient recommendations',
            'GET data formatting bad < 2',
            'GET data formatting bad < 4',
            'GET rate formatting bad < 3',
            'GET rate split bad',
            'skipping invalid request type'
            ]
        messages = [
            # good request message for user 284507
            "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # 'bad server request format'
            "test, data".encode('utf-8'),
            # 'bad recommendation request format'
            "2022-02-08T18:06:56.145104,284507,recommendation request 17645".encode('utf-8'),
            # 'bad recommendation request' because insufficient ':'
            "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # 'bad recommendation request' because too many ':'
            "2022-02-09T01:45:32.945123,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 0, result: java.util.concurrent.TimeoutException: Request timeout to 17645-team17.isri.cmu.edu/128.2.205.118:8082 after 800 ms, 815 ms".encode('utf-8'),
            # 'insufficient recommendations'
            "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, 133 ms".encode('utf-8'),
            # 'GET data formatting bad < 2'
            "2022-02-23T19:40:32,284507,GET data".encode('utf-8'),
            # 'GET data formatting bad < 4'
            "2022-02-23T19:40:32,284507,GET /data/mrichard+pryor+live+on+the+sunset+strip+1982".encode('utf-8'),
            # 'GET rate formatting bad < 3'
            "2022-02-25T13:38:49,284507,GET /rate".encode('utf-8'),
            # 'GET rate split bad'
            "2022-02-25T13:38:49,284507,GET /rate/audition+1999".encode('utf-8'),
            # skipping invalid request type
            "this,is,a bad request".encode('utf-8'),
            # good request message for different user - 284508 - to ensure no previous error messages also wrote data
            "2022-02-08T18:06:56.145104,284508,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # good GET data for user 284508
            "2022-02-23T19:40:32,284508,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg".encode('utf-8'),
            # good GET rate for user 284508
            "2022-02-25T13:38:49,284508,GET /rate/audition+1999=3".encode('utf-8')
        ]
        recommendations, user_watched_results, user_rated_results, errors = \
            process_messages(messages)
        # all correct errors and only those errors
        assert (correct_errors == errors)
        # both good recommendation requests
        assert (len(recommendations) == 2)
        # only 1 in user watched and rated
        assert (len(user_watched_results) == 1)
        assert (len(user_rated_results) == 1)

    def test_create_test_data(self):
        messages =   [
            # request message for 284507 - rate and watch
            "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # GET data for user 284507
            "2022-02-23T19:40:32,284507,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg".encode('utf-8'),
            # good GET rate for user 284507
            "2022-02-25T13:38:49,284507,GET /rate/audition+1999=3".encode('utf-8'),
            # request message for 284508 - just rate
            "2022-02-08T18:06:56.145104,284508,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # good GET rate for user 284508
            "2022-02-25T13:38:49,284508,GET /rate/audition+1999=3".encode('utf-8'),
            # request message for 284509 - just watch
            "2022-02-08T18:06:56.145104,284509,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # GET data for user 284509
            "2022-02-23T19:40:32,284509,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg".encode('utf-8'),
            # request message for 284510 - no watch or rate
            "2022-02-08T18:06:56.145104,284510,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
        ]

        recommendations, user_watched_results, user_rated_results, errors = \
            process_messages(messages)
        online_test_data, other_recommendations = \
            create_test_data(recommendations, user_watched_results, user_rated_results)
        # ensure correct lengths returned for test data
        assert(len(online_test_data) == 3)
        assert(len(other_recommendations) == 1)
    
    def test_write_online_test_files(self):
        messages =   [
            # request message for 284507 - rate and watch
            "2022-02-08T18:06:56.145104,284507,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # GET data for user 284507
            "2022-02-23T19:40:32,284507,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg".encode('utf-8'),
            # good GET rate for user 284507
            "2022-02-25T13:38:49,284507,GET /rate/audition+1999=3".encode('utf-8'),
            # request message for 284508 - just rate
            "2022-02-08T18:06:56.145104,284508,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # good GET rate for user 284508
            "2022-02-25T13:38:49,284508,GET /rate/audition+1999=3".encode('utf-8'),
            # request message for 284509 - just watch
            "2022-02-08T18:06:56.145104,284509,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
            # GET data for user 284509
            "2022-02-23T19:40:32,284509,GET /data/m/richard+pryor+live+on+the+sunset+strip+1982/24.mpg".encode('utf-8'),
            # request message for 284510 - no watch or rate
            "2022-02-08T18:06:56.145104,284510,recommendation request 17645-team17.isri.cmu.edu:8082, status 200, result: boxing+helena+1993, aliens+1986, airplane+1980, a+bugs+life+1998, cast+away+2000, about+a+boy+2002, ace+ventura+pet+detective+1994, apollo+13+1995, alien+1992, a+nightmare+on+elm+street+1984, ben-hur+1959, a+beautiful+mind+2001, amadeus+1984, a+time+to+kill+1996, another+stakeout+1993, ace+ventura+pet+detective+1994, addams+family+values+1993, johnny+mnemonic+1995, aladdin+1992, home+alone+1990, 133 ms".encode('utf-8'),
        ]

        recommendations, user_watched_results, user_rated_results, errors = \
            process_messages(messages)
        online_test_data, other_recommendations = \
            create_test_data(recommendations, user_watched_results, user_rated_results)
        path = write_online_test_files(online_test_data, other_recommendations, 'unit_test_jenkins', 'w')
        # ensure files exsit
        assert(exists(f'{path}/other_recommendations_unit_test_jenkins.csv'))
        assert(exists(f'{path}/online_test_data_unit_test_jenkins.csv'))

if __name__ == '__main__':
    unittest.main()