# ProyectoIngenieriaDatos
Este es un proyecto en donde se ocupan una serie de herramientas de ingeniería de datos con el fin de mostrar su uso. 
* Se transformarán datos desde archivos .csv, los cuales utilizados para distintas tareas.
* Se extraerán datos de una API de tiempo, que muestra temperaturas y precipitaciones. Esto en base a los datos del punto anterior.
* Estos datos extraídos serán enviados a través de Kafka producer
* Se almacenarán datos en una base de datos
* Se hará una comparación de estos datos con los datos 
* Seguir explicando como funciona paso a paso

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


## Flask

## Python
### Paquetes requeridos

# Origen de los datos
## Temperaturas
https://datos.gob.cl/dataset/32806/resource/3572bdac-96f7-409f-8e6f-712b8a9cd245

## Precipitaciones
https://datos.gob.cl/dataset/2719/resource/1994cc0d-3ab0-4493-8740-698392e1add5
