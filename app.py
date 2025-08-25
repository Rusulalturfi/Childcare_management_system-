import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random string

def get_db_connection():
    conn = sqlite3.connect('childcare.db')  # Update with your actual DB name
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Welcome to the Childcare Management System!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password. Please try again."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Welcome to your dashboard, {session['username']}!"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

