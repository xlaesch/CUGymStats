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


def get_raw_html(debug=False):
    url = os.environ.get('url')

    if url:
        r = requests.get(url, headers=headers)
    else:
        raise Exception("Please specify the url in environment variables. Variable name 'url'.")

    if debug:
        print(r) #gives status code of response received, 200 --> successful response
    
    return r

def parse_html(r, debug=False):

    #Parse the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    #Helen Newman Data Extraction
    helen_newman_data = soup.select_one('.col-md-3.col-sm-6 .circleChart')
    print(helen_newman_data)

    if helen_newman_data: # ! does not work for now
        data_lastcount = helen_newman_data.get('data-lastcount')
        data_percent = helen_newman_data.get('data-percent')
    else:
        print('Element not found.')
        
    data = {
        'location' : 'helen_newman',
        'data_lastcount' : 40,
        'data_percent' : 50,
        'data_timestamp' : "2025-01-14 18:17:54"
    } #how all data should be saved from parsed html
    #! using testing data for the moment
        
    if debug:
        print(data)
    
    return data

def get_all_gym_names():
    pass #TODO: helper function to find out how many tables to create and put names in list

if __name__ == "__main__":
    pass