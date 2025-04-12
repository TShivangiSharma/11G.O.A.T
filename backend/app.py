from flask import Flask, request, session, jsonify
from flask_session import Session
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# ─────────────── Flask Setup ───────────────
app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Replace with env var in production
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# ─────────────── Google Sheets Setup ───────────────
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"  # <-- Important for searching
]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes)
client = gspread.authorize(creds)
sheet = client.open("Customer Support Mails").sheet1  # Replace with your sheet name

# ─────────────── Dummy Admin Credentials ───────────────
TEAM_USERS = {
    'admin1': {'password': 'admin_password', 'team': 'Technical'},
    'admin2': {'password': 'psych_team_password', 'team': 'Psychological'},
    'admin3': {'password': 'general_team_password', 'team': 'General'},
}


# ─────────────── Routes ───────────────

@app.route('/')
def root():
    return jsonify({"message": "Backend running"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = TEAM_USERS.get(username)

    if user and user['password'] == password:
        session['username'] = username
        session['team'] = user['team']
        return jsonify({"message": "Login successful", "team": user['team']}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    team = session['team']
    records = sheet.get_all_records()

    team_data = [row for row in records if row.get('label') == team]

    total = len(team_data)
    new = sum(1 for row in team_data if row.get('status') == 'new')
    in_progress = sum(1 for row in team_data if row.get('status') == 'in_progress')
    resolved = sum(1 for row in team_data if row.get('status') == 'resolved')

    return jsonify({
        "team": team,
        "stats": {
            "total": total,
            "new": new,
            "in_progress": in_progress,
            "resolved": resolved
        }
    }), 200

@app.route('/receive_email', methods=['POST'])
def receive_email():
    data = request.get_json()
    sender = data.get('sender')
    subject = data.get('subject')
    label = data.get('label')
    snippet = data.get('snippet')
    timestamp = data.get('timestamp') or datetime.datetime.now().isoformat()

    if not all([sender, subject, label, snippet]):
        return jsonify({"error": "Missing fields"}), 400

    sheet.append_row([sender, subject, label, snippet, timestamp, 'new'])
    return jsonify({"message": "Email logged successfully"}), 200

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

# ─────────────── Run App ───────────────

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'  # or 'redis', 'mongodb', etc.
    Session(app)

    app.run(debug=True)
