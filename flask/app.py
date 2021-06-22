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


@app.route('/users')
def users():
    try:
        query = "INSERT INTO  Persons values ('Meier','Erwin',29);"
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        query = "SELECT * FROM Persons"
        cursor = conn.cursor()
        cursor.execute(query)
        persons = cursor.fetchall()
        output = []
    
        i=0
        while i<len(persons):
            person_data = {'LastName':persons[i][1],'FirstName':persons[i][2],'Years':persons[i][3]}
            output.append(person_data)
            i += 1
        return {"persons":output}
    except:
        return 'Error connecting to the Database'

# @app.route('/addUser',methods=['POST'])
# def addUser():
#     try:
#         query = "INSERT INTO  Persons values ('Meier','Erwin',29);"
#         cursor = conn.cursor()
#         cursor.execute(query)
#         conn.commit()
#         return 'User added succesfully'
#     except:
#         return 'Error connecting to the Database'



@app.route('/tiempo/<id>')
def obtener_tiempo(id):
    try:
        query = f"SELECT TOP 10 FROM {id} ORDEY BY id DESC"
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
    except:
        return f'No hay datos sobre {id}'   


@app.route('/tiempo', methods=['POST'])   
def agregar_tiempo():
    query = f"INSERT INTO {request.json['nombre']} values('{request.json['coordenada']}','{request.json['fecha']}',{request.json['temperatura']},'{request.json['precipitaciones']}')"
    cursor = conn.cursor()
    cursor.execute(query)
    cursor2=conn.cursor()
    cursor2.execute("SELECT @@IDENTITY AS ID;")
    id = int(cursor2.fetchone()[0])
    conn.commit()
    return {'id': id}


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