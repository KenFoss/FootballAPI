import csv
import json
import os
import pandas as pd
import sys

def get_headers():
    '''
    Get the headers for all the file types this will be the sql tables
    '''

    table_headers = {
        'passing_stats' : ['year'],
        'rushing_stats' : ['year'],
        'receiving_stats' : ['year'],
        'fantasy_stats' : ['name', 'fantasy_pts']
    }


    script_directory = os.path.dirname(os.path.abspath(__file__))

    for root, dirs, files in os.walk(f'{script_directory}/pff_data'):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            df = pd.read_csv(file_path)
            headers = list(df.columns)
            
            if len(table_headers['passing_stats']) == 1 and 'passing_stats' in file_name:
                for header in headers:
                    table_headers['passing_stats'].append(header)
            elif len(table_headers['rushing_stats']) == 1  and 'rushing_stats' in file_name:
                for header in headers:
                    table_headers['rushing_stats'].append(header)
            elif len(table_headers['receiving_stats']) == 1  and 'receiving_stats' in file_name:
                for header in headers:
                    table_headers['receiving_stats'].append(header)
            # csv_to_json(file_path, f'{script_directory}/pff_data/json/{os.path.splitext(file_name)[0]}.json')
    
    json_file = open(f'{script_directory}/pff_data/json/headers.json', 'w')
    json.dump(table_headers, json_file, indent=4)



if __name__ == '__main__':
   sys.exit(get_headers())