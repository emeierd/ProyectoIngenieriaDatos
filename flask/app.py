from flask import Flask, request, jsonify
import pyodbc
from datetime import datetime, timedelta

app = Flask(__name__)

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=ProjectoID;"
                      "uid=sa;"
                      "pwd=aselga123")

@app.route('/')
def index():
    return 'Bienvenido'


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


@app.route('/tiempo/<id>/24h')
def ultimas_24h(id):
    hoy = datetime.now()
    ayer=hoy-timedelta(hours=24)
    format ='%Y-%m-%d'
    ayer = ayer.strftime(format)
    xd = '2021-06-24'
    try:
        query = f"SELECT * FROM {id} WHERE fecha LIKE '{xd}%'"
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


@app.route('/tiempo/resumen_dia', methods=['POST'])
def guardar_resumen_dia(id):
    hoy = datetime.now()
    ayer=hoy-timedelta(hours=24)
    format ='%Y-%m-%d'
    ayer = ayer.strftime(format)
    nombre = request.json['nombre']
    nombre = nombre.replace(" ","_")
    coordenada = request.json['coordenada']
    try:
        query = f"SELECT * FROM {nombre} WHERE fecha LIKE '{ayer}%'"
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

        query2 = f"INSERT INTO {nombre}_24h values ('{coordenada}','{ayer}',{minimo},{maximo},{precipitaciones}"
        cursor2=conn.cursor()
        cursor2.execute(query2)
        conn.commit()
        
        return {"coordenada" : tiempos[0][1], "minimo" : minimo, "maximo" : maximo, "precipitaciones" : precipitaciones}
    except Exception as e:
        return f'Ha ocurrido un error: {e}'          

# @app.route('/cars/<id>', methods=['DELETE'])    
# def delete_car(id):
#     try:
#         query = f"DELETE FROM Cars WHERE id={id}"
#         cursor = conn.cursor()
#         cursor.execute(query)
#         conn.commit()

#         return f'Car {id} deleted'
#     except:
#         return f'No car has id: {id}'       

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)