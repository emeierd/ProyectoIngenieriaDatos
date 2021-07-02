import pyodbc
from collections import Counter
import pandas as pd

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProjectoID;"
                      "uid=sa;"
                      "pwd=aselga123")

# Cargar data
data = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/data.csv",
    names = ['Nombre','Latitud','Longitud','Coordenadas','AA+-o','Mes',
    'Dia','TMinima','TMaxima','Precipitaciones'])

# Eliminar primera fila con headers
data.drop(index=data.index[0], axis=0, inplace=True) 

# Obtener todas las coordenadas y nombres unicos, en orden
nombres = list(Counter(data['Nombre']).keys())    

for nombre in nombres:
    nombre = nombre.replace(" ","_")
    # Crear tablas por cada nombre
    query = f"CREATE TABLE {nombre} (id int IDENTITY(1,1) PRIMARY KEY, coordenada varchar(50), fecha varchar(50) UNIQUE, temperatura float, precipitaciones float);"
    # Crear tablas resumen diario
    query2 = f"CREATE TABLE {nombre}_24 (id int IDENTITY(1,1) PRIMARY KEY, coordenada varchar(50), fecha varchar(50) UNIQUE, temperatura_minima float, temperatura_maxima float, precipitaciones float);"
    #print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.execute(query2)


conn.commit()    