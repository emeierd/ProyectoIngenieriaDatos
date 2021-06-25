import requests
from datetime import datetime, timedelta

# Obtener hora actual
time = datetime.now()
# time2=time-timedelta(hours=6)
# timeStart=time-timedelta(seconds=120)

# Formato de hora requerida por la api
format ='%Y-%m-%dT%H:%M:%SZ'
time = time.strftime(format)

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

    return response


##Guardar datos cada una hora
##Cada dia ver cual es el minimo y maximo y guardarlo en una bd diaria

## Crear kafka producer
## Mandar response a producer
## Hacer consumer para bd
## Hacer consumer para comparacion?
## Conectar consumer comparacion a Flask API?