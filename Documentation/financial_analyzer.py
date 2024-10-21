import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation and analysis
import matplotlib.pyplot as plt  # For creating plots
from typing import List, Tuple  # For type hinting
import requests  # For making HTTP requests
from datetime import datetime, timedelta  # For date and time operations
import os  # For adding reports to the folder

class FinancialDataAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key  
        self.data = None  # store the raw data
        self.sorted_data = None  # store the sorted data
        self.max_subarray = None  #store the maximum subarray
        self.anomalies = None  #store detected anomalies
        self.symbol = None  #store the stock symbol

    def fetch_data(self, symbol: str):
        self.symbol = symbol  
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={self.api_key}'
        print(f"Requesting data from URL: {url}")
        print("Note: Free API key limits data to approximately the last 100 trading days.")
        
        r = requests.get(url)  # Make the API request
        data = r.json()  # Parse the JSON response

        if 'Error Message' in data:
            raise ValueError(f"API returned an error: {data['Error Message']}")
        
        if 'Information' in data:
            raise ValueError(f"API rate limit exceeded: {data['Information']}")
        
        if 'Time Series (Daily)' not in data:
            raise ValueError(f"Unexpected API response format. Keys in response: {list(data.keys())}")

        # Convert the data to a DataFrame
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.index = pd.to_datetime(df.index)  # Convert index to datetime
        df = df.astype(float)  # Convert data to float
        df = df.sort_index()  # Sort data by date
        
        # Store only the closing prices
        self.data = df[['4. close']].rename(columns={'4. close': 'Closing'})

    def merge_sort(self, data: pd.DataFrame) -> pd.DataFrame:
        # Base case: if data has 1 or fewer elements, it's already sorted
        if len(data) <= 1:
            return data
        
        # Divide the data into two halves
        mid = len(data) // 2
        left = self.merge_sort(data.iloc[:mid])  # Recursively sort left half
        right = self.merge_sort(data.iloc[mid:])  # Recursively sort right half
        
        # Merge the sorted halves
        return self.merge(left, right)

    def merge(self, left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        result = pd.DataFrame(columns=left.columns)  # Initialize result DataFrame
        i, j = 0, 0  # Pointers for left and right DataFrames
        
        # Compare elements from left and right and merge them in sorted order
        while i < len(left) and j < len(right):
            if left.index[i] <= right.index[j]:
                result = pd.concat([result, left.iloc[[i]]])
                i += 1
            else:
                result = pd.concat([result, right.iloc[[j]]])
                j += 1
        
        # Add any remaining elements
        result = pd.concat([result, left.iloc[i:]])
        result = pd.concat([result, right.iloc[j:]])
        
        return result

    def sort_data(self):
        # Sort the data if it exists
        if self.data is not None and not self.data.empty:
            self.sorted_data = self.merge_sort(self.data)
        else:
            print("No data to sort. Please fetch data first.")

    def find_max_subarray(self):
        # Calculate daily returns
        returns = self.sorted_data['Closing'].pct_change().fillna(0).values
        
        def find_max_subarray(arr):
            # Kadane's algorithm to find maximum subarray
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

        # Find the maximum subarray in the returns
        low, high, max_sum = find_max_subarray(returns)
        self.max_subarray = (self.sorted_data.index[low], self.sorted_data.index[high], max_sum)

    def detect_anomalies(self, threshold: float = 0.03):
        # Convert data to list of (date, price) tuples
        points = list(zip(self.sorted_data.index.astype(int), self.sorted_data['Closing']))
        
        def distance(p1, p2):
            # Calculate Euclidean distance between two points
            return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        def closest_pair(points):
            # Find the closest pair of points using divide and conquer
            if len(points) <= 3:
                return min((distance(points[i], points[j]), points[i], points[j])
                           for i in range(len(points))
                           for j in range(i+1, len(points)))
            
            # Divide points into left and right halves
            mid = len(points) // 2
            midpoint = points[mid][0]
            left = points[:mid]
            right = points[mid:]
            
            # Recursively find closest pair in each half
            left_closest = closest_pair(left)
            right_closest = closest_pair(right)
            
            # Find the minimum of left and right closest pairs
            min_distance = min(left_closest, right_closest)
            
            # Check for closer pairs across the dividing line
            strip = [p for p in points if abs(p[0] - midpoint) < min_distance[0]]
            strip.sort(key=lambda p: p[1])
            
            for i in range(len(strip)):
                for j in range(i+1, min(i+7, len(strip))):
                    dist = distance(strip[i], strip[j])
                    if dist < min_distance[0]:
                        min_distance = (dist, strip[i], strip[j])
            
            return min_distance
        
        # Find the closest pair of points
        _, p1, p2 = closest_pair(points)
        
        # Calculate price change percentage
        price_change = abs(p1[1] - p2[1]) / min(p1[1], p2[1])
        
        # If price change exceeds threshold, consider it an anomaly
        if price_change > threshold:
            self.anomalies = pd.Series({
                pd.Timestamp(p1[0]): p1[1],
                pd.Timestamp(p2[0]): p2[1]
            })
        else:
            self.anomalies = pd.Series()

    def generate_report(self):
        # Use the existing "Generated Reports" folder
        report_folder = "Generated Reports"
        
        # Ensure the folder exists
        os.makedirs(report_folder, exist_ok=True)

        # Create stock price over time plot
        plt.figure(figsize=(14, 10))
        plt.plot(self.sorted_data.index, self.sorted_data['Closing'], label='Close Price')
        plt.title(f'Stock Price Over Time - {self.symbol}', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price ($)', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add annotations for start and end prices
        start_price = self.sorted_data['Closing'].iloc[0]
        end_price = self.sorted_data['Closing'].iloc[-1]
        plt.annotate(f'Start: ${start_price:.2f}', (self.sorted_data.index[0], start_price), 
                     textcoords="offset points", xytext=(0,10), ha='center', fontsize=10)
        plt.annotate(f'End: ${end_price:.2f}', (self.sorted_data.index[-1], end_price), 
                     textcoords="offset points", xytext=(0,-15), ha='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(report_folder, f'{self.symbol}_stock_graph.png'), dpi=300)
        plt.close()

        # Generate a text report
        report_text = f"""
Stock Price Analysis for {self.symbol}
Date Range: {self.sorted_data.index[0].date()} to {self.sorted_data.index[-1].date()}
Starting Price: ${start_price:.2f}
Ending Price: ${end_price:.2f}
Overall Change: {((end_price - start_price) / start_price) * 100:.2f}%

Maximum Gain Period: {self.max_subarray[0].date()} to {self.max_subarray[1].date()}
Maximum Return: {self.max_subarray[2]:.2%}

Anomalies Analysis
Number of anomalies detected: {len(self.anomalies)}
"""
        if not self.anomalies.empty:
            report_text += "Top 5 anomalies:\n"
            report_text += self.anomalies.sort_values(ascending=False).head().to_string()

        # Save the text report
        with open(os.path.join(report_folder, f'{self.symbol}_report.txt'), 'w') as f:
            f.write(report_text)

        # Create anomalies plot if anomalies were found
        if not self.anomalies.empty:
            plt.figure(figsize=(14, 10))
            plt.plot(self.sorted_data.index, self.sorted_data['Closing'], label='Close Price')
            plt.scatter(self.anomalies.index, self.anomalies, color='red', label='Anomalies')
            plt.title(f'Stock Price with Anomalies (Closest Pair Method) - {self.symbol}', fontsize=16)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Price ($)', fontsize=12)
            plt.legend(fontsize=10)
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # Add labels for anomalies
            for date, price in self.anomalies.items():
                plt.annotate(f'${price:.2f}', (date, price), 
                             textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
            
            plt.tight_layout()
            plt.savefig(os.path.join(report_folder, f'{self.symbol}_anomalies_graph.png'), dpi=300)
            plt.close()

        print(f"\nReport generated. Check the '{report_folder}' folder for the report files.\n")

# Example usage
if __name__ == "__main__":
    try:
        API_KEY = '5FFF9XIWKC05HMB5'  # API key for Alpha Vantage
        analyzer = FinancialDataAnalyzer(API_KEY)  

        symbol = 'BA'  # stock symbol
        analyzer.fetch_data(symbol)  # Fetch data for the symbol
        analyzer.sort_data()  # Sort the fetched data
        analyzer.find_max_subarray()  # Find the maximum subarray (period of maximum gain)
        analyzer.detect_anomalies()  # Detect anomalies in the data
        analyzer.generate_report()  # Generate and save the report


    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())
