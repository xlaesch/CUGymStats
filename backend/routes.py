from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import os
import time
import hmac
import hashlib
from psycopg import sql
from db_helper_pg import get_average_for_day, get_db_connection
from dotenv import load_dotenv

app = Flask(__name__)
# If you need browser direct access for debugging, constrain CORS to your dev origin.
# Production should route via BFF only.
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:3000", "http://localhost:3000"]}})

load_dotenv()

# Shared secret used for HMAC verification of BFF calls
DOMAIN_API_SECRET = os.getenv("DOMAIN_API_SECRET")
if not DOMAIN_API_SECRET:
    # Keep running, but warn loudly. Prefer failing fast in production.
    print("[WARN] DOMAIN_API_SECRET not set. HMAC verification will fail.")

# Lightweight, in-memory safety rate limiter (per remote addr)
_rate_bucket = {}
_RATE_LIMIT = int(os.getenv("FLASK_SAFETY_RPS", "120"))  # requests per minute per remote
_WINDOW_SECONDS = 60


def _too_many_requests(key: str) -> bool:
    now = int(time.time())
    window = now // _WINDOW_SECONDS
    bucket = _rate_bucket.get(key)
    if not bucket or bucket[0] != window:
        _rate_bucket[key] = (window, 1)
        return False
    count = bucket[1] + 1
    _rate_bucket[key] = (window, count)
    return count > _RATE_LIMIT


def _verify_hmac_or_abort():
    """
    Verify HMAC signed request from BFF.
    Expected headers:
    - X-Timestamp: unix epoch seconds
    - X-Nonce: random UUID/string
    - X-Signature: hex(hmac_sha256(secret, canonical_string))

    canonical_string = "\n".join([
        timestamp, nonce, method, path, query, body
    ])
    where body is exact raw body string (empty for GET).
    """
    if not DOMAIN_API_SECRET:
        abort(500, description="Server misconfigured: missing DOMAIN_API_SECRET")

    # Basic safety rate limit
    remote_key = request.headers.get("X-Forwarded-For") or request.remote_addr or "unknown"
    if _too_many_requests(remote_key):
        abort(429, description="Too Many Requests")

    ts = request.headers.get("X-Timestamp")
    nonce = request.headers.get("X-Nonce")
    sig = request.headers.get("X-Signature")

    if not ts or not nonce or not sig:
        abort(401, description="Unauthorized: missing auth headers")

    try:
        ts_int = int(ts)
    except ValueError:
        abort(400, description="Invalid timestamp")

    # Reject requests too far from current time (5 minutes skew)
    if abs(time.time() - ts_int) > 300:
        abort(401, description="Unauthorized: timestamp skew")

    method = request.method.upper()
    path = request.path
    query = request.query_string.decode("utf-8")
    body = request.get_data(as_text=True) or ""

    canonical = "\n".join([str(ts_int), nonce, method, path, query, body])
    expected = hmac.new(
        DOMAIN_API_SECRET.encode("utf-8"),
        canonical.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, sig):
        abort(401, description="Unauthorized: bad signature")

@app.route("/api/gymstats", methods=['GET'])
def get_gym_stats():
    _verify_hmac_or_abort()
    location = request.headers.get('X-Location')
    if not location:
        abort(400, description="Missing 'X-Location' header.")
        
    con = get_db_connection()
    cur = con.cursor()
    
    query = sql.SQL('''SELECT id, lastcount, percent, "timestamp"
                FROM {}''').format(sql.Identifier(location))
    cur.execute(query)
    
    output = cur.fetchall()
    cur.close()
    
    response = [{'id': row[0], 'lastcount': row[1], 'percentage': row[2], 'timestamp': (row[3].isoformat() if hasattr(row[3], 'isoformat') else row[3])}
                for row in output]
        
    return jsonify(response)

@app.route('/api/average-occupancy', methods=['GET'])
def average_occupancy():
    _verify_hmac_or_abort()
    location = request.headers.get('X-Location')
    if not location:
        abort(400, description="Missing 'X-Location' header.")

    day_param = request.headers.get('X-Day-Of-Week')
    if day_param is None:
        abort(400, description='Missing X-Day-Of-Week header.')

    try:
        day_of_week = int(day_param)
    except (TypeError, ValueError):
        abort(400, description='Invalid X-Day-Of-Week header. Expected integer 0-6.')

    if day_of_week < 0 or day_of_week > 6:
        abort(400, description='Invalid X-Day-Of-Week header. Expected integer 0-6.')

    data = get_average_for_day(day_of_week, location)
    result = [{'hour': int(row[0]), 'avg_percentage': float(row[1]) if row[1] is not None else None} for row in data]
    return jsonify(result)


if __name__ == '__main__':
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    # In production, run behind a reverse proxy and do not expose publicly; trust only BFF.
    app.run(host=host, port=port, debug=debug)