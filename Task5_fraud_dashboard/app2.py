# app.py
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the datasets
fraud_data = pd.read_csv('D:/week8&9 data/Fraud_Data.csv')

@app.route('/', methods=['GET'])
def index():
    return "Fraud Detection API is running!"

@app.route('/summary', methods=['GET'])
def get_summary():
    total_transactions = len(fraud_data)
    fraud_cases = fraud_data[fraud_data['class'] == 1]
    total_fraud_cases = len(fraud_cases)
    fraud_percentage = (total_fraud_cases / total_transactions) * 100

    summary = {
        "total_transactions": total_transactions,
        "total_fraud_cases": total_fraud_cases,
        "fraud_percentage": fraud_percentage
    }
    return jsonify(summary)

@app.route('/trends', methods=['GET'])
def get_trends():
    # Convert purchase_time to datetime if not already
    fraud_data['purchase_time'] = pd.to_datetime(fraud_data['purchase_time'])
    # Group by date and sum fraud cases
    trends = fraud_data.groupby(fraud_data['purchase_time'].dt.date).agg({'class': 'sum'}).reset_index()
    trends = trends.rename(columns={'class': 'fraud_cases', 'purchase_time': 'date'})
    return trends.to_json(orient='records')

@app.route('/geo_data', methods=['GET'])
def get_geo_data():
    geo_data = fraud_data.groupby('ip_address').agg({'class': 'sum'}).reset_index()
    geo_data = geo_data.rename(columns={'class': 'fraud_cases'})
    return geo_data.to_json(orient='records')

@app.route('/device_data', methods=['GET'])
def get_device_data():
    device_data = fraud_data.groupby('device_id').agg({'class': 'sum'}).reset_index()
    device_data = device_data.rename(columns={'class': 'fraud_cases'})
    return device_data.to_json(orient='records')

@app.route('/browser_data', methods=['GET'])
def get_browser_data():
    browser_data = fraud_data.groupby('browser').agg({'class': 'sum'}).reset_index()
    browser_data = browser_data.rename(columns={'class': 'fraud_cases'})
    return browser_data.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
