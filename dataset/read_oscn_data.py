import json
import os
import sys

import pandas as pd

def initialize(data):
    pandas_dict = {}
    for key in data.keys():
        pandas_dict[key] = []
    return pandas_dict

def change_file_name_extension(file_name):

    file_name_parts = file_name.split('.')
    file_name_parts[1] = '.csv'
    return ''.join(file_name_parts)

def main():
    path = f'{os.getcwd()}/'
    file_name = sys.argv[1]
    file_name_with_path = f'{path}{file_name}'
    target_dataset = []

    with open(file_name_with_path) as r:
        data = r.read()
        pythoninc_data = json.loads(data)
        for datumset in pythoninc_data:
            for key, datum in datumset.items():
                if key == "events" and datum:
                    target = []
                    for each_event in datum:
                        target.append({**{"case_index":datumset["case_index"]}, **each_event})
                    target_dataset.extend(target)
    
    pandas_dict = initialize(target_dataset[0])
    for data in target_dataset:
        for key, datum in data.items():
            pandas_dict[key].append(datum)
    

    event_data_set = pd.DataFrame.from_dict(target_dataset)
    event_data_set = event_data_set.drop_duplicates()
    event_data_set.to_csv(f'{path}/{change_file_name_extension(file_name)}')
        
if __name__ == "__main__":
    main()