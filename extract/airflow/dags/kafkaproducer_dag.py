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
    dag_id="kafkaproducer_dag",
    schedule_interval="*/60 * * * *",
    default_args= default_args,
    start_date = datetime(2020,6,23),
    catchup=False
) as f:
    producer = BashOperator(
    task_id="producer",
    bash_command="python3 /usr/local/airflow/dags/functions/producer.py")    


producer