# dashboard.py
import dash
from dash import dcc, html
import plotly.express as px
import requests
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Fetch data from Flask API
summary_response = requests.get('http://localhost:5000/summary').json()
trends_response = requests.get('http://localhost:5000/trends').json()
geo_response = requests.get('http://localhost:5000/geo_data').json()
device_response = requests.get('http://localhost:5000/device_data').json()
browser_response = requests.get('http://localhost:5000/browser_data').json()

# Summary data
total_transactions = summary_response['total_transactions']
total_fraud_cases = summary_response['total_fraud_cases']
fraud_percentage = summary_response['fraud_percentage']

# Trends data
trends_df = pd.DataFrame(trends_response)

# Create figures
line_chart = px.line(trends_df, x='date', y='fraud_cases', title='Fraud Cases Over Time')

# Geographical data
geo_df = pd.DataFrame(geo_response)
geo_chart = px.choropleth(geo_df, locations='ip_address', color='fraud_cases',
                          locationmode='country names', title='Fraud Cases by Country')

# Device data
device_df = pd.DataFrame(device_response)
device_chart = px.bar(device_df, x='device_id', y='fraud_cases', title='Fraud Cases by Device')

# Browser data
browser_df = pd.DataFrame(browser_response)
browser_chart = px.bar(browser_df, x='browser', y='fraud_cases', title='Fraud Cases by Browser')

app.layout = html.Div([
    html.H1("Fraud Detection Dashboard"),
    html.Div([
        html.Div([
            html.H3("Total Transactions"),
            html.P(total_transactions)
        ], className="summary-box"),
        html.Div([
            html.H3("Total Fraud Cases"),
            html.P(total_fraud_cases)
        ], className="summary-box"),
        html.Div([
            html.H3("Fraud Percentage"),
            html.P(f"{fraud_percentage:.2f}%")
        ], className="summary-box")
    ], className="summary-container"),
    dcc.Graph(id='line-chart', figure=line_chart),
    dcc.Graph(id='geo-chart', figure=geo_chart),
    dcc.Graph(id='device-chart', figure=device_chart),
    dcc.Graph(id='browser-chart', figure=browser_chart)
])

if __name__ == '__main__':
    app.run_server(debug=True)
