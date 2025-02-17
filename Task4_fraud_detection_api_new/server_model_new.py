# serve_model.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import logging
from logging.handlers import RotatingFileHandler

# Load the trained Random Forest model
model = joblib.load('D:/week8&9 data/random_forest_model.pkl')

# Initialize the Flask application
app = Flask(__name__)

# Set up logging
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/', methods=['GET'])
def index():
    return "Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the POST request
        data = request.get_json(force=True)
        app.logger.info(f'Received data: {data}')

        # Convert data into numpy array
        input_data = np.array(data['features']).reshape(1, -1)

        # Make prediction
        prediction = model.predict(input_data).tolist()
        app.logger.info(f'Prediction: {prediction}')

        # Return prediction as JSON
        return jsonify({'prediction': prediction})

    except Exception as e:
        app.logger.error(f'Error: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
