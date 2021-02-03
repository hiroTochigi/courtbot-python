import json
import math
import os
import random
import sys
import time
import traceback

import oscn

ATTR_LIST = ['attorneys', 'case_index', 'case_number', 'closed', 'events', 'filed', 'issues', 'judge', 'number', 'offense', 'parties', 'path', 'pleas', 'response', 'sentences', 'type', 'valid',]
#ATTR_LIST = ['attorneys', 'case_index', 'case_number', 'closed', 'cmid', 'cmids', 'counts', 'county', 'directory', 'docket', 'events', 'filed', 'headers', 'issues', 'judge', 'number', 'offense', 'parties', 'path', 'pleas', 'response', 'save', 'sentences', 'type', 'valid', 'year']

EVENTS_ATTR_LIST = ['Docket', 'Event', 'Party', 'Reporter']

def log_traceback(ex):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    tb_text = ''.join(tb_lines)
    print(tb_text)

def get_event_list(case):

    event_list = []
    event_data_dict = {}
    for event in case.events:
            try:
                print(event)
                for attr in EVENTS_ATTR_LIST:
                    print(attr)
                    event_data_dict[attr] = eval(f"event.{attr}")
                event_list.append(event_data_dict)
            except:
                print(f"there is no {attr} attribute")
    if len(event_list)>0:
        return event_list
    return None
        
def replace_event_obj_event_list(attr, event_list, case):

    if attr == "event":
        return event_list
    return 

def read_data_from_file(file_name):
    try:
        with open(file_name, "r") as r:
            text = r.read()
            case_number_dict = json.loads(text)
        return case_number_dict
    except FileNotFoundError as ex:
        print(f'There is no {file_name}')
        log_traceback(ex)
    except Exception as ex:
        log_traceback(ex)

def change_file_name_extension(file_name):

    file_name_parts = file_name.split('.')
    file_name_parts[1] = '.json'
    return ''.join(file_name_parts)

def main():

    file_name = sys.argv[1]
    case_number_dict = read_data_from_file(file_name)

    index_list = {}
    for key, data in case_number_dict.items():
        index_list[key] = []
        for i in range(math.ceil(len(data)/1000)):
            if not index_list[key]:
                index_list[key].append(random.randint(0,len(data)-1))
            else:
                random_num = random.randint(0,len(data)-1)
                while random_num in index_list[key]:
                    random_num = random.randint(0,len(data)-1)
                index_list[key].append(random_num)

    data_list = []
    for county, ran_num_list in index_list.items():
        case_num_list = case_number_dict[county]
        for index in ran_num_list:
            year = case_num_list[index][3:7]
            case_num = case_num_list[index]
            time.sleep(2.5)
            try:
                case = oscn.request.Case(year=year, county=county, number=case_num)
                if case.events:
                    case_data_set = {attr:eval(f"case.{attr}", {}, {"case": case}) for attr in ATTR_LIST}
                    case_data_set["events"] = get_event_list(case)
                    data_list.append(case_data_set)
                else:
                    data_list.append({attr:eval(f"case.{attr}", {}, {"case": case}) for attr in ATTR_LIST})
            except Exception as ex:
                log_traceback(ex)
                print(f"Does not get data {case_num}")

    json_data = json.dumps(data_list)

    save_file_name = change_file_name_extension(file_name)
    with open(save_file_name, "w") as w:
        w.write(json_data)

if __name__ == "__main__":
    main()

"""
for data in data_list:
    for attr, val in data.items():
        print(f"{attr}:{val}")
    print()
"""