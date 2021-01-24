
import json
import requests


def get_days():
    days = []
    for i in range(1,32):
        if i < 10:
            days.append('0'+str(i))
        else:
            days.append(str(i))
    return days

month = ['12', '01']
days = get_days()
year = ['2020', '2021']

def get_response(month, day, year):
    response = requests.get(f'https://www.oscn.net/dockets/Results.aspx?db=all&number=&lname=&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=&FiledDateL={month}%2F{day}%2F{year}&FiledDateH=&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=')
    if response.status_code == 200:
        text_lines = response.text.split('\n')
        return text_lines
    else:
        return None

def store_case_number(keys, case_num_dict, month, day, year):
    print(month)
    print(day)
    print(year)
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

keys = []
case_num_dict = {}

for i in range(len(month)):
    if i == 0:
        for j in range(len(days)):
            print(j)
            keys, case_num_dict = store_case_number(keys, case_num_dict, month[i], days[j], year[i])
    else:
        for j in range(21):
            print(j)
            keys, case_num_dict = store_case_number(keys, case_num_dict, month[i], days[j], year[i])

case_num_dict = change_set_to_tuple(case_num_dict)
json_data = json.dumps(case_num_dict)

with open("dataset.txt", "w") as w:
    w.write(json_data)

python_data = None
with open("dataset.txt", "r") as r:
    text = r.read()
    python_data = json.loads(json_data)

for key, data in python_data.items():
    print(key)
    print(data)

