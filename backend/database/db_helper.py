import sqlite3
from datetime import datetime

def get_db_connection():
    return sqlite3.connect("backend/database/data.db")

def init_table(table_name: str):
    con = get_db_connection()
    cur = con.cursor()

    # Create table if it does not exist
    cur.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}"
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastcount INTEGER,
                    percent INTEGER,
                    timestamp TEXT,
                    dayofweek INTEGER,
                    hour INTEGER)''')
    
    con.close()

def tables_exist(table_names):
    con = get_db_connection()
    cur = con.cursor()
    for table_name in table_names:
        cur.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}' ''')
        if cur.fetchone() is None:
            con.close()
            return False
    con.close()
    return True

month_code_map = {
    '01' : 0,
    '02' : 3,
    '03' : 3,
    '04' : 6,
    '05' : 1,
    '06' : 4,
    '07' : 6,
    '08' : 2,
    '09' : 5,
    '10' : 0,
    '11' : 3,
    '12' : 5
}

century_code = 6 #assuming that this project will not be running once the 2000s century is over

def get_year_code(year: str)->int:
    yy = int(year[-2:]) #get last two digits and convert to int
    return (yy + (yy//4)) % 7

def get_leapyear_code(year: str)->int:
    year = int(year)
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return 1
    else:
        return 0

def get_day_of_week(year_code, month_code, century_code, date_number, leapyear_code):
    return (year_code + month_code + century_code + date_number - leapyear_code) % 7


def insert_new_data(scraped_data):
    """
    Accepts scraped_data as a dict where each key is a facility name and the corresponding value
    is a list: [last_count, percent, is_closed]. Inserts a new row into the 
    table corresponding to each facility.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    # Use weekday() where Monday=0, Sunday=6
    dayofweek = now.weekday()
    hour = now.strftime("%H")

    for facility, values in scraped_data.items():
        last_count, percent, is_closed = values
        
        print(f'Attempting connection to database for facility: {facility}...')
        con = get_db_connection()
        print('Successful connection!')
        cur = con.cursor()
        
        print('Attempting to insert new data...')
        cur.execute(
            f'''INSERT INTO "{facility}" (lastcount, percent, timestamp, dayofweek, hour)
                VALUES (?,?,?,?,?)''', 
            (last_count, percent, timestamp, dayofweek, hour)
        )
        con.commit()
        con.close()
        print(f'Successful insertion for facility: {facility}!')

def get_average_for_day(dayofweek):
    # Connect to database
    print('Attempting connection to database...')
    con = get_db_connection()
    print('Successful connection!')
    cur = con.cursor()
    
    # Find values for day of week
    print('Attempting to find data...')
    cur.execute('''SELECT hour, AVG(percent) AS avg_percentage
                FROM helen_newman 
                WHERE dayofweek = ?
                GROUP BY hour
                ORDER BY hour;''', (dayofweek))
    
    data = cur.fetchall()
    con.close()
    
    if data:
        print('Was able to find!')
    
    return data

def get_average_for_day_hour(dayofweek: int, hour: str)-> int:
    # Connect to database
    print('Attempting connection to database...')
    con = get_db_connection()
    print('Successful connection!')
    cur = con.cursor()
    
    # Find values for day of week
    print('Attempting to find data...')
    cur.execute('''SELECT AVG(percent)
                   FROM helen_newman
                   WHERE dayOfWeek = ? AND hour = ?, ''', (dayofweek, hour)) 
    
    avg = cur.fetchone()[0]
    con.close()
    
    if avg:
        print('Was able to find!')
    
    return avg

def clean_data(schedule, table):
    con = get_db_connection()
    cur = con.cursor()

    # Get the hours for the given table
    open_hour, close_hour = schedule[table]

    # Delete rows that are outside the operating hours
    cur.execute(f'''DELETE FROM "{table}"
                    WHERE hour < ? OR hour >= ?''', (open_hour, close_hour))

    con.commit()
    con.close()
    
if __name__ == '__main__':
    pass