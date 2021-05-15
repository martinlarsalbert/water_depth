import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
import datetime
import os

def get_data_from_response(response)->pd.Series:
    
    xml = response.text
    root = ET.fromstring(xml)

    df_data = pd.DataFrame()

    regexp = re.compile('\{[^}]*\}')


    for value in root.findall('{https://opendata.smhi.se/xsd/ocobs_v1.xsd}value'):

        s = pd.Series()

        for data in value:
            key = regexp.sub('', string = data.tag)
            s[key] = data.text

        s.name = s.date

        df_data = df_data.append(s)

    df_data.drop(columns=['date'], inplace=True)
    df_data.index = pd.to_datetime(df_data.index)
    data_depth = df_data['value'].astype('float')

    return data_depth

def request(station:int=2110, url = r'https://opendata-download-ocobs.smhi.se/'):
    response = requests.get(f'{url}api/version/latest/parameter/6/station/{station}/period/latest-day/data.xml')
    return response

def get(station:int=2110)->pd.Series:
    response = request(station=station)
    data_depth = get_data_from_response(response=response)
    return data_depth

def run(save_dir_path = 'data/raw'):

    if not os.path.exists(save_dir_path):
        os.mkdir(save_dir_path)
    
    station = 2110  ## (Stenungsund)
    print('request water depth')
    data_depth = get(station=station)
    
    now = datetime.datetime.now()
    file_name = f'station_{station}_{now}.json'
    file_path = os.path.join(save_dir_path, file_name)
    print(f'Saving to:{file_path}')
    data_depth.to_csv(file_path)

if __name__ == '__main__':
    run()
