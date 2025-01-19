from database.db_helper import init_table
#from scraper import get_all_gym_names

#list_names = get_all_gym_names()
list_names = ['helen_newman']
for name in list_names:
    init_table(name)