import requests
from datetime import datetime, timedelta
import pandas as pd
from collections import Counter

# Cargar data
data = pd.read_csv("csv/data.csv",
    names = ['Nombre','Latitud','Longitud','Coordenadas','AA+-o','Mes',
    'Dia','TMinima','TMaxima','Precipitaciones'])

# Eliminar primera fila con headers
data.drop(index=data.index[0], axis=0, inplace=True) 

# Obtener hora actual
time = datetime.now()
time2=time-timedelta(hours=6)
timeStart=time-timedelta(seconds=120)

# Formato de hora requerida por la api
format ='%Y-%m-%dT%H:%M:%SZ'
time = time.strftime(format)
timeStart=timeStart.strftime(format)

def obtener_datos_api(coordenada):
    URL = "https://api.tomorrow.io/v4/timelines"

    QUERYSTRING = {"apikey":"ZzNvUwVGe96cTbbB9NbKSyg59zqm5bb8"}

    payload = {
        "fields": ["temperature", "precipitationType", "precipitationIntensity"],
        "units": "metric",
        "timesteps": ["current"],
        "location": coordenada,
        "timezone": "Chile/Continental"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", URL, json=payload, headers=headers, params=QUERYSTRING)

    print(response.text)


# Obtener todas las coordenadas unicas
coordenadas = list(Counter(data['Coordenadas']).keys())

# Iterar sobre coordenadas y llamar a la funcion para obtener datos mediante API
for coordenada in coordenadas:
    obtener_datos_api(coordenada)    

##Guardar datos cada una hora
##Cada dia ver cual es el minimo y maximo y guardarlo en una bd diaria

## Crear kafka producer
## Mandar response a producer
## Hacer consumer para bd
## Hacer consumer para comparacion?
## Conectar consumer comparacion a Flask API?