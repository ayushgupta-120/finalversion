from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import init_database, create_user, verify_user, get_user
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize database when app starts
init_database()

@app.route('/')
def home():
    """Home route - redirect to login if not logged in, otherwise to dashboard"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Basic validation
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('register.html')
        
        # Try to create user
        if create_user(username, email, password):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists!', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Please enter both username and password!', 'error')
            return render_template('login.html')
        
        if verify_user(username, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard route - only accessible to logged-in users"""
    if 'username' not in session:
        flash('Please login to access dashboard!', 'error')
        return redirect(url_for('login'))
    
    user = get_user(session['username'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout(): 
    """User logout route"""
    session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))

@app.route('/test-css')
def test_css():
    """Test route to check if CSS is accessible"""
    return f"<h1>CSS Test</h1><p>Static folder path: {app.static_folder}</p><a href='/static/style.css'>Check CSS file</a>"

if __name__ == '__main__':
    app.run(debug=True)