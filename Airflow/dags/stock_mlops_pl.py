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


@dag(dag_id = 'stock_mlops_pl',
    default_args = default_args,
    start_date = None,
    schedule_interval = None, 
    tags = ['binance stock', 'mlops']
     )
def etl_pipeline():

    @task
    def get_data(ti):
        results = get_api()
        print(results)
        # ti.xcom_push(key = 'stock_data', value = results)
        
    @task
    def create_insesrt_data(ti):
        # results = ti.xcom_pull(task_ids = 'get_data', key = 'stock_data')
        # print(results)
        results = get_api()
        print(results)
        create_insert_table(results)
        
    get_data() >> create_insesrt_data()

dag = etl_pipeline()

