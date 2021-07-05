# Este script realiza la extracción de data desde la API tiempo (tomorrow.io)
import requests
from datetime import datetime, timedelta

# Obtener hora actual
time = datetime.now()
# time2=time-timedelta(hours=6)
# timeStart=time-timedelta(seconds=120)

# Formato de hora requerida por la api
format ='%Y-%m-%dT%H:%M:%SZ'
time = time.strftime(format)

# Este método realiza la consulta a la API según la coordenada que se le envíe
def obtener_datos_api(coordenada):
    URL = "https://api.tomorrow.io/v4/timelines"

    QUERYSTRING = {"apikey":"ZzNvUwVGe96cTbbB9NbKSyg59zqm5bb8"}

    # Datos que requiere la API
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

    # Se realiza la consulta POST a la API, devuelve data en formato json
    response = requests.request("POST", URL, json=payload, headers=headers, params=QUERYSTRING)

    return response