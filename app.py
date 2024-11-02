from flask import Flask, render_template, request, redirect, url_for, flash, session
import cx_Oracle
import csv
import os
import re
import logging

# Set Oracle Instant Client environment variables
os.environ["LD_LIBRARY_PATH"] = "/opt/oracle/instantclient_23_5"
os.environ["ORACLE_HOME"] = "/opt/oracle/instantclient_23_5"

# Set up the Oracle Instant Client library path
try:
    cx_Oracle.init_oracle_client(lib_dir="/opt/oracle/instantclient_23_5")
except Exception as e:
    logging.error(f"Oracle Client initialization error: {e}")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging for better error tracking
logging.basicConfig(level=logging.DEBUG)

# Database configuration
dsn = "localhost:1521/XE"
username = "admin"
password = "password"

# Initialize a connection pool with more detailed debugging
try:
    pool = cx_Oracle.SessionPool(
        user=username,
        password=password,
        dsn=dsn,
        min=2,
        max=10,
        increment=1,
        threaded=True,
        encoding="UTF-8"
    )
    logging.debug("Connection pool created successfully.")
except cx_Oracle.DatabaseError as e:
    logging.error(f"Database connection pool error: {e}")

# Input validation functions
def is_valid_username(username):
    return re.match("^[a-zA-Z0-9_]{3,30}$", username)

def is_valid_password(password):
    return 8 <= len(password) <= 30

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        
        # Input validation
        if not is_valid_username(user) or not is_valid_password(pw):
            flash("Invalid username or password format.", "danger")
            return redirect(url_for('login'))
        
        try:
            # Get a connection from the pool
            connection = pool.acquire()
            cursor = connection.cursor()

            # Simplified query with explicit error handling
            cursor.execute("SELECT password FROM users WHERE username = :username", {"username": user})
            result = cursor.fetchone()
            
            if result:
                stored_password = result[0]
                logging.debug(f"Retrieved password from database: {stored_password}")

                if stored_password == pw:  # Use a hash comparison in production
                    session['username'] = user
                    flash("Login successful!", "success")
                    return redirect(url_for('home'))
                else:
                    flash("Invalid password.", "danger")
            else:
                flash("Invalid username.", "danger")
        
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            logging.error(f"Database error code: {error.code}")
            logging.error(f"Database error message: {error.message}")
            flash(f"Database error: {error.message}", "danger")
        
        finally:
            if cursor:
                cursor.close()
            if connection:
                pool.release(connection)

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    
    try:
        connection = pool.acquire()
        cursor = connection.cursor()
        
        # Fetch data with limited rows
        cursor.execute("SELECT transaction_id, transaction_date, amount, category, is_fraud FROM credit_card_fraud FETCH FIRST 100 ROWS ONLY")
        result = cursor.fetchall()

        return render_template('home.html', table=result)
    
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        logging.error(f"Database error code: {error.code}")
        logging.error(f"Database error message: {error.message}")
        flash("Failed to fetch data from the database.", "danger")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            pool.release(connection)

@app.route('/load_data')
def load_data():
    if 'username' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))

    csv_file_path = "data/credit_card_fraud_dataset.csv"

    try:
        connection = pool.acquire()
        cursor = connection.cursor()
        
        with open(csv_file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row

            for row in csv_reader:
                cursor.execute("""
                    INSERT INTO credit_card_fraud (transaction_id, transaction_date, amount, category, is_fraud)
                    VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5)
                """, row)

        connection.commit()
        flash("Data loaded successfully from CSV!", "success")
    
    except FileNotFoundError:
        flash("CSV file not found. Please ensure the file is available.", "danger")
    
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        logging.error(f"Database error code: {error.code}")
        logging.error(f"Database error message: {error.message}")
        flash(f"Database error: {error.message}", "danger")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            pool.release(connection)

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

# Security headers to prevent XSS, clickjacking, etc.
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    app.run(debug=True)
