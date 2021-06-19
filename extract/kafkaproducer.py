from kafka import KafkaProducer
from extracciondata import obtener_datos_api
from collections import Counter
import json
from bson import json_util
import pandas as pd

# Cargar data
data = pd.read_csv("csv/data.csv",
    names = ['Nombre','Latitud','Longitud','Coordenadas','AA+-o','Mes',
    'Dia','TMinima','TMaxima','Precipitaciones'])

# Eliminar primera fila con headers
data.drop(index=data.index[0], axis=0, inplace=True) 

# Obtener todas las coordenadas unicas
coordenadas = list(Counter(data['Coordenadas']).keys())

# Inicializar Kafka Producer
producer = KafkaProducer(bootstrap_servers='172.17.0.5:9092') #172.17.0.5 ip de maquina2 docker

# Iterar sobre coordenadas, llamar a la funcion para obtener datos mediante API y enviar respuesta a kafka producer
for coordenada in coordenadas:
    respuesta = obtener_datos_api(coordenada).text  
    producer.send('test4', json.dumps(respuesta, default=json_util.default).encode('utf-8'))

producer = KafkaProducer(bootstrap_servers='172.17.0.5:9092') #172.17.0.5 ip de maquina2 docker
for j in range(10):
    print(f"Iteration {j}")
    producer.send('test4', b'xD5')
    
producer.flush()    