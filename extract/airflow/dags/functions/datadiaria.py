# En este script se obtendrá la temperatura mínima, máxima y las precipitaciones totales en un día
import requests
from datetime import date, datetime, timedelta
import json

# Obtener hora actual
hoy = datetime.now()
ayer=hoy-timedelta(hours=24)
format ='%Y-%m-%d'
ayer = ayer.strftime(format)

url = 'http://127.0.0.1:8090/tiempo'

x = json.loads(requests.get(f"{url}/Temuco").text)

fecha = x['tiempos'][0]['fecha']

fecha = fecha.replace("-04:00","")
fecha = datetime.strptime(fecha,'%Y-%m-%dT%H:%M:%S')
fecha = fecha.strftime(format)

query = f"SELECT * FROM Temuco WHERE fecha LIKE'{fecha}%'"
print(query)