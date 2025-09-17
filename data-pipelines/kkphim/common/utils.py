import requests
import random
import json
import os
import psycopg2
import sys
import pandas as pd

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Now you can import connection_params
from connection_params import postgres_params

class PostgreUtils:
    @staticmethod
    def execute_query(input_query):
        # Connect ot PostgreSQL
        conn = psycopg2.connect(**postgres_params)

        # create a cursor
        cur = conn.cursor()

        try:
            # Execute the query
            cur.execute(input_query)

            # commit the transaction
            conn.commit()
            print('Execute query successfully!!!')
        
        except Exception as e:
            # rollback in case of error
            conn.rollback()
            print('Error occured:', e)
        
        finally:
            # close the cursor and connection
            cur.close()
            conn.close()

    @staticmethod
    def fetch_data(input_query):
        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(**postgres_params)

            # use pandas to read SQL directly into a Dataframe
            df = pd.read_sql_query(input_query, conn)

            return df
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            # close the connection
            if conn:
                conn.close()

class Kkphim:

    base_url = "https://phimapi.com/danh-sach/phim-moi-cap-nhat?page=" # class attribute

    @staticmethod
    def get_items(page_id):
        # This function gets data given page_id from kkphim

        # URL of the API
        url = Kkphim.base_url + str(page_id)

        # Send a GET request to the API
        response = requests.get(url)

        # check if the request was successful
        if response.status_code == 200:
            # parse the JSON data
            data = response.json()

            return data
        
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    @staticmethod
    def find_page_id(given_timestamp):
        # given timestamp get the page_id such that
        # items[0]['modified']['time'] >= given_timestamp >= items[-1]['modified']['time']

        start_page = 1
        tmp_page_id = random.randint(1,200)
        tmp_data = Kkphim.get_items(tmp_page_id)
        end_page = tmp_data['pagination']['totalPages']

        # using binary search to find the page_id
        while start_page < end_page:
            investigated_page = (start_page + end_page) // 2

            tmp_data = Kkphim.get_items(investigated_page)
            
            # get first_item and last_item in the investigated_page
            first_item = tmp_data['items'][0]
            last_item = tmp_data['items'][-1]

            # get modified time of the first_item and last_item
            first_item_modified_time = first_item['modified']['time']
            last_item_modified_time = last_item['modified']['time']

            if (first_item_modified_time >= given_timestamp) \
                and (given_timestamp >= last_item_modified_time):
                return investigated_page
            elif given_timestamp > first_item_modified_time:
                end_page = investigated_page - 1
            else: # last_item_modified_time > given_timestamp
                start_page = investigated_page + 1

        return start_page

    @staticmethod
    def crawl_data(start_page_id, end_page_id):

        start_idx = min(start_page_id, end_page_id)
        end_idx = max(start_page_id, end_page_id)
        
        for page_id in range(start_idx, end_idx+1):
            data = Kkphim.get_items(page_id)

            page_id = str(page_id).zfill(6)
            filename = 'page_' + page_id + '.json'
            relative_path = '../temp/raw_items/' + filename

            # Ensure the directory exists
            os.makedirs(os.path.dirname(relative_path), exist_ok=True)

            with open(relative_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            print(f"Data saved to {filename}")