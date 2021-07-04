# ProyectoIngenieriaDatos
Este es un proyecto en donde se ocupan una serie de herramientas de ingeniería de datos con el fin de mostrar su uso. 
* Se transformarán datos desde archivos .csv y son guardados dentro de [csv/data.csv](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f98dc3ec1ff89ddcc4984e3e952821104139c2a4/csv/data.csv) los cuales utilizados para distintas tareas.
* Se extraerán datos de una API de tiempo, que muestra temperaturas y precipitaciones. Esto en base a los datos del punto anterior.
* Estos datos extraídos serán enviados a través de Kafka producer, el cual estará dentro de un DAG de Apache Airflow, para que se ejecute de forma automática cada 60 minutos.
* Se creará un Kafka consumer que leerá los mensajes enviados por producer, el cual posteriormente se comunicará con la API Flask para almacenar estos datos en SQL Server.
* Se creará otro DAG de Airflow, el cual se ejecutará todos los dias a las 4AM, el cual obtendrá los datos del día anterior, calculará las temperaturas mínimas y máximas, así como el total de precipitaciones y luego se comunicará con la API Flask para ingresar estos datos a la base de datos.
* Se hará una comparación de estos datos contra los datos dentro del archivo [csv/data.csv](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f98dc3ec1ff89ddcc4984e3e952821104139c2a4/csv/data.csv) y se mostrará mediante una consulta a la API Flask.

# Herramientas ocupadas
## Docker
Se utilizó Docker con el fin de ser la plataforma para distintos servicios como Microsoft SQL Server 2019, Apache Kafka y Apache Airflow. Docker hace posible utilizar estos servicios sin necesidad de ser instalados en la máquina, también se podría generar un cluster de Apache Kafka, montando varios servidores o *brokers* que se conecten al mismo Zookeeper.

### Docker compose
Necesario para levantar Apache Airflow, el cual utiliza un contenedor de MySQL como base de datos para su funcionamiento y un contenedor Webserver, el cual contiene Airflow y la interfaz de usuario para este.

## SQL Server
Para el servidor de SQL Server se ocupó la imagen oficial de Microsoft con el comando:
docker run --name sqlserver2019 -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=aselga123' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-latest

Una vez creado el contenedor de SQl Server se puede ingresar a este utilizando Microsoft SQL Server Management Studio(SSMS) o desde la línea de comandos.
Más información disponible en [pasosbd.txt](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/main/flask/pasosbd.txt), *cabe mencionar que los pasos señalados se realizaron en ubuntu 20.4, por lo que para windows se recomienda utilizar SSMS*

Dentro de este servidor crearemos una base de datos con el nombre ProjectoID, en el cual se crearán las tablas utilizando el script
[creaciontablasbd.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/main/flask/creaciontablasbd.py)

Con esto tenemos el servidor de SQL Server funcionando, en caso de que se quiera parar este servicio, se debe ejecutar el comando\
**docker stop sqlserver2019**

Para volver a levantar el servidor se debe utilizar el comando\
**docker start sqlserver2019**

## Apache Airflow
Airflow es utilizado para automatizar todo el proceso de extracción, transformación y carga de datos. De esta forma, no se necesita estar pendiente
al 100% para tener un flujo de trabajo constante y programado. Esta herramienta será la responsable de correr el [script que realiza las consultas a la API
del tiempo](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dags/functions/producer.py) y el [script que realiza un resumen del día anterior](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dags/functions/datadiaria.py).

