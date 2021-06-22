import pyodbc
from collections import Counter
import pandas as pd

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=AppTiempo;"
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

# Crear tablas por cada nombre
for nombre in nombres:
    nombre = nombre.replace(" ","_")
    query = f"CREATE TABLE {nombre} (id int IDENTITY(1,1) PRIMARY KEY, coordenada varchar(50), fecha varchar(50), temperatura int, precipitaciones int);"
    #print(query)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()