from kafka import KafkaConsumer

consumer = KafkaConsumer(bootstrap_servers='172.17.0.05:9092')
consumer.subscribe('test4')
for msg in consumer:
    print (msg)