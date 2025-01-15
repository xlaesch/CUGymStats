#Temp file just to do certain tests of helper functions and such
try:
    from database.db_helper import insert_new_data
except ImportError:
    print("Error: Could not import 'insert_new_data' from 'database.db_helper'")

data = {
    'location' : 'helen_newman',
    'data_lastcount' : 12,
    'data_percent' : 12,
    'data_timestamp' : "2025-12-12 12:12:12"
}

insert_new_data(data)