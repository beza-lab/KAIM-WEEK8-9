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
    # Convert purchase_time to datetime format if not already
    fraud_data['purchase_time'] = pd.to_datetime(fraud_data['purchase_time'])
    
    # Group by purchase_time and aggregate fraud cases
    trends = fraud_data.groupby(fraud_data['purchase_time'].dt.date).agg({'class': 'sum'}).reset_index()
    trends = trends.rename(columns={'class': 'fraud_cases', 'purchase_time': 'date'})
    return trends.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)
