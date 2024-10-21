# Financial Data Analyzer Tutorial

## Introduction

This tutorial will guide you through using the Financial Data Analyzer, a Python application that fetches stock data, analyzes it, and generates reports.

## Prerequisites

Before you begin, ensure you have Python 3.7 or later installed on your system.

### Required Libraries

You'll need to install the following Python libraries:

- numpy
- pandas
- matplotlib
- requests

You can install these libraries using pip: pip install numpy pandas matplotlib requests


## Getting Started

1. First, you'll need an API key from Alpha Vantage. Visit [Alpha Vantage](https://www.alphavantage.co/) and sign up for a free API key.

2. Clone or download the Financial Data Analyzer code from the repository.

3. Open the `financial_analyzer.py` file and replace the `API_KEY` value with your Alpha Vantage API key:

   ```python
   API_KEY = 'YOUR_API_KEY_HERE'
   ```

## Using the Application

1. Open a terminal or command prompt and navigate to the directory containing `financial_analyzer.py`.

2. Run the script:

   ```
   python financial_analyzer.py
   ```

3. By default, the script will analyze the stock symbol 'VZ' (Verizon). To analyze a different stock, modify the `symbol` variable in the main block:

   ```python
   symbol = 'AAPL'  # Change to your desired stock symbol
   ```

4. The script will fetch data, perform analysis, and generate reports. You'll see output in the console indicating the progress.

5. Once complete, check the "Generated Reports" folder for the following files:
   - `{symbol}_stock_graph.png`: A graph of the stock's closing prices over time.
   - `{symbol}_anomalies_graph.png`: A graph highlighting any detected anomalies in the stock price (will only be created if anomalies are found).
   - `{symbol}_report.txt`: A text report summarizing the analysis.

## Understanding the Reports

### Stock Graph
This graph shows the closing price of the stock over time. It includes annotations for the starting and ending prices.

### Anomalies Graph
If any anomalies are detected (unusual price changes), they will be highlighted on this graph.

### Text Report
The text report includes:
- Date range of the analysis
- Starting and ending prices
- Overall price change percentage
- Period of maximum gain
- Number of anomalies detected

## Troubleshooting

- If you encounter a "rate limit exceeded" error, wait a few minutes before trying again. The free API key has usage limits.
- Ensure all required libraries are installed correctly.
- Check that your API key is entered correctly and has not expired.

## Conclusion

You've now learned how to use the Financial Data Analyzer to fetch and analyze stock data. Experiment with different stock symbols and time ranges to gain insights into various stocks' performance.

