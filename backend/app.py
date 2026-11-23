
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask application
app = Flask(__name__)

# Load the trained model from the same folder as app.py
model_path = os.path.join(
    os.path.dirname(__file__),
    'superkart_model.joblib'
)

model = joblib.load(model_path)


# Home route
@app.route('/')
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


# Single prediction endpoint
@app.route('/v1/predict', methods=['POST'])
def predict():

    try:
        # Get JSON data from request
        input_data = request.get_json()

        # Convert JSON into a DataFrame
        input_df = pd.DataFrame([input_data])

        # Make prediction
        prediction = model.predict(input_df)

        # Return prediction as JSON
        return jsonify({
            'Predicted_Product_Store_Sales_Total': float(prediction[0])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Batch prediction endpoint
@app.route('/v1/predictbatch', methods=['POST'])
def predictbatch():

    try:
        # Check whether a file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        # Read uploaded CSV file
        input_df = pd.read_csv(file)

        # Generate predictions
        predictions = model.predict(input_df)

        # Add predictions to DataFrame
        input_df['Predicted_Product_Store_Sales_Total'] = predictions

        # Return predictions as JSON
        return input_df.to_json(orient='records')

    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
