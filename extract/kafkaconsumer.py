from kafka import KafkaConsumer
from json import loads

consumer = KafkaConsumer(bootstrap_servers='172.17.0.03:9092',auto_offset_reset='earliest',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
consumer.subscribe('apitest')
for msg in consumer:
    try:
        #print(msg.value)
        print(f"Hora: {msg.value['data']['timelines'][0]['intervals'][0]['startTime']}")
        print(f"Temperatura: {msg.value['data']['timelines'][0]['intervals'][0]['values']['temperature']}")
        print(f"Precipitaciones: {msg.value['data']['timelines'][0]['intervals'][0]['values']['precipitationIntensity']}")
    except:
        print("No data")    