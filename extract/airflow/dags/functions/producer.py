from kafka import KafkaProducer
from functions.extracciondata import obtener_datos_api
#from extracciondata import obtener_datos_api
from collections import Counter
import json
from bson import json_util
import pandas as pd

# Cargar data
## Local
# data = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/data.csv",
#     names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])
## Airflow   
data = pd.read_csv('/usr/local/airflow/dags/functions/data.csv',
    names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])

# Eliminar primera fila con headers
data.drop(index=data.index[0], axis=0, inplace=True) 

# Obtener todas las coordenadas y nombres unicos, en orden
coordenadas = list(Counter(data['Coordenadas']).keys())
nombres = list(Counter(data['Nombre']).keys())

# Inicializar Kafka Producer
producer = KafkaProducer(bootstrap_servers='172.20.0.4:9092') #172.17.0.3 ip de maquina2 docker

# Iterar sobre coordenadas, llamar a la funcion para obtener datos mediante API y enviar respuesta a kafka producer
def crear_mensaje():
    i = 0
    for i in range(len(coordenadas)):
        respuesta = json.loads(obtener_datos_api(coordenadas[i]).text)  
        # Agregar nombre a json entregado por API
        respuesta['nombre'] = nombres[i]
        # Agregar coordenada a json
        respuesta['coordenada'] = coordenadas[i]
        i += 1
        producer.send('projectotiempo', json.dumps(respuesta, default=json_util.default).encode('utf-8'))
        print(respuesta)

    producer.flush() 

crear_mensaje()