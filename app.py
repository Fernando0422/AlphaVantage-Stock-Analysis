from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
base_url = 'https://www.alphavantage.co/query'

def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return {"error": "Error fetching data from Alpha Vantage"}
    data = response.json()
    if "Time Series (1min)" not in data:
        return {"error": data.get("Note", "Invalid response from Alpha Vantage API")}
    return data

def analyze_stock(symbol):
    data = get_stock_data(symbol)
    if 'Time Series (1min)' not in data:
        return {"error": "Invalid response from Alpha Vantage API"}
    latest_data = list(data['Time Series (1min)'].values())[0]
    latest_price = latest_data['1. open']
    volume = latest_data['5. volume']
    return {"symbol": symbol, "latest_price": latest_price, "volume": volume}

@app.route('/analyze', methods=['GET'])
def analyze():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No stock symbol provided"}), 400
    analysis = analyze_stock(symbol)
    return jsonify(analysis)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
