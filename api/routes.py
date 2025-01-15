from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
#TODO: add a way to specify which table to get stats from different gyms

@app.route("/api/gymstats", methods=['GET']) #tell Flask what URL should trigger function, specified method GET
def get_gym_stats():
    con = sqlite3.connect("database/data.db")
    cur = con.cursor()
    
    cur.execute('''SELECT *
                FROM helen_newman
                ''')
    
    output = cur.fetchall()
    cur.close()
    
    #Convert into json
    response = [{'lastcount': row[0], 'percentage': row[1], 'timestamp': row[2]}
                for row in output]
        
    return jsonify(response)
        

if __name__ == '__main__':
    app.run(debug=True)