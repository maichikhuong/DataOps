import json
import os
import sys

sys.path.append('../common')
from utils import PostgreUtils

def get_insert_query(table_name, tmp_li):
    str_li = []
    for item in tmp_li:
        modified_time = str(item['modified']['time'])
        _id = str(item['_id'])
        name = str(item['name']).replace("'", "''")
        slug = str(item['slug'])
        origin_name = str(item['origin_name']).replace("'", "''")
        poster_url = str(item['poster_url'])
        thumb_url = str(item['thumb_url'])
        year = str(item['year'])

        tmp_str = ', '.join([
            "'" + modified_time + "'"
            , "'" + _id + "'"
            , "'" + name + "'"
            , "'" + slug + "'"
            , "'" + origin_name + "'"
            , "'" + poster_url + "'"
            , "'" + thumb_url + "'"
            , "'" + year + "'"
        ])

        tmp_str = '(' + tmp_str + ')'
        str_li.append(tmp_str)

    four_indent_str = '    '
    insert_query = f"INSERT INTO {table_name} (modified_time, _id, name, slug, origin_name, poster_url, thumb_url, year)\n"
    insert_query += "VALUES\n"
    for i, str_value in enumerate(str_li):
        if i != len(str_li) - 1:
            insert_query += four_indent_str + str_value + ',\n'
        else:
            insert_query += four_indent_str + str_value

    return insert_query


def bulk_delete(tmp_li):
    print('Delete files in tmp_li from local directory')

def main(args):
    # global args
    
    refresh = args['refresh']

    # Define the path to the directory
    directory_path = args['directory_path']
    # directory_path = '../temp/raw_items'

    # table_name = 'kkphim.items'
    table_name = args['table_name']

    if refresh:
        print('######## Refreshing data ########')
        query = f'TRUNCATE TABLE {table_name}'
        PostgreUtils.execute_query(query)

    # List all files in the directory
    files = os.listdir(directory_path)

    # Filter out directories, keeping only files
    files = [file for file in files if os.path.isfile(os.path.join(directory_path, file))]

    tmp_li = []

    batch_idx = 0
    for f in files:
        # Define the path to json files
        json_file_path = directory_path + '/' + f
        
        # load the json file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        tmp_li += data['items']
        
        # batch insert for each 1000 records
        if len(tmp_li) == 1000:

            # do batch insert to postgres
            batch_idx += 1
            print(f'######## Start batch-inserting for {batch_idx}-th batch ########')
            insert_query = get_insert_query(table_name, tmp_li)
            PostgreUtils.execute_query(insert_query)

            # do delete files in tmp_li from local directory
            # bulk_delete(tmp_li)

            # reset tmp_li to be empty
            tmp_li = []


    if len(tmp_li) != 0:
        # do bulk insert to postgres the remaining records in tmp_li
        batch_idx += 1
        print(f'######## Start batch-inserting for {batch_idx}-th batch ########')
        insert_query = get_insert_query(table_name, tmp_li)
        PostgreUtils.execute_query(insert_query)

    #     # do delete files in tmp_li from local directory
    #     print('Delete files in tmp_li from local directory')

if __name__ == "__main__":
    args = {
        'refresh': True,
        'directory_path': '../temp/raw_items',
        'table_name': 'kkphim.items'
    }

    main()

    