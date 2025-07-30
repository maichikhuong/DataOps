from airflow.decorators import dag, task 
from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'Khuong',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}


@dag(dag_id = 'our_first_dag',
    default_args = default_args,
    start_date = None,
    schedule_interval = None, 
    tags = ['test enviroment']
     )
def etl_pipeline():

    # kkphim task
    @task
    def greet():
        a = 10
        print(a)
        
    greet()

dag = etl_pipeline()