from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import re
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging for better error tracking
logging.basicConfig(level=logging.DEBUG)

# Input validation functions
def is_valid_username(username):
    return re.match("^[a-zA-Z0-9_]{3,30}$", username)

def is_valid_password(password):
    return 8 <= len(password) <= 30

@app.route('/')
def index():
    # Redirect to login page when accessing the root
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        
        # Input validation
        if not is_valid_username(user) or not is_valid_password(pw):
            flash("Invalid username or password format.", "danger")
            return redirect(url_for('login'))
        
        # For demonstration, we’ll bypass database authentication
        if user == "admin" and pw == "password":  # Replace with your own conditions if needed
            session['username'] = user
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    
    # Read the CSV file directly and convert it to a list of lists
    csv_file_path = "data/credit_card_fraud_dataset.csv"  # Update with your actual file path
    try:
        data = pd.read_csv(csv_file_path)
        data_list = data.values.tolist()  # Convert DataFrame to a list of lists
    except FileNotFoundError:
        data_list = []
        flash("CSV file not found. Please ensure the file path is correct.", "danger")
    
    return render_template('home.html', table=data_list)

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
