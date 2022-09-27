from kafka import KafkaConsumer
from json import loads

# Create a consumer to read data from kafka
consumer = KafkaConsumer(
    'test-nidhi',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest'
)


for message in consumer:
    print(loads(message.value))