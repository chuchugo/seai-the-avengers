import pandas as pd


collaborative_results = pd.read_csv('../kafka-consumer/statuses/collaborative_test/rec_results.csv')
collaborative_times = collaborative_results['response_time']
clean_collaborative_times = pd.Series([int(value.split(' ')[0]) for value in collaborative_times])
mean_collab = clean_collaborative_times.mean()
print('mean collab: ', mean_collab)

content_results = pd.read_csv('../kafka-consumer/statuses/ongoing/rec_results_2.csv')
content_times = content_results['response_time']
clean_content_times = pd.Series([int(value.split(' ')[0]) for value in content_times])
mean_content = clean_content_times.mean()
print('mean content: ', mean_content)
