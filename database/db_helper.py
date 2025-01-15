#TODO: add helper functions --> average out for given time/day 


month_code = {
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



