import sys
from database.db_helper import init_table, insert_new_data
from scraper.scraper import *

hours={
    'Helen Newman Fitness Center': (6, 21),
    'Noyes Fitness Center': (7,23),
    'Teagle Down Fitness Center': (7,22),
    'Teagle Up Fitness Center': (7,22),
    'Toni Morrison Fitness Center': (14,23),
    'HNH Court 1 Basketball' : (6,21),
    'HNH Court 2 Volleyball/Badminton': (6,21),
    'Noyes Court Basketball' : (6,21)
}

scraped_data = parse_html_with_selenium()

'''if sys.argv[1] == '-setup':  # Checking to see if it's the first time running and if tables need to be initialized
    data_names = list(scraped_data.keys())
    for name in data_names:
        init_table(name)''' #TODO: Fix!

insert_new_data(scraped_data)

