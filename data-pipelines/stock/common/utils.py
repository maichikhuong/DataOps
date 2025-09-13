import warnings 
warnings.filterwarnings('ignore')
import os
import sys
import duckdb
import pandas as pd
sys.path.append('../../..')
from connection_params import *
# initiate the MotherDuck connection through a service token through
conn = duckdb.connect(f"md:my_db?motherduck_token={duckdb_token}")

cur = conn.cursor()

def create_insert_table(value):
    global conn, cur
    try:
    
        create_script = """ CREATE TABLE IF NOT EXISTS BINANCE (
                                Pair_ID varchar(30),
                                Timestamp varchar(40),
                                Open float,
                                High float,
                                Low float,
                                Close float,
                                Volume float
        )
        """

        conn.sql(create_script)

        for record in value:
            conn.sql(f"""INSERT INTO BINANCE VALUES {record}""")
        print("Create and Insert Data Successfully!")

        
    except Exception as e:
        print(e)