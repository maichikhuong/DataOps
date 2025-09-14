import warnings 
warnings.filterwarnings('ignore')
import os
import sys

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


## import key connect to duckdb
sys.path.insert(0, 'DataOps')
from connection_params import duckdb_token
## import stock data-pipeline
sys.path.insert(0, 'DataOps/data-pipelines/stock/py-files')
from call_get_data_daily import get_data_daily
sys.path.insert(0, 'DataOps/data-pipelines/stock/common')
from utils import create_insert_table

default_args = {
    'owner': 'Khuong',  
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}


@dag(dag_id = 'stock_mlops_pl_daily',
    default_args = default_args,
    start_date=datetime(2025, 9, 14, 2, 0),  # <-- 02:00 UTC = 09:00 VN
    schedule_interval="0 2 * * *", # run every day at 02:00 UTC
    catchup=False,  
    tags = ['binance stock', 'mlops']
     )
def etl_pipeline():
    with TaskGroup(group_id="etl_group") as etl_group:
        @task
        def get_data(ti):
            ti.xcom_push(key = 'stock_data', value = get_data_daily())
            
        @task
        def create_insert_data(ti):
            create_insert_table(ti.xcom_pull(task_ids = 'etl_group.get_data', key = 'stock_data'))
            
        get_data() >> create_insert_data()
    
    etl_group

dag = etl_pipeline()

