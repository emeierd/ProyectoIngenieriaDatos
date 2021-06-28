try:
    from datetime import timedelta
    from airflow import DAG
    from datetime import datetime
    from airflow.operators.bash_operator import BashOperator

    print("All Dag modules are ok.....")
except Exception as e:
    print("Error {} ".format(e))    


default_args= {
        "owner":"airflow",
        "retries":2,
        "retry_delay": timedelta(minutes=1)
    }

with DAG(
    dag_id="resumen_24h_dag",
    schedule_interval="*/1440 * * * *",
    default_args= default_args,
    start_date = datetime(2020,6,30),
    catchup=False
) as f:
    resumen_24h = BashOperator(
    task_id="resumen_24h",
    bash_command="python3 /usr/local/airflow/dags/functions/datadiaria.py")    


resumen_24h