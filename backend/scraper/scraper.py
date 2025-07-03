from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

ua = UserAgent() #to bypass Mod_Security --> bot prevention

headers = {
    'User-Agent' : ua.random
}

# Load environment variables from .env file if it exists
load_dotenv()

url = os.getenv('url')
api_key = os.getenv('API_KEY')

if not url or not api_key:
    raise Exception("Please specify the URL and API_KEY in environment variables.")

def get_raw_html(debug=False):
    # Initialize Selenium WebDriver with headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Remove or comment out this:
    # options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Allow the page to fully load and JavaScript to render the content
    time.sleep(5)

    # Get the page source after rendering
    rendered_html = driver.page_source

    # Close the WebDriver
    driver.quit()

    if debug:
        print(rendered_html) # Print the rendered HTML for debugging

    return rendered_html

def parse_html_with_selenium(debug=False):
    rendered_html = get_raw_html(debug)
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(rendered_html, 'html.parser')

    # Find all circleChart divs
    circle_charts = soup.find_all('div', class_='circleChart')
    
    data_dic = {}

    if circle_charts:
        for chart in circle_charts:
            data_fcolor = chart.get('data-fcolor')
            data_percent = chart.get('data-percent')
            data_isclosed = chart.get('data-isclosed')

            # Find the sibling div that contains facility info
            facility_info_div = chart.find_next('div', style="text-align:center;")
            if facility_info_div:
                info_lines = list(facility_info_div.stripped_strings)
                facility_name = info_lines[0] if len(info_lines) > 0 else "Unknown"

                # Look for the line that starts with "Last Count:"
                last_count = "Unknown"
                for line in info_lines:
                    if "Last Count:" in line:
                        # Extract the count value after "Last Count:"
                        last_count = line.split("Last Count:")[1].strip().split()[0]
                        break
            else:
                facility_name = "Unknown"
                last_count = "Unknown"
            
            if debug:
                print(f"Facility Name: {facility_name}")
                print(f"Color: {data_fcolor}")
                print(f"Last Count: {last_count}")
                print(f"Percentage: {data_percent}")
                print(f"Is Closed: {data_isclosed}")
                print("-" * 20)
            
            data_dic[facility_name]=[last_count,data_percent,data_isclosed]
        
        return data_dic
            
    else:
        print("No elements found!")
        

# Example usage
if __name__ == "__main__":
    output=parse_html_with_selenium(debug=False)
    print(output)