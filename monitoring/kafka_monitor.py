from kafka import KafkaConsumer
from prometheus_client import Counter, Histogram, Gauge, start_http_server

start_http_server(8765)

# Counter, Gauge, Histogram, Summaries
REQUEST_COUNT = Counter('request_count', 'Recommendation Request Count', ['http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request Latency')
REQUEST_STATUS_RATIO = Gauge('request_status_200_ratio', 'Request Status 200')

if __name__ == "__main__":
    consumer = KafkaConsumer(
        'movielog17',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id='the-avengers-m3-provenance',
        enable_auto_commit=True,
        auto_commit_interval_ms=1000
    )

    count_200 = 0
    count_not_200 = 0

    for message in consumer:
        event = message.value.decode('utf-8')
        values = event.split(',')

        if 'recommendation request' in values[2]:
            print(values)
            status = values[3].strip().split(" ")[1]
            REQUEST_COUNT.labels(status).inc()

            if status == "200":
                count_200 += 1
            else:
                count_not_200 += 1
            REQUEST_STATUS_RATIO.set(count_200 / (count_200 + count_not_200))

            time_taken = float(values[-1].strip().split(" ")[0])
            REQUEST_LATENCY.observe(time_taken / 1000)