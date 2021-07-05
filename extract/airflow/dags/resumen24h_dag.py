# Este DAG será el que corra el script de que realizará el resumen del día anterior

# Se comprueba que los módulos se cargaron correctamente
try:
    from datetime import timedelta
    from airflow import DAG
    from datetime import datetime
    from airflow.operators.bash_operator import BashOperator

    print("All Dag modules are ok.....")
except Exception as e:
    print("Error {} ".format(e))    

# Se inicializan argumentos necesarios para Airflow
default_args= {
        "owner":"airflow",
        "retries":2,
        "retry_delay": timedelta(minutes=1)
    }

# Se inicializa el DAG, el cual será ejecutado todos los días a las 4AM hora servidor airflow o 12AM hora Chile
with DAG(
    dag_id="resumen24h_dag",
    schedule_interval="00 4 * * *",
    default_args= default_args,
    start_date = datetime(2020,7,3),
    catchup=False
) as f:
    # Se crea el operador 'resumen_24h' el cual correrá el script datadiaria.py
    resumen_24h = BashOperator(
    task_id="resumen_24h",
    bash_command="python3 /usr/local/airflow/dags/functions/datadiaria.py")    

# Se indica el flujo de tareas, como solo hay un operador, solo que indica 'resumen_24h'
resumen_24h