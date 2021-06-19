from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='172.17.0.5:9092') #172.17.0.5 ip de maquina2 docker
for j in range(10):
    print(f"Iteration {j}")
    producer.send('test4', b'xD5')
    
producer.flush()    