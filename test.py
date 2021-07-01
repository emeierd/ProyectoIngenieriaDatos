import pandas as pd
from collections import Counter
import pyodbc
from datetime import datetime, timedelta

hoy = datetime.now()
ayer=hoy-timedelta(hours=24)
format ='%Y-%m-%d'
ayer = ayer.strftime(format)

data = pd.read_csv("csv/data.csv",
    names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])

data.drop(index=data.index[0], axis=0, inplace=True) 

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=192.168.1.64,1433;"
                      "Database=ProjectoID;"
                      "uid=sa;"
                      "pwd=aselga123")

#@app.route('/tiempo/comparar/<id>')
def comparar(id):
    # data = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/data.csv",
    #     names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])
    data = pd.read_csv("csv/data.csv",
        names = ['Nombre','Coordenadas','Fecha','TMinima','TMaxima','Precipitaciones'])

    data.drop(index=data.index[0], axis=0, inplace=True) 

    nombre = id.replace("_"," ")
    nombrebd = id+"_24"
    data = data[data.Nombre == nombre]

    query = f"SELECT TOP 1 fecha, temperatura_minima, temperatura_maxima, precipitaciones FROM {nombrebd} ORDER BY ID DESC"

    cursor = conn.cursor()
    cursor.execute(query)
    resumen = cursor.fetchall()
    fechabd = resumen[0][0]
    fechabd = fechabd.split("-")[1]+"-"+fechabd.split("-")[2]

    for index, row in data.iterrows():
        fecha = row['Fecha']
        split = fecha.split("-")
        mes = split[1]
        dia = split[2]
        if (len(mes)==1):
            mes = "0"+mes
        if (len(dia)==1):
            dia = "0"+dia    

        fecharow = mes+"-"+dia    
        if (fechabd == fecharow):
            print(fecha)
            print(f"temperatura minima: 2012: {row['TMinima']} 2021: {resumen[0][1]}")
            print(f"temperatura maxima: 2012: {row['TMaxima']} 2021: {resumen[0][2]}")
            print(f"total precipitaciones: 2012: {row['Precipitaciones']} 2021: {resumen[0][3]}")


comparar("Temuco")