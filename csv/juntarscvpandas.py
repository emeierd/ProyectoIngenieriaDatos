import pandas as pd
from collections import Counter

temperaturas = pd.read_csv("csv/temperaturas.csv",
    names = ['_id','IdEstacion','Nombre','Latitud','Longitud','Altura','AA+-o','Mes',
    'Dia','TMinima','TMaxima'])
precipitaciones = pd.read_csv("csv/precipitaciones.csv",
    names = ['_id','IdEstacion','Nombre','Latitud','Longitud','Altura','AA+-o','Mes',
    'Dia','Valor'])

# Eliminar primera fila que contiene headers
temperaturas.drop(index=temperaturas.index[0], axis=0, inplace=True)
precipitaciones.drop(index=precipitaciones.index[0], axis=0, inplace=True)

# Nombres unicos
countTemp = list(Counter(temperaturas['Nombre']).keys())

# Verificar si las listas de nombre son identicas 
if(Counter(temperaturas['Nombre']).keys()==Counter(precipitaciones['Nombre']).keys()):
    print("yes")
else:
    print("no")    

# Crear dos listas distintas para ver que estaciones tienen 366 datos en ambas dataframe
listTemp = list(Counter(temperaturas['Nombre']).values())
listPrec = list(Counter(precipitaciones['Nombre']).values())
#print(listTemp)
#print(listPrec)

# Crear lista vacia para agregar nombres en ambas listas con 366 datos
mezcla = [countTemp,listTemp,[]]
for i in range(len(mezcla[1])):
    mezcla[2].append("Distintos")

for i in range(len(mezcla[1])):
    if(mezcla[1][i]==listPrec[i]):
        print(f'{mezcla[1][i]}==>{listPrec[i]}')
        if(listPrec[i]==366):
            mezcla[2][i]="Iguales"


for i in range(len(mezcla[1])):
    if(mezcla[2][i]=="Distintos"):
        print(mezcla[0][i])
        temperaturas.drop(temperaturas[temperaturas.Nombre == mezcla[0][i]].index, inplace=True)
        precipitaciones.drop(precipitaciones[precipitaciones.Nombre == mezcla[0][i]].index, inplace=True)


# Ver la cantidad de filas unicas en la dataframe
#print(temperaturas.nunique())

# Reiniciar los indices para que no haya problema al juntar las 2 dataframes
temperaturas = temperaturas.reset_index(drop=True)
precipitaciones = precipitaciones.reset_index(drop=True)

# Agregar mediante insert
# t = pd.Series(precipitaciones['Valor'])
# temperaturas.insert(loc=11, column='Precipitaciones', value=t) ## tengo que eliminar los indices
# Agregar de forma mas simple
temperaturas['Precipitaciones'] = precipitaciones['Valor']
print(temperaturas)

### FALTA ###
#TRANSFORMAR MINUTOS A DECIMALES, ELIMINAR DATOS QUE NO SE OCUPAN

# Guardar data transformada en csv
temperaturas.to_csv('csv/mezcla.csv')