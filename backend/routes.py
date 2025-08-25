from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
from db_helper_pg import get_average_for_day, get_db_connection
from dotenv import load_dotenv

app = Flask(__name__)
# Update CORS to be more specific - allow only your frontend origin
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "https://yourdomain.com"]}})

load_dotenv()

API_KEY = os.getenv('API_KEY')

# Option 1: Use referrer checking
def authenticate_request():
    # Check if the request is coming from your website
    referrer = request.headers.get('Referer', '')
    allowed_domains = ['127.0.0.1', 'localhost', 'yourdomain.com']
    
    is_valid_referrer = any(domain in referrer for domain in allowed_domains)
    
    if not is_valid_referrer:
        abort(401, description='Unauthorized')

# Option 2: Add rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/gymstats", methods=['GET'])
@limiter.limit("30 per minute")  # Add rate limiting
def get_gym_stats():
    authenticate_request()  # Use referrer checking
    con = get_db_connection()
    cur = con.cursor()
    
    cur.execute('''SELECT id, lastcount, percent, "timestamp"
                FROM "Helen Newman Fitness Center"''')
    
    output = cur.fetchall()
    cur.close()
    
    response = [{'id': row[0], 'lastcount': row[1], 'percentage': row[2], 'timestamp': row[3]}
                for row in output]
        
    return jsonify(response)

@app.route('/api/average-occupancy', methods=['GET'])
@limiter.limit("30 per minute")  # Add rate limiting
def average_occupancy():
    authenticate_request()  # Use referrer checking
    day_of_week = int(request.args.get('dayofweek'))
    
    data = get_average_for_day(day_of_week)
    
    result = [{'hour': row[0], 'avg_percentage': row[1] } for row in data]
    
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)