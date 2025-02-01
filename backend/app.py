import sys
from database.db_helper import init_table
from scraper.scraper import *

scraped_data = parse_html_with_selenium()

if sys.argv[1]: #Checking to see if it's the first time running and to see if tables have to be initialized
    data_names = list(scraped_data.keys())
    for name in data_names:
        init_table(name)

