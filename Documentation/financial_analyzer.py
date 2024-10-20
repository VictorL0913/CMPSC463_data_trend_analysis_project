import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple
import requests
from datetime import datetime, timedelta

class FinancialDataAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.data = None
        self.sorted_data = None
        self.max_subarray = None
        self.anomalies = None

    def fetch_data(self, symbol: str):
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.api_key}'
        print(f"Requesting data from URL: {url}")
        
        r = requests.get(url)
        data = r.json()

        if 'Error Message' in data:
            raise ValueError(f"API returned an error: {data['Error Message']}")
        
        if 'Time Series (Daily)' not in data:
            raise ValueError(f"Unexpected API response format. Keys in response: {list(data.keys())}")

        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df.astype(float)
        
        self.data = df[['4. close']].rename(columns={'4. close': 'Closing'})
 
    def sort_data(self):
        self.sorted_data = self.data.sort_index()

    def find_max_subarray(self):
        returns = self.sorted_data['Closing'].pct_change().fillna(0).values
        
        def find_max_subarray(arr):
            max_ending_here = max_so_far = arr[0]
            start, end, s = 0, 0, 0
            for i in range(1, len(arr)):
                if arr[i] > max_ending_here + arr[i]:
                    max_ending_here = arr[i]
                    s = i
                else:
                    max_ending_here = max_ending_here + arr[i]
                if max_ending_here > max_so_far:
                    max_so_far = max_ending_here
                    start, end = s, i
            return start, end, max_so_far

        low, high, max_sum = find_max_subarray(returns)
        self.max_subarray = (self.sorted_data.index[low], self.sorted_data.index[high], max_sum)

    def detect_anomalies(self, window_size: int = 5, threshold: float = 2.5):
        returns = self.sorted_data['Closing'].pct_change().fillna(0)
        rolling_mean = returns.rolling(window=window_size).mean()
        rolling_std = returns.rolling(window=window_size).std()
        z_scores = (returns - rolling_mean) / rolling_std

        anomalies = z_scores[abs(z_scores) > threshold]
        self.anomalies = anomalies

    def generate_report(self):
        plt.figure(figsize=(12, 8))
        plt.plot(self.sorted_data.index, self.sorted_data['Closing'], label='Close Price')
        plt.title('Stock Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.savefig('stock_price.png')
        plt.close()

        if self.max_subarray:
            start_date, end_date, max_return = self.max_subarray
            print(f"Maximum Gain Period: {start_date.date()} to {end_date.date()}")
            print(f"Maximum Return: {max_return:.2%}")

        if self.anomalies is not None:
            plt.figure(figsize=(12, 8))
            plt.plot(self.sorted_data.index, self.sorted_data['Closing'], label='Close Price')
            plt.scatter(self.anomalies.index, self.sorted_data.loc[self.anomalies.index, 'Closing'], color='red', label='Anomalies')
            plt.title('Stock Price with Anomalies')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            plt.savefig('anomalies.png')
            plt.close()

            print(f"Number of anomalies detected: {len(self.anomalies)}")
            print("Top 5 anomalies:")
            print(self.anomalies.sort_values(ascending=False).head())

# Example usage
if __name__ == "__main__":
    try:
        API_KEY = '5FFF9XIWKC05HMB5' 
        print("Initializing FinancialDataAnalyzer...")
        analyzer = FinancialDataAnalyzer(API_KEY)

        symbol = 'AAPL'  # Example: Apple Inc.
        print(f"Fetching data for {symbol}...")
        analyzer.fetch_data(symbol)
        analyzer.sort_data()
        analyzer.find_max_subarray()
        analyzer.detect_anomalies()
        print("Generating report...")
        analyzer.generate_report()
        print("Report generated. Check for 'stock_price.png' and 'anomalies.png' in your current directory.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
