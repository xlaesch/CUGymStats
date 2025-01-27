import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

ua = UserAgent() #to bypass Mod_Security --> bot prevention
load_dotenv()

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
    
    print(soup)

    #Helen Newman Data Extraction
    circle_charts = soup.find_all('div', class_='circleChart')
    
    if circle_charts:

        # Extract and print data attributes along with the facility name
        for chart in circle_charts:
            data_fcolor = chart.get('data-fcolor')
            data_lastcount = chart.get('data-lastcount')
            data_percent = chart.get('data-percent')
            data_isclosed = chart.get('data-isclosed')

            # The facility name is in the sibling or parent structure, find it
            facility_name_div = chart.find_next('div', style="text-align:center;")
            facility_name = facility_name_div.text.split('\n')[0].strip() if facility_name_div else "Unknown"

            print(f"Facility Name: {facility_name}")
            print(f"Color: {data_fcolor}")
            print(f"Last Count: {data_lastcount}")
            print(f"Percentage: {data_percent}")
            print(f"Is Closed: {data_isclosed}")
            print("-" * 20)

    else:
        return "No elements found!"

        
    data = {
        'location' : 'helen_newman',
        'data_lastcount' : 40,
        'data_percent' : 50,
        'data_timestamp' : "2025-01-14 18:17:54"
    } #how all data should be saved from parsed html
    #! using testing data for the moment
        
    if debug:
        '''print(soup)
        print(data)'''
    
    return data #TODO: use selenium to parse the HTML since the elements have been changed to be dynamically genetated using js

def get_all_gym_names():
    pass #TODO: helper function to find out how many tables to create and put names in list

if __name__ == "__main__":
    r=get_raw_html(debug=True)
    print(parse_html(r,debug=True))
    
    
    
    
    