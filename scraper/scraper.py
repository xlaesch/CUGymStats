import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
import sqlite3

ua = UserAgent() #to bypass Mod_Security --> bot prevention

headers = {
    'User-Agent' : ua.random
}

#TODO: get all sibling elements of <div class="panel-body"> parent. currently getting first (which is helen newman)

url = os.environ.get('url')

if url:
    r = requests.get(url, headers=headers)
else:
    raise Exception("Please specify the url in environment variables. Variable name 'url'.")

print(r) #gives status code of response received, 200 --> successful response

#Parse the HTML
soup = BeautifulSoup(r.content, 'html.parser')

#Helen Newman Data Extraction
helen_newman_data = soup.select_one('.col-md-3.col-sm-6 .circleChart')
print(helen_newman_data)

#TODO: make sure to get the timestamp as well

if helen_newman_data:
    data_lastcount = helen_newman_data.get('data-lastcount')
    data_percent = helen_newman_data.get('data-percent')
else:
    print('Element not found.')
    
data_lastcount = 40
data_percent = 50
data_timestamp = "2025-01-14 18:17:54"

print(data_lastcount,data_percent)

#TODO: save data in a database with date included
con = sqlite3.connect("database/data.db") # connection to the db
cur = con.cursor() #cursor creation

# Create table if it does not exist
cur.execute('''CREATE TABLE IF NOT EXISTS helen_newman
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                lastcount INTEGER,
                percent INTEGER,
                timestamp TEXT)''')

cur.execute("INSERT INTO helen_newman(lastcount, percent, timestamp) VALUES (?,?,?)", (data_lastcount,data_percent,data_timestamp))
con.commit()
con.close()




    