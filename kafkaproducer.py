from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092')
for j in range(10):
    print(f"Iteration {j}")
    data = {'counter': j}
    producer.send('test', value=data)