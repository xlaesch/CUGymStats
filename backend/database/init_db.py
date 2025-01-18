import sqlite3

def init_table(table_name: str):
    con = sqlite3.connect("database/data.db") # connection to the db
    cur = con.cursor() #cursor creation

    # Create table if it does not exist
    cur.execute('''CREATE TABLE IF NOT EXISTS ?
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lastcount INTEGER,
                    percent INTEGER,
                    timestamp TEXT,
                    dayofweek INTEGER,
                    hour INTEGER)''', (table_name))
    
    con.close()