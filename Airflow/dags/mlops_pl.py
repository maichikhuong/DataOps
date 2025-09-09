import warnings 
warnings.filterwarnings('ignore')
import os
import sys

from airflow.decorators import dag, task 
from datetime import datetime, timedelta
import pendulum
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


## import key connect to duckdb
sys.path.insert(0, 'DataOps')
from connection_params import duckdb_token
## import stock data-pipeline
sys.path.insert(0, 'DataOps/data-pipelines/stock/py-files')
from call_get_data import get_api
sys.path.insert(0, 'DataOps/data-pipelines/stock/common')
from utils import create_insert_table


default_args = {
    'owner': 'Khuong',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}


@dag(dag_id = 'pl_mlops',
    default_args = default_args,
    start_date = None,
    schedule_interval = None, 
    tags = ['mlops', 'binance stock']
     )
def etl_pipeline():

    # kkphim task
    @task
    def get_data():
        result = get_api()
        print(result)
    
    @task
    def create_insert_data():
        result = get_api()
        create_insert_table(result)
        
    get_data() >> create_insert_data()

dag = etl_pipeline()

