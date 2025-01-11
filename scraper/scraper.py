import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os


ua = UserAgent() #to bypass Mod_Security --> bot prevention

headers = {
    'User-Agent' : ua.random
}

url = os.environ.get('url', None)

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

if helen_newman_data:
    data_lastcount = helen_newman_data.get('data-lastcount')
    data_percent = helen_newman_data.get('data-percent')
else:
    print('Element not found.')    

print(data_lastcount,data_percent)

#TODO: save data in a database with date included



    