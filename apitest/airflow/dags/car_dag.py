try:
    from datetime import timedelta
    from airflow import DAG
    from datetime import datetime
    from airflow.operators.python_operator import PythonOperator
    from functions.app import add_car

    print("All Dag modules are ok.....")
except Exception as e:
    print("Error {} ".format(e))    

def car_dag():
    print("running car_dag")
    json = {
    "brand" : "Test",
    "model" : "Test",
    "year" : 2021,
    "description" : "xD"
    }
    add_car(json)


default_args= {
        "owner":"airflow",
        "retries":2,
        "retry_delay": timedelta(minutes=1)
    }

with DAG(
    dag_id="car_dag",
    schedule_interval="*/1 * * * *",
    default_args= default_args,
    start_date = datetime(2020,4,23),
    catchup=False
) as f:
    car_dag = PythonOperator(
    task_id="car_dag",
    python_callable=car_dag)    


car_dag