from kafka import KafkaConsumer
from json import loads
import requests

# Creando URL para comunicarse con Flask API
url='http://192.168.1.64:8090/tiempo'

# Crear consumer utilizando como bootstrap server el contenedor de docker conectado a red de airflow
consumer = KafkaConsumer(bootstrap_servers='172.20.0.4:9092',auto_offset_reset='earliest',
    value_deserializer=lambda x: loads(x.decode('utf-8')))

# Suscripcion a topic utilizado por producer    
consumer.subscribe('projectotiempo')
for msg in consumer:
    try:
        nombre = msg.value['nombre']
        coordenada = msg.value['coordenada']
        fecha = msg.value['data']['timelines'][0]['intervals'][0]['startTime']
        temperatura = msg.value['data']['timelines'][0]['intervals'][0]['values']['temperature']
        precipitaciones = msg.value['data']['timelines'][0]['intervals'][0]['values']['precipitationIntensity']
        
        json = {
            "nombre" : nombre,
            "coordenada" : coordenada,
            "fecha" : fecha,
            "temperatura" : temperatura,
            "precipitaciones" : precipitaciones
        }

        x = requests.post(url, json=json)    

        print(x.text)
        
    except Exception as e:
        print(f"No data, {e}")    