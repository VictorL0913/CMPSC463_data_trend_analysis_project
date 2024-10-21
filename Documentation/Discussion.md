# Discussion

## Findings and Insights

1. **Kadane's Algorithm for Maximum Gain**: One of the more intriguing aspects of this project was the implementation of Kadane's algorithm to find the maximum subarray, representing the period of maximum gain. The algorithm has an O(n) complexity, which is efficient for finding the most profitable time period.

2. **Anomaly Detection**: The implementation of the closest pair algorithm for anomaly detection proved effective in identifying significant price changes. This could be useful for investors in identifying unusual behavior or potential trading opportunities.

3. **Data Visualization**: While basic, the generation of line graphs for stock prices and anomaly graphs provides a visual of the data, making it easier to interpret trends and unusual patterns.

## Challenges Faced

1. **Report Generating**: Creating a more detailed analysis report proved to be more complex than initially anticipated. While the system successfully generates basic line graphs and anomaly graphs, there's room for more comprehensive reporting.

2. **API Rate Limiting**: The free tier of the Alpha Vantage API imposes rate limits, which restricts the amount of data that can be fetched in a given time period. This limitation affects the ability to analyze multiple stocks and also limits the time period that can be analyzed.

3. **Manual Stock Symbol Input**: The current implementation requires manual changes to the stock symbol for each company analysis, which limits the ease of use for analyzing multiple stocks.

## Limitations

The current system has several limitations:

1. **Data**: The analysis is limited to approximately the last 100 trading days due to API constraints, which may not be sufficient for long-term trend analysis.

2. **Single Stock Analysis**: The system is designed to analyze one stock at a time, that needs manual changes for each stock analysis.

3. **Reporting**: The reporting capabilities are currently limited to basic graphs and text summaries.

## Areas for Improvement

1. **Enhanced Reporting**: Develop more detailed and interactive reports, possibly including statistical summaries, trend indicators, and comparative analyses.

2. **Multiple Stock Analysis**: Implement functionality to analyze multiple stocks in a single run or choose from a list of stocks, allowing for easier comparative analysis.

4. **User Interface**: Develop a user-friendly interface for inputting stock symbols and viewing results, making the tool more accessible to non-technical users.

5. **Extended Data Range**: Explore free API options for accessing and analyzing longer periods of historical data to provide more comprehensive long-term analysis.

6. **Advanced Analytics**: Incorporate machine learning algorithms for better analysis and anomaly detection.