Dentro de la carpeta [extract](https://github.com/emeierd/ProyectoIngenieriaDatos/tree/main/extract) encontraremos la carpeta [airflow](https://github.com/emeierd/ProyectoIngenieriaDatos/tree/main/extract/airflow), donde encontraremos la carpeta **dags**, **dockerfiles** y el archivo [docker-compose.yml](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/docker-compose.yml) es el archivo necesario para poder arrancar los contenedores necesarios para Airflow mediante *Docker compose*. En este destacan los servicios, *postgresql* y *webserver*, cada uno de estos servicios será cargado dentro de un contenedor aparte.

El contenedor de **postgresql** cargará una imagen desde *docker hub* (postgres 9.6), mientras que el contenedor de **webserver** o Airflow creará una imágen personalizada, la cual encontraremos de la carpeta **dockerfiles**, archivo [Dockerfile](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dockerfiles/Dockerfile), el cual utiliza una imagen predeterminada de airflow: **puckel/docker-airflow:latest**, se cambia el huso horario y se instala **python3** con los paquetes requeridos por los script.

En [dags](https://github.com/emeierd/ProyectoIngenieriaDatos/tree/main/extract/airflow/dags) nos encontramos con los **DAG**(Directed Acyclic Graph) los cuales se encargan
de darle una estructura y orden a las tareas programadas en Airflow, y con la carpera [functions](https://github.com/emeierd/ProyectoIngenieriaDatos/tree/main/extract/airflow/dags/functions), la cual contiene los script que serán ejecutados por Airflow:
* [datadiaria.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dags/functions/datadiaria.py) encargado de realizar el resumen del día anterior por cada ciudad dentro de data.csv - ejecutado cada día a las 4:00AM
* [extracciondata.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dags/functions/extracciondata.py) encargado de extraer la data desde la API del tiempo
* [producer.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dags/functions/producer.py) encargado de producir los mensajes de Kafka producer al topic *projectotiempo* - ejecutado todos los días cada 60 minutos
* [data.csv](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f87015b2d33a059b83d57bebcae5834df89709b9/extract/airflow/dags/functions/data.csv) es la data transformada que contiene las ciudades con sus respectivas temperaruras y precipitaciones por fecha

En cada uno de estos script se encuentra la explicación de su código, por lo cual no serán abordados en este apartado.

Una vez que ya tenemos una noción de lo que es Airflow, procedemos a arrancarlo mediante Docker compose, para esto ejecutamos el siguiente comando dentro de la carpeta airflow:\
**docker-compose up --build**
*ejemplo: C:\ProyectoIngenieriaDatos\extract\airflow> docker-compose up --build*
Este comando creará los dos contenedores necesarios para el funcionamiento de airflow (postgres y webserver) y también una *red docker* llamada **airflow_default**, la cual
utilizaremos más adelante para conectar nuestros contenedores de Kafka y Zookeeper. Ya arriba los dos contenedores podemos ingresar a Airflow desde nuestro navegador preferido
ingresando la siguiente dirección: *localhost:8080*, donde encontraremos los dos DAG que creamos con un *switch* en OFF, el cual dejaremos tal cual por ahora.


## Apache Kafka
poner que se tiene que conectar a red de airflow y poner pasos para crear los dos contenedores
Para Apache Kafka se crearán dos contenedores Docker, maquina1 y maquina2.\
**maquina1** será el contenedor que contenga Zookeeper, que es el encargado de manejar los distintos servidores o *brokers* de Kafka. Este es
imprescindible para que Apache Kafka funcione.\
**maquina2** será el contenedor que contenga un broker de Kafka, el cual se conectará a Zookeeper arrancado en el contenedor maquina1. Si se quisiera
se pueden crear más contenedores con broker de Kafka, con el fin de distribuir cargas de trabajo, en este caso solo se utilizó un broker, ya que el
proyecto tiene fines de probar herramientas.

Cabe mencionar que los siguentes pasos son ejecutados en Linux, para Windows deben realizar los pasos equivalentes mediante la UI de Windows y ejecutar los script
de Kafka dentro de la carpeta windows, por ejemplo *C:\Kafka\bin\windows\kafka-server-start.bat*

Para crear los contenedores se debe ejecutar lo siguiente, una ventana de línea de comandos por contenedor:
1. docker run --name maquina1 -it ubuntu:latest
2. docker run --name maquina2 -it ubuntu:latest
3. En una ventana distinta ejecutar lo siguente para cambiar de red a los contenedores
  3.1 docker network disconnect bridge maquina1
    3.1.1 docker network connect airflow_default maquina1
  3.2 docker network disconnect bridge maquina2
    3.2.1. docker network connect airflo_default maquina2
4. En ambas máquinas ejecutar
  4.1. apt update && apt install -y nano openjdk-8-jre wget
  4.2. wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz
  4.3. tar -xzf kafka_2.13-2.8.0.tgz 
  4.4. cat /etc/hosts
5. En máquina1 ejecutar
  5.1. nano kafka_2.13-2.8.0/config/zookeeper.properties
  5.2. dataDir=/kafka_2.13-2.8.0/zookeeper-logs  
  5.3. mkdir kafka_2.13-2.8.0/zookeeper-logs
  5.4. kafka_2.13-2.8.0/bin/zookeeper-server-start.sh kafka_2.13-2.8.0/config/zookeeper.properties
6. En máquina2 ejecutar  
  6.1. nano kafka_2.13-2.8.0/config/server.properties
  6.2. zookeeper.connect=ipmaquina1:2181
  6.3. listener=PLAINTEXT://ipmaquina2:9092
  6.4. log.dirs=kafka_2.13-2.8.0/kafka-logs
  6.5. kafka_2.13-2.8.0/bin/kafka-server-start.sh kafka_2.13-2.8.0/config/server.properties
    
Estos pasos se pueden encontrar en [extract/pasoskafka.txt](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/main/extract/pasoskafka.txt).

Con esto ya tenemos Kafka operativo, se debe recordar la ip de maquina2, ya que será necesaria para conectar los Kafka producer y consumer
en los script python.

En este proyecto se utiliza Kafka para utilizar un producer, el cual producirá mensajes con la data obtenida desde la API del tiempo, luego habrá un
consumer, el cual leerá esta data en formato json y realizará una *request post* para comunicarse con la API Flask, la cual se encargará de almacenar
los datos en SQL Server

## Python
Python es el lenguaje de programación escogido, debido a que contiene una serie de módulos que facilitan el trabajo con la data, además es el lenguaje de 
programación que ocupa Apache Airflow.

### Paquetes o módulos requeridos
* **pandas** utilizado para leer los csv y transformar la data(eliminar, agregar columnas), etc.
* **pyodbc** utilizado para hacer la conexión con SQL Server.
* **flask** utilizado para crear la API que funcionará como intermermediario para las distintas tareas.
* **collections** utilizado para obtener llaves y valores únicos de una *dataframe* de pandas.
* **datetime** utilizado para manejar fechas.
* **kafka - kafka-python** kafka-python es el módulo que se debe instalar mediante *pip install kafka-python*, luego para utilizarlo en python se debe importar el paquete kafka. Este es necesario para hacer las conexiones con los *broker* de Kafka.
* **json** utilizado para decodificar los mensajes de la API en formato json.
* **bson - pymongo** se debe instalar el módulo pymongo mediante *pip install pymongo* para poder utilizar el paquete bson en python. Este se utiliza para codificar los mensajes del Kafka producer en formato json.
* **requests** utilizado para realizar consultas a las API, para así obtener datos de esta o mandar consultas POST a la API Flask para que esta se comunique con la base de datos.

### Flask
El código para la API Flask lo encontramos en [flask/app.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f98dc3ec1ff89ddcc4984e3e952821104139c2a4/flask/app.py), en la que encontramos una serie de métodos. Se designó como *host* la ip propia de la máquina en la red local y no *localhost*, de no ser así los contenedores de Docker no podrían comunicarse con la API, también es escogió el puerto 8090, ya que el puerto 8080 está ocuparo por Airflow.

Los métodos que encontramos en la API son los siguentes:
* **/** *GET* que es la dirección por defecto y nos devuelve un mensaje de bienvenida, *ejemplo 192.168.1.64:8090/*
* **/tiempo/id** *GET* nos devuelve todos los datos sobre la *id*(nombre de la ciudad) ingresada, comenzando con mayúscula y reemplazando los espacios por _, *ejemplo 192.168.1.64:8090/tiempo/Puerto_Montt*
*  **tiempo/id/24h** *GET* nos devuelve los datos del día anterior sibre ka *id*(nombre de la ciudad) ingresada, comenzando con mayúscula y reemplazando los espacios por _, *ejemplo 192.168.1.64:8090/tiempo/Puerto_Montt/24h*
*  **/tiempo** *POST* obtiene los datos en formato json que fueron enviados por la consulta y los transforma para crear una *query* hacia la base de datos de SQL Server. Es utilizado por el script [extract/kafkaconsumer.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f98dc3ec1ff89ddcc4984e3e952821104139c2a4/extract/kafkaconsumer.py) par guardar las temperaturas y precipitaciones de las ciudades cada hora.
*  **tiempo/id/resumen_dia** *GET* muestra el resumen del día anterior sobre la *id*(nombre de la ciudad) ingresada, comenzando con mayúscula y reemplazando los espacios por _, *ejemplo 192.168.1.64:8090/tiempo/Puerto_Montt/resumen_dia*
*  **tiempo/resumen_dia** *POST* obtiene los datos en formato json que fueron enviados por la consulta y los transforma para crear una *query* hacia la base de datos e SQL Server. Es utilizado por el script [extract/airflow/dags/functions/datadiaria.py](https://github.com/emeierd/ProyectoIngenieriaDatos/blob/f98dc3ec1ff89ddcc4984e3e952821104139c2a4/extract/airflow/dags/functions/datadiaria.py) para extraer las temperaturas mínimas, máximas y precipitaciones totales de las ciudades y luego guardarlas en la base de datos.
*  **tiempo/comparar/id** *GET* realiza una comparación del día anterior de las precipitaciones y temperaturas, entre la data obtenida desde la API del tiempo y la data en formato .csv sobre la *id*(nombre de la ciudad) ingresada, comenzando con mayúscula y reemplazando los espacios por _, *ejemplo 192.168.1.64:8090/tiempo/comparar/Puerto_Montt*

# Origen de los datos
## Temperaturas
https://datos.gob.cl/dataset/32806/resource/3572bdac-96f7-409f-8e6f-712b8a9cd245

## Precipitaciones
https://datos.gob.cl/dataset/2719/resource/1994cc0d-3ab0-4493-8740-698392e1add5

## API Tiempo
https://www.tomorrow.io/
