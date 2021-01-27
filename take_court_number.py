
import json
import requests
import sys
from calendar import monthrange

import traceback

def print_traceback(ex):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    tb_text = ''.join(tb_lines)
    print(tb_text)


def get_date_range(year, month):

    year = None 
    month = None
    date_range = 0
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        date_range = monthrange(year, month)[1] + 1
        return date_range
    except ValueError:
        print("Enter number as argument")
        print_traceback(ex)
        return None
    except Exception as ex:
        print(ex)
        return None

def get_days(date_range):
    days = []
    for i in range(1,date_range):
        if i < 10:
            days.append('0'+str(i))
        else:
            days.append(str(i))
    return days

def get_response(month, day, year):
    response = requests.get(f'https://www.oscn.net/dockets/Results.aspx?db=all&number=&lname=&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=&FiledDateL={month}%2F{day}%2F{year}&FiledDateH=&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=')
    if response.status_code == 200:
        text_lines = response.text.split('\n')
        return text_lines
    else:
        return None

def store_case_number(keys, case_num_dict, month, day, year):

    text_lines = get_response(month, day, year)
    if not text_lines is None:
        for text in text_lines:
            if text.find("<a href") > 0 and text.find("class") == -1:
                start = len('    <td><a href="GetCaseInformation.aspx?db=')
                pre_data = text[start:]
                if pre_data.find('&number')>0:
                    region = pre_data[:pre_data.find('&number')]
                    start = len(f'{region}&number=')
                    end = pre_data.find('&cmid')
                    case_number = pre_data[start:end]
                    print(case_number)
                    if not region in keys:
                        case_num_dict[region] = set()
                        keys.append(region)
                        case_num_dict[region].add(case_number)
                    else:
                        case_num_dict[region].add(case_number)
    return keys, case_num_dict

def change_set_to_tuple(case_num_dict):
    for region, case_num_list in case_num_dict.items():
        case_num_dict[region] = [case_num for case_num in case_num_list]
    return case_num_dict

def main():

    year = sys.argv[1]
    month = sys.argv[2]
    date_range = get_date_range(year, month)
    days = get_days(date_range)
    if date_range:
        keys = []
        case_num_dict = {}
        for j in range(len(days)):
            keys, case_num_dict = store_case_number(keys, case_num_dict, month, days[j], year)
        case_num_dict = change_set_to_tuple(case_num_dict)
        json_data = json.dumps(case_num_dict)

        with open(f"dataset-{month}-{year}.txt", "w") as w:
            w.write(json_data)
    else:
        print("something wrong")

if __name__ == "__main__":
    main()

"""
python_data = None
with open("dataset.txt", "r") as r:
    text = r.read()
    python_data = json.loads(json_data)

for key, data in python_data.items():
    print(key)
    print(data)
"""
