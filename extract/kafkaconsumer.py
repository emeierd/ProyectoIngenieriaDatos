from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='172.17.0.03:9092')
consumer.subscribe('apitest')
for msg in consumer:
    print (msg)