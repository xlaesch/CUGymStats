import sys
from database.db_helper import init_table, insert_new_data
from scraper.scraper import *

scraped_data = parse_html_with_selenium()

'''if sys.argv[1] == '-s':  # Checking to see if it's the first time running and if tables need to be initialized
    data_names = list(scraped_data.keys())
    for name in data_names:
        init_table(name)''' #TODO: Fix!

insert_new_data(scraped_data)

