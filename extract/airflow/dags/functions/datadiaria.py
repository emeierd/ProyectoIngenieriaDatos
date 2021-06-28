# En este script se comunicara con la API mediante un metodo POST, el cual enviara el nombre de
# la ciudad para que la api obtenga los datos de las ultimas 24h y luego los guarde en la tabla 24h
import requests
import json
import pandas as pd
from collections import Counter

# Cargar data
## Local
data = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/data.csv",
    names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])
## Airflow   
# data = pd.read_csv('/usr/local/airflow/dags/functions/data.csv',
#     names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])

# Eliminar primera fila con headers
data.drop(index=data.index[0], axis=0, inplace=True) 

# Obtener todas las coordenadas y nombres unicos, en orden
coordenadas = list(Counter(data['Coordenadas']).keys())
nombres = list(Counter(data['Nombre']).keys())

url = 'http://127.0.0.1:8090/tiempo/resumen_dia'

def post_24h():
    i = 0
    for i in range(len(coordenadas)):
        try:
            json = {
                "nombre" : nombres[i],
                "coordenada" : coordenadas[i]
            }
            x = requests.post(url, json=json)    

            print(x.text)   
        except Exception as e:  
            print(f"Error conectando a API: {e}")  
        i+=1               


post_24h()