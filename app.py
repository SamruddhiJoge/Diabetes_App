from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash
import joblib
import numpy as np
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key_here'

# Load the trained model
MODEL_PATH = os.path.join('model', 'diabetes_model.pkl')
model = joblib.load(MODEL_PATH)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to database
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Fetch user's hashed password from the database
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user_row = cursor.fetchone()
        conn.close()

        # Verify username exists AND password matches the stored hash
        if user_row and check_password_hash(user_row[0], password):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        
        features = [
            float(data.get('pregnancies', 0)),
            float(data.get('glucose', 0)),
            float(data.get('bloodPressure', 0)),
            float(data.get('skinThickness', 0)),
            float(data.get('insulin', 0)),
            float(data.get('bmi', 0)),
            float(data.get('dpf', 0)),
            float(data.get('age', 0))
        ]
        
        input_data = np.array([features])
        prediction = model.predict(input_data)[0]
        
        confidence = None
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0]
            confidence = round(float(proba[prediction]) * 100, 2)
            
        return jsonify({
            'status': 'success',
            'prediction': int(prediction),
            'label': 'Diabetes Detected (Positive)' if prediction == 1 else 'No Diabetes Detected (Negative)',
            'confidence': confidence
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)