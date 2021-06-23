from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost,1433;"
                      "Database=AppTiempo;"
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