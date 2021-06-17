import requests
from datetime import datetime, timedelta

time = datetime.now()
time2=time-timedelta(hours=6)
timeStart=time-timedelta(seconds=120)
format ='%Y-%m-%dT%H:%M:%SZ'
time = time.strftime(format)
timeStart=timeStart.strftime(format)

url = "https://api.tomorrow.io/v4/timelines"

querystring = {"apikey":"ZzNvUwVGe96cTbbB9NbKSyg59zqm5bb8"}

payload = {
    "fields": ["temperature", "precipitationType", "precipitationIntensity"],
    "units": "metric",
    "timesteps": ["current"],
    "location": "68.87,93.52000000000001",
    "timezone": "Chile/Continental"
}
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

print(response.text)
print(time)

##Guardar datos cada una hora
##Cada dia ver cual es el minimo y maximo y guardarlo en una bd diaria

## Leer el csv y sacar la localizacion de cada nombre
## usar este metodo
## listTemp = list(Counter(temperaturas['Nombre']).values())
## deberia hacer una columna de coordenadas, pero se supone que las latitudes y longitudes de cada estacion son distintas