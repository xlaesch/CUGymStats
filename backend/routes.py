from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
from database.db_helper import get_average_for_day, get_db_connection
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:3000"}})

load_dotenv()

API_KEY = os.getenv('API_KEY')
print(f'printing API_KEY: {API_KEY}')

def authenticate_request():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        abort(401, description='Unauthorized')

@app.route("/api/gymstats", methods=['GET'])
def get_gym_stats():
    authenticate_request()
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute('''SELECT *
                FROM helen_newman
                ''')
    
    output = cur.fetchall()
    cur.close()
    
    response = [{'lastcount': row[0], 'percentage': row[1], 'timestamp': row[2]}
                for row in output]
        
    return jsonify(response)

@app.route('/api/average-occupancy', methods=['GET'])
def average_occupancy():
    authenticate_request()
    day_of_week = request.args.get('dayofweek')
    
    data = get_average_for_day(day_of_week)
    
    result = [{'hour': row[0], 'avg_percentage': row[1] } for row in data]
    
    return jsonify(result)

@app.route('/api/get-api-key', methods=['GET'])
def get_api_key():
    response = jsonify({'api_key': API_KEY})
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:3000')
    return response

if __name__ == '__main__':
    app.run(debug=True)