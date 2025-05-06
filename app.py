from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd
from database import Database

app = Flask(__name__)

# Load the trained model and initialize database
model = joblib.load('output/random_forest_model.pkl')
db = Database()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get values from the form
        store = float(request.form['store'])
        day_of_week = float(request.form['day_of_week'])
        promo = float(request.form['promo'])
        state_holiday = float(request.form['state_holiday'])
        school_holiday = float(request.form['school_holiday'])
        store_type = float(request.form['store_type'])
        assortment = float(request.form['assortment'])
        competition_distance = float(request.form['competition_distance'])
        competition_open_since_month = float(request.form['competition_open_since_month'])
        competition_open_since_year = float(request.form['competition_open_since_year'])
        promo2 = float(request.form['promo2'])
        promo2_since_week = float(request.form['promo2_since_week'])
        promo2_since_year = float(request.form['promo2_since_year'])
        is_promo_month = float(request.form['is_promo_month'])
        month = float(request.form['month'])
        year = float(request.form['year'])
        
        # Make prediction
        features = np.array([[store, day_of_week, promo, state_holiday, 
                            school_holiday, store_type, assortment, 
                            competition_distance, competition_open_since_month,
                            competition_open_since_year, promo2, 
                            promo2_since_week, promo2_since_year,
                            is_promo_month, month, year]])
        prediction = model.predict(features)
        
        # Save to database
        features_dict = {
            'store': store,
            'day_of_week': day_of_week,
            'promo': promo,
            'state_holiday': state_holiday,
            'school_holiday': school_holiday,
            'store_type': store_type,
            'assortment': assortment,
            'competition_distance': competition_distance,
            'competition_open_since_month': competition_open_since_month,
            'competition_open_since_year': competition_open_since_year,
            'promo2': promo2,
            'promo2_since_week': promo2_since_week,
            'promo2_since_year': promo2_since_year,
            'is_promo_month': is_promo_month,
            'month': month,
            'year': year
        }
        db.save_prediction(features_dict, prediction[0])
        
        return render_template('index.html', 
                             prediction=f'Predicted Sales: ${prediction[0]:.2f}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
