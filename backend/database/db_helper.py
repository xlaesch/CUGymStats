import sqlite3

def get_db_connection():
    return sqlite3.connect("backend/database/data.db")

def init_table(table_name: str):
    print(table_name)
    con = get_db_connection()
    cur = con.cursor() #cursor creation

    # Create table if it does not exist
    cur.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}"
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastcount INTEGER,
                    percent INTEGER,
                    timestamp TEXT,
                    dayofweek INTEGER,
                    hour INTEGER)''')
    
    con.close()

#TODO: make a helper function to connect to the database, so we'll only have to change the path on one function

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


def insert_new_data(data):
    
    #Find day of week
    year = data['data_timestamp'][0:4]
    year_code = get_year_code(year)
    month_code = month_code_map[data['data_timestamp'][5:7]]
    date_number = data['data_timestamp'][8:10]
    leapyear_code = get_leapyear_code(data['data_timestamp'][0:4])
    dayofweek = get_day_of_week(year_code,month_code,century_code,date_number,leapyear_code)
    hour = data['data_timestamp'][11:14] #this would be a round down
    
    #Connect to database
    print('Attempting connection to database...')
    con = get_db_connection()
    print('Successful connection!')
    cur = con.cursor()
    
    #Inserting new data
    print('Attempting to insert new data...')
    cur.execute(f'''INSERT INTO {data['location']}(lastcount,percent,timestamp,daysofweek)
                VALUES (?,?,?)''', (data['data_lastcount'], data['data_percent'], data['data_timestamp'], dayofweek, hour))
    con.commit()
    con.close()
    print('Successful insertion!')

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
                ORDER BY hour;''', (dayofweek)) #TODO: figure out why it's saying no such table for helen_newman??
    
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
    
if __name__ == '__main__':
    pass