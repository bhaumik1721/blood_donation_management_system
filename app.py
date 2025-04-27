from flask import Flask, request, jsonify
from db import get_db_connection
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)  # Allow CORS for frontend

# Example route
@app.route('/')
def home():
    return "Blood Donation Management System API is Running!"


# Register Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username already exists
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({'message': 'Username already exists!'}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert into database
    cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'User registered successfully!'}), 201

# -----------------------------

# Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Find user
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful!', 'role': user['role']}), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

from datetime import datetime

# -----------------------------
# Add or Update Donor Details Route
@app.route('/add_donor_details', methods=['POST'])
@app.route('/add_donor_details', methods=['POST'])
def add_donor_details():
    data = request.get_json()
    username = data.get('username')  # from frontend / postman
    blood_group = data.get('blood_group')  # donor detail
    contact = data.get('contact')  # donor detail
    last_donated = data.get('last_donated')  # donor detail (date)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Step 1: Fetch user_id from users table using username
        cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]  # user[0] because fetchone() returns tuple (user_id,)

            # Step 2: Insert into donor_details table
            cursor.execute('''
                INSERT INTO donor_details (user_id, blood_group, contact, last_donated)
                VALUES (%s, %s, %s, %s)
            ''', (user_id, blood_group, contact, last_donated))

            conn.commit()
            return jsonify({'message': 'Donor details added successfully'}), 201

        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        print('Error:', e)
        return jsonify({'error': 'An error occurred while adding donor details.'}), 500

    finally:
        cursor.close()
        conn.close()
@app.route('/view_camps', methods=['GET'])
def view_camps():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # dictionary=True to get nice JSON

    cursor.execute('SELECT * FROM camps')
    camps = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({'camps': camps})


@app.route('/signup_camp', methods=['POST'])
def signup_camp():
    data = request.get_json()
    username = data.get('username')
    camp_id = data.get('camp_id')

    # Get user_id using username
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()

    if user:
        user_id = user[0]

        # Insert the signup information into camp_signups
        cursor.execute('''
            INSERT INTO camp_signups (user_id, camp_id, signup_date)
            VALUES (%s, %s, CURDATE())
        ''', (user_id, camp_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Signed up for camp successfully'})
    else:
        cursor.close()
        conn.close()
        return jsonify({'error': 'User not found'}), 404


@app.route('/add_camp', methods=['POST'])
def add_camp():
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected."}), 400

    data = request.get_json()
    camp_name = data.get('camp_name')
    location = data.get('location')
    date = data.get('date')  # Expected format: 'YYYY-MM-DD'
    timing = data.get('timing')  # Expected format: 'HH:MM:SS'

    if not all([camp_name, location, date, timing]):
        return jsonify({"error": "Missing required fields."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO camps (camp_name, location, date, timing)
        VALUES (%s, %s, %s, %s)
    ''', (camp_name, location, date, timing))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Camp added successfully'}), 201


@app.route('/edit_camp', methods=['PUT'])
def edit_camp():
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected."}), 400

    data = request.get_json()
    camp_id = data.get('camp_id')
    camp_name = data.get('camp_name')
    location = data.get('location')
    date = data.get('date')  # Expected format: 'YYYY-MM-DD'
    timing = data.get('timing')  # Expected format: 'HH:MM:SS'

    if not all([camp_id, camp_name, location, date, timing]):
        return jsonify({"error": "Missing required fields."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE camps
        SET camp_name = %s, location = %s, date = %s, timing = %s
        WHERE camp_id = %s
    ''', (camp_name, location, date, timing, camp_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Camp updated successfully'}), 200


@app.route('/delete_camp', methods=['DELETE'])
def delete_camp():
    data = request.get_json()
    camp_id = data.get('camp_id')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM camps WHERE camp_id = %s', (camp_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Camp deleted successfully'}), 200


@app.route('/get_camps', methods=['GET'])
def get_camps():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT camp_id, camp_name, location, DATE_FORMAT(date, '%Y-%m-%d') as date, TIME_FORMAT(timing, '%H:%i') as timing FROM camps"
        cursor.execute(query)

        camps = cursor.fetchall()

        return jsonify({'camps': camps}), 200

    except Exception as e:
        return jsonify({'message': 'Error fetching camps', 'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
