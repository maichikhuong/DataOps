from airflow.decorators import dag, task 
from datetime import datetime, timedelta
import pendulum
from airflow import DAG 
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import os
import sys

## import kkphim data-pipeline
sys.path.insert(0, 'phimville/data-pipelines/kkphim/py-files')
sys.path.insert(0, 'phimville/data-pipelines/kkphim/common')
from utils import PostgreUtils
# from backfill_load_step_1 import main as kkphim_ft_backfill_step_1
# from backfill_load_step_2 import main as kkphim_ft_backfill_step_2


default_args = {
    'owner': 'Khuong',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}


@dag(dag_id = 'phimville_pl',
     default_args = default_args,
     start_date = None,
     schedule_interval = None, 
     params = {
        "start_time": None,
        "end_time": None,
        'refresh': True,
        'directory_path': {
            'kkphim': 'temp/kkphim/raw_items',
            'ophim': 'temp/ophim/raw_items'
            },
        'table_name': {
            'kkphim': 'kkphim.items',
            'ophim': 'ophim.items'
            }
        },
    tags = ['phimville_pl', 'parameterized']
     )
def etl_pipeline():

    # kkphim task
    @task
    def kkphim_backfill_step_1(params):
        args = params
        kkphim_ft_backfill_step_1(args = args)
    
    @task
    def kkphim_backfill_step_2(params):
        args = params
        sql_script = open('phimville/data-pipelines/kkphim/ddl-files/changelog_01.sql', 'r').read()
        PostgreUtils.execute_query(sql_script)
        kkphim_ft_backfill_step_2(args = args)        

    kkphim_backfill_step_1() >> kkphim_backfill_step_2()
    

dag = etl_pipeline()