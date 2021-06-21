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
    return 'Welcome to the car API!'

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

# @app.route('/cars')    
# def all_cars():
#     query = "SELECT * FROM Cars"
#     cursor = conn.cursor()
#     cursor.execute(query)
#     cars = cursor.fetchall()
#     output = []
    
#     i=0
#     while i<len(cars):
#         car_data = {'brand':cars[i][1],'model':cars[i][2],'year':cars[i][3],'description':cars[i][4]}
#         output.append(car_data)
#         i += 1
#     return {"cars":output}


# @app.route('/cars/<id>')
# def get_car(id):
#     try:
#         query = f"SELECT * FROM Cars WHERE id={id}"
#         cursor = conn.cursor()
#         cursor.execute(query)
#         cars = cursor.fetchall()
#         car_data = {'brand':cars[0][1],'model':cars[0][2],'year':cars[0][3],'description':cars[0][4]}

#         return {"car": car_data}
#     except:
#         return f'No car has id: {id}'   


# @app.route('/cars', methods=['POST'])   
# def add_car():
#     query = f"INSERT INTO Cars values('{request.json['brand']}','{request.json['model']}',{request.json['year']},'{request.json['description']}')"
#     cursor = conn.cursor()
#     cursor.execute(query)
#     cursor2=conn.cursor()
#     cursor2.execute("SELECT @@IDENTITY AS ID;")
#     id = int(cursor2.fetchone()[0])
#     conn.commit()
#     return {'id': id}


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