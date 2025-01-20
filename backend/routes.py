from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
from database.db_helper import get_average_for_day,get_db_connection


app = Flask(__name__)
#TODO: add a way to specify which table to get stats from different gyms
CORS(app)

API_KEY = os.getenv('API_KEY')

def authenticate_request():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        abort(401, description='Unauthorized')

@app.route("/api/gymstats", methods=['GET']) #tell Flask what URL should trigger function, specified method GET
def get_gym_stats():
    authenticate_request()
    con = get_db_connection()
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
        
@app.route('/api/average-occupancy', methods=['GET'])
def average_occupancy():
    authenticate_request()
    day_of_week = request.args.get('dayofweek') #GET request would be --> http://example.com/api/average-occupancy?dayofweek=0
    
    data = get_average_for_day(day_of_week)
    
    result = [{'hour': row[0], 'avg_percentage': row[1] } for row in data]
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)