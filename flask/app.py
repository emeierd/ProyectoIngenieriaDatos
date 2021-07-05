from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime, timedelta
import pandas as pd

# Se inicializa la aplicación Flask
app = Flask(__name__)

# Se inicializa la conexión con la base de datos
conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProjectoID;"
                      "uid=sa;"
                      "pwd=aselga123")

# Mensaje de bienvenida
@app.route('/')
def index():
    return 'Bienvenido'

# Se obtienen los datos de la tabla 'id'
@app.route('/tiempo/<id>')
def obtener_tiempo(id):
    try:
        query = f"SELECT * FROM {id}"
        cursor = conn.cursor()
        cursor.execute(query)
        tiempos = cursor.fetchall()
        output = []
        
        i = 0
        while(i<len(tiempos)):
            tiempos_data = {'coordenada':tiempos[i][1],'fecha':tiempos[i][2],'temperatura':tiempos[i][3],'precipitaciones':tiempos[i][4]}
            output.append(tiempos_data)
            i += 1

        return {"tiempos": output}
    except Exception as e:
        return f'No hay datos sobre {id}: {e}'   


# Se obtienen los datos del día anterior de la tabla 'id'
@app.route('/tiempo/<id>/24h')
def ultimas_24h(id):
    hoy = datetime.now()
    ayer=hoy-timedelta(hours=24)
    format ='%Y-%m-%d'
    ayer = ayer.strftime(format)
    try:
        query = f"SELECT * FROM {id} WHERE fecha LIKE '{ayer}%'"
        cursor = conn.cursor()
        cursor.execute(query)
        tiempos = cursor.fetchall()
        output = []
        
        i = 0
        while(i<len(tiempos)):
            tiempos_data = {'coordenada':tiempos[i][1],'fecha':tiempos[i][2],'temperatura':tiempos[i][3],'precipitaciones':tiempos[i][4]}
            output.append(tiempos_data)
            i += 1

        return {"tiempos": output}
    except Exception as e:
        return f'No hay datos sobre {id}: {e}'  


# Se guardan los datos recibidos en formato json dentro de la base de datos
@app.route('/tiempo', methods=['POST'])   
def agregar_tiempo():
    nombre = request.json['nombre']
    nombre = nombre.replace(" ","_")
    query = f"INSERT INTO {nombre} values('{request.json['coordenada']}','{request.json['fecha']}',{request.json['temperatura']},'{request.json['precipitaciones']}')"
    
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        cursor2=conn.cursor()
        cursor2.execute("SELECT @@IDENTITY AS ID;")
        id = int(cursor2.fetchone()[0])
        conn.commit()
        return {'id': id,
                'nombre' : request.json['nombre']}
    except Exception as e:
        return f'Query: {query} produjo error de conexión de la base de datos: {e}'


# Se muestra el resumen del día de ayer
@app.route('/tiempo/<id>/resumen_dia')
def resumen_dia(id):
    hoy = datetime.now()
    ayer=hoy-timedelta(hours=24)
    format ='%Y-%m-%d'
    ayer = ayer.strftime(format)
    #test = '2021-06-24'
    try:
        query = f"SELECT * FROM {id} WHERE fecha LIKE '{ayer}%'"
        cursor = conn.cursor()
        cursor.execute(query)
        tiempos = cursor.fetchall()
        temperaturas = []
        precipitaciones = 0
        
        i = 0
        while(i<len(tiempos)):
            temperaturas.append(tiempos[i][3])
            precipitaciones += tiempos[i][4]
            i += 1

        minimo = min(temperaturas)
        maximo = max(temperaturas)
        
        return {"coordenada" : tiempos[0][1], "minimo" : minimo, "maximo" : maximo, "precipitaciones" : precipitaciones}
    except Exception as e:
        return f'No hay datos sobre {id}: {e}'  


# Se obtienen los datos del día anterior y se guardan dentro la tabla 24h de la ciudad correspondiente
@app.route('/tiempo/resumen_dia', methods=['POST'])
def guardar_resumen_dia():
    hoy = datetime.now()
    ayer=hoy-timedelta(hours=24)
    format ='%Y-%m-%d'
    ayer = ayer.strftime(format)
    nombre = request.json['nombre']
    nombre = nombre.replace(" ","_")
    coordenada = request.json['coordenada']
    #test = "2021-06-29"
    query = f"SELECT * FROM {nombre} WHERE fecha LIKE '{ayer}%'"
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        tiempos = cursor.fetchall()
        temperaturas = []
        precipitaciones = 0
        
        i = 0
        while(i<len(tiempos)):
            temperaturas.append(tiempos[i][3])
            precipitaciones += tiempos[i][4]
            i += 1

        minimo = min(temperaturas)
        maximo = max(temperaturas)

        nombre = nombre+"_24"
        query2 = f"INSERT INTO {nombre} values ('{coordenada}','{ayer}',{minimo},{maximo},{precipitaciones})"
        cursor2=conn.cursor()
        cursor2.execute(query2)
        conn.commit()
        
        return {"coordenada" : tiempos[0][1], "minimo" : minimo, "maximo" : maximo, "precipitaciones" : precipitaciones}
    except Exception as e:
        return f'Ha ocurrido un error: {e}'  


# Se obtiene la comparación del día de ayer entre data actualizada y data del 2012
@app.route('/tiempo/comparar/<id>')
def comparar(id):
    try:
        data = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/data.csv",
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
        tmin = []
        tmax = []
        precipitaciones = []

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
                tmin.append({"2012" : row['TMinima']})
                tmin.append({"2021" : resumen[0][1]})
                tmax.append({"2012" : row['TMaxima']})
                tmax.append({"2021" : resumen[0][2]})
                precipitaciones.append({"2012" : row['Precipitaciones']})
                precipitaciones.append({"2021" : resumen[0][3]})

        return {"fecha" : fechabd,"temperatura minima" : tmin,"temperatura maxima" : tmax, "precipitaciones" : precipitaciones}
    except Exception as e:
        return f'Ha ocurrido un error: {e}'

# Se indica la ip host y el puerto al cual será vinculado
if __name__ == '__main__':
    app.run(host='192.168.1.64', port=8090, debug=True)
