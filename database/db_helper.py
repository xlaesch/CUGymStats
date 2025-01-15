import sqlite3

#TODO: add helper functions --> average out for given time/day 


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
    
    #Connect to database
    print('Attempting connection to database...')
    con = sqlite3.connect('database/data.db')
    print('Successful connection!')
    cur = con.cursor()
    
    #Inserting new data
    print('Attempting to insert new data...')
    cur.execute(f'''INSERT INTO {data['location']}(lastcount,percent,timestamp,daysofweek)
                VALUES (?,?,?)''', (data['data_lastcount'], data['data_percent'], data['data_timestamp'], dayofweek))
    con.commit()
    con.close()
    print('Successful insertion!')

def get_average_for_day(dayofweek):
    pass