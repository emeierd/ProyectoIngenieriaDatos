import pandas as pd
from collections import Counter

temperaturas = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/temperaturas.csv",
    names = ['_id','IdEstacion','Nombre','Latitud','Longitud','Altura','AA+-o','Mes',
    'Dia','TMinima','TMaxima'])
precipitaciones = pd.read_csv("/home/erwin/Desktop/ProyectoIngenieriaDatos/csv/precipitaciones.csv",
    names = ['_id','IdEstacion','Nombre','Latitud','Longitud','Altura','AA+-o','Mes',
    'Dia','Valor'])


temperaturas.drop(index=temperaturas.index[0], axis=0, inplace=True)
precipitaciones.drop(index=precipitaciones.index[0], axis=0, inplace=True)
print(temperaturas[['_id','IdEstacion','Nombre','Latitud','Longitud',
    'AA+-o','Mes','Dia','TMinima','TMaxima']])
print(precipitaciones[['Valor']])

countTemp = list(Counter(temperaturas['Nombre']).keys())

# Verificar si las listas de nombre son identicas 
if(Counter(temperaturas['Nombre']).keys()==Counter(precipitaciones['Nombre']).keys()):
    print("yes")
else:
    print("no")    

# Crear dos listas distintas para ver que estaciones tienen 366 datos en ambas dataframe
listTemp = list(Counter(temperaturas['Nombre']).values())
listPrec = list(Counter(precipitaciones['Nombre']).values())

# Crear lista vacia para agregar nombres en ambas listas con 366 datos
mezcla = [countTemp,listTemp,[]]
for i in range(len(mezcla[1])):
    mezcla[2].append("Distintos")

for i in range(len(mezcla[1])):
    for e in range(len(listPrec)):
        if(mezcla[1][i]==listPrec[e]):
            mezcla[2][i]="Iguales"

# for i in mezcla[1]:
#     for e in listPrec:
#         if(i==e):
#             mezcla[2].append("iguales")
#         else:
#             mezcla[2].append("distintos")   

for i in range(len(mezcla)):
    if(mezcla[2][i]=="Distintos"):
        t#emperaturas.drop(temperaturas[temperaturas.Nombre == mezcla[0][i]].index, inplace=True)
        temperaturas = temperaturas[temperaturas.Nombre == mezcla[0][i]]


print(temperaturas)        