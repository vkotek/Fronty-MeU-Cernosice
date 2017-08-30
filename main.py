import requests, re, datetime
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup as bs

# Retrieve HTML data
url = "http://ke.customer.decent.cz/a022/mon/"
filename = "meu_data.xlsx"

soup = bs(requests.get(url).content, 'html5lib')
tables = soup.find_all('table')

# Get and format timestamp from first table.
raw_datetime = tables[2].get_text()
date = re.search(r'(\d+).(\d+).(\d+)', raw_datetime)
time = re.search(r'(\d\d)\s(\d\d)', raw_datetime)

# Create datetime object from data, not very pretty..
timestamp = datetime.datetime(
    int(date.group(3)),
    int(date.group(2)),
    int(date.group(1)), 
    int(time.group(1)),
    int(time.group(2)))

# Get data and import it into a Pandas DataFrame, format it.
raw_data = tables[4]
rows = raw_data.find_all('tr')
rows = [x.find_all('td') for x in rows]
data = [[col.get_text() for col in row] for row in rows]

headers = ['activity', 'queue', 'x','active_booths', 'wait_time','x']
table = pd.DataFrame( data[1:], columns=headers).set_index('activity')[:11]
table = table.drop('x', axis=1)

tables = {}

for col in table:
    tables[col] = pd.DataFrame(table[col].str.extract("(\d+)", expand=False).fillna('0'))
    tables[col].columns = [timestamp]
    tables[col] = tables[col].transpose()

# Create 3D array with queue, open booths, and wait time.
data_current = pd.Panel(tables)

data_old = {}

# Check if file exists
if Path.is_file(Path(filename)):
    
    # Load excel, each sheet to separate dataframe and create Panel
    excel_data = pd.read_excel(filename, sheetname=None, header=0, index_col=0)
    excel_data = pd.Panel(excel_data)

    
    for sheet in table_base:
        data_old[sheet] = excel_data[sheet].append(data_current[sheet])


        
data_merged = pd.Panel(data_old)

data_merged.to_excel(filename)
