from database.db_helper import init_table
from scraper.scraper import *
#from scraper import get_all_gym_names

#list_names = get_all_gym_names()
scraped_data = parse_html_with_selenium()
data_names = list(scraped_data.keys())

for name in data_names:
    init_table(name)