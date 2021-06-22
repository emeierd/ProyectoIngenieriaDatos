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
# if(Counter(temperaturas['Nombre']).keys()==Counter(precipitaciones['Nombre']).keys()):
#     print("yes")
# else:
#     print("no")    

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
        if(listPrec[i]==366):
            mezcla[2][i]="Iguales"


for i in range(len(mezcla[1])):
    if(mezcla[2][i]=="Distintos"):
        #print(mezcla[0][i])
        temperaturas.drop(temperaturas[temperaturas.Nombre == mezcla[0][i]].index, inplace=True)
        precipitaciones.drop(precipitaciones[precipitaciones.Nombre == mezcla[0][i]].index, inplace=True)


# Ver la cantidad de filas unicas en la dataframe
#print(temperaturas.nunique())

# Reiniciar los indices para que no haya problema al juntar las 2 dataframes
temperaturas = temperaturas.reset_index(drop=True)
precipitaciones = precipitaciones.reset_index(drop=True)

# Agregar mediante insert
# t = pd.Series(precipitaciones['Valor'])
# temperaturas.insert(loc=11, column='Precipitaciones', value=t)
# Agregar de forma mas simple
temperaturas['Precipitaciones'] = precipitaciones['Valor']

# Eliminar columnas innecesarias
temperaturas.drop('_id',axis=1,inplace=True)
temperaturas.drop('IdEstacion',axis=1,inplace=True)
temperaturas.drop('Altura',axis=1,inplace=True)

# Transformar formato de coordenadas a decimales
for i in range(len(temperaturas['Nombre'])):
    latitud = temperaturas['Latitud'][i].split()
    gradoLat = int(latitud[0].split('&')[0])
    minutosLat=int(latitud[1].replace("'",""))
    segundosLat=int(latitud[2].replace("'",""))
    latitud = gradoLat+(minutosLat*60+segundosLat)/100
    temperaturas['Latitud'][i] = latitud

    longitud = temperaturas['Longitud'][i].split()
    gradoLon = int(longitud[0].split('&')[0])
    minutosLon=int(longitud[1].replace("'",""))
    segundosLon=int(longitud[2].replace("'",""))
    longitud = gradoLon+(minutosLon*60+segundosLon)/100
    temperaturas['Longitud'][i] = longitud
    #print(f'[{latitud},{longitud}]')

# Agregar columna Coordenadas, juntando latitud y longitud
coordenadas = []
for index, row in temperaturas.iterrows():
    coordenadas.append(f"{row['Latitud']},{row['Longitud']}")

# Agregar coodenadas a temperatura
temperaturas.insert(loc=3, column='Coordenadas', value=coordenadas)    

# Eliminar 4 nombres unicos de la lista, ya que la api solo acepta 500 consultas al dia
nombres = list(Counter(temperaturas['Nombre']).keys())
temperaturas.drop(temperaturas[temperaturas.Nombre == nombres[7]].index, inplace=True)
temperaturas.drop(temperaturas[temperaturas.Nombre == nombres[8]].index, inplace=True)
temperaturas.drop(temperaturas[temperaturas.Nombre == nombres[10]].index, inplace=True)
temperaturas.drop(temperaturas[temperaturas.Nombre == nombres[21]].index, inplace=True)
#print(temperaturas.nunique())

# Modificar nombres a nombre de comuna
#print(nombres)
temperaturas['Nombre'].replace('Chacalluta, Arica Ap.', 'Arica', inplace=True)
temperaturas['Nombre'].replace('Diego Aracena Iquique Ap.', 'Iquique', inplace=True)
temperaturas['Nombre'].replace('El Loa, Calama Ad.', 'Calama', inplace=True)
temperaturas['Nombre'].replace('Cerro Moreno  Antofagasta  Ap.', 'Antofagasta', inplace=True)
temperaturas['Nombre'].replace('Mataveri  Isla de Pascua Ap.', 'Isla de Pascua', inplace=True)
temperaturas['Nombre'].replace('Desierto de Atacama, Caldera  Ap.', 'Caldera', inplace=True)
temperaturas['Nombre'].replace('La Florida, La Serena Ad.', 'La Serena', inplace=True)
temperaturas['Nombre'].replace('Rodelillo, Ad.', 'Rodelillo', inplace=True)
temperaturas['Nombre'].replace('Quinta Normal, Santiago', 'Quinta Normal Santiago', inplace=True)
temperaturas['Nombre'].replace('Pudahuel Santiago ', 'Pudahuel Santiago', inplace=True)
temperaturas['Nombre'].replace('Santo Domingo, Ad.', 'Santo Domingo', inplace=True)
temperaturas['Nombre'].replace('Juan Fern?ndez, Estaci?n Meteorol?gica.', 'Juan Fernández', inplace=True)
temperaturas['Nombre'].replace('General Freire, Curic? Ad.', 'Curicó', inplace=True)
temperaturas['Nombre'].replace('Bernardo O"higgins, Chill?n Ad.', 'Chillán', inplace=True)
temperaturas['Nombre'].replace('Carriel Sur, Concepci?n.', 'Concepción', inplace=True)
temperaturas['Nombre'].replace('Mar?a Dolores, Los Angeles Ad.', 'Los Angeles', inplace=True)
temperaturas['Nombre'].replace('Maquehue, Temuco Ad.', 'Temuco', inplace=True)
temperaturas['Nombre'].replace('Pichoy, Valdivia Ad.', 'Valdivia', inplace=True)
temperaturas['Nombre'].replace('Ca?al Bajo,  Osorno Ad.', 'Osorno', inplace=True)
temperaturas['Nombre'].replace('El Tepual  Puerto Montt Ap.', 'Puerto Montt', inplace=True)
temperaturas['Nombre'].replace('Teniente Vidal, Coyhaique Ad.', 'Coyhaique', inplace=True)
temperaturas['Nombre'].replace('Balmaceda Ad.', 'Balmaceda', inplace=True)
temperaturas['Nombre'].replace('Carlos Iba?ez, Punta Arenas Ap.', 'Punta Arenas', inplace=True)
temperaturas['Nombre'].replace('C.M.A. Eduardo Frei Montalva, Ant?rtica ', 'Antártica', inplace=True)
#nombres = list(Counter(temperaturas['Nombre']).keys())
#print(nombres)


# Guardar data transformada en csv
temperaturas.to_csv('csv/data.csv', index=False)