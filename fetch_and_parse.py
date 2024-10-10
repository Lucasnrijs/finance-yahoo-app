import requests
import json

def fetch_stock_analysis(stock_symbol):
    try:
        # Make a GET request to the stock analysis endpoint
        response = requests.get(f'http://127.0.0.1:8000/stock-analysis-US/{stock_symbol}')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock analysis: {e}")
        return None

def save_analysis_data(data, stock_symbol):
    if data:
        # Save the data to a JSON file
        json_file_path = f'{stock_symbol}_analysis.json'
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Analysis data saved to {json_file_path}")
    else:
        print("No data to save.")

def main():
    stock_symbol = 'AAPL'  # Example stock symbol
    analysis_data = fetch_stock_analysis(stock_symbol)
    save_analysis_data(analysis_data, stock_symbol)

if __name__ == "__main__":
    main()