from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

with open('common_passwords.txt') as f:
    leaked_passwords = set(p.strip() for p in f.readlines())

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    password = data.get('password', '')

    remarks = []
    suggestions = []

    length_criteria = len(password) >= 8
    lower_criteria = bool(re.search(r'[a-z]', password))
    upper_criteria = bool(re.search(r'[A-Z]', password))
    digit_criteria = bool(re.search(r'\d', password))
    special_criteria = bool(re.search(r'[^A-Za-z0-9]', password))
    leaked = password.lower() in leaked_passwords

    score = sum([
        int(length_criteria),
        int(lower_criteria),
        int(upper_criteria),
        int(digit_criteria),
        int(special_criteria)
    ])

    if leaked:
        remarks.append("⚠️ This password is commonly used or leaked. Avoid using it.")
        suggestions.append("Pick a password not used in common lists.")

    if not length_criteria:
        suggestions.append("Use at least 8 characters.")
    if not lower_criteria:
        suggestions.append("Include lowercase letters.")
    if not upper_criteria:
        suggestions.append("Include uppercase letters.")
    if not digit_criteria:
        suggestions.append("Add at least one digit.")
    if not special_criteria:
        suggestions.append("Include special characters (e.g., @, #, !).")

    if score <= 2 or leaked:
        strength = "Weak"
    elif score == 3 or score == 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return jsonify({
        "strength": strength,
        "remarks": remarks,
        "suggestions": suggestions
    })

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = []
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)

        for user in users:
            if user['username'] == username:
                return "Username already exists. Try logging in.", 409

        hashed_password = generate_password_hash(password)
        users.append({"username": username, "password": hashed_password})

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=2)

        session['user'] = username
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)

            for user in users:
                if user['username'] == username and check_password_hash(user['password'], password):
                    session['user'] = username
                    return redirect(url_for('home'))

        return "Invalid username or password.", 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
