"""
Stock Data Loading Module

This module handles downloading historical stock price data using the Yahoo Finance API.
It provides functions to fetch stock data and prepare it for analysis.

Author: Stock Trading Strategy Project
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os


def download_stock_data(ticker, start_date=None, end_date=None, period="2y"):
    """
    Download historical stock price data from Yahoo Finance.
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'SPY')
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format. If None, uses period parameter.
    end_date : str, optional
        End date in 'YYYY-MM-DD' format. If None, uses today's date.
    period : str, optional
        Period to download data for. Options: '1d', '5d', '1mo', '3mo', '6mo', 
        '1y', '2y', '5y', '10y', 'ytd', 'max'. Default is '2y'.
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with columns: Open, High, Low, Close, Volume, Adj Close
        Index is DatetimeIndex with daily dates.
    
    Example:
    --------
    >>> data = download_stock_data('AAPL', start_date='2022-01-01', end_date='2023-12-31')
    >>> print(data.head())
    """
    try:
        # Create ticker object
        stock = yf.Ticker(ticker)
        
        # Download data
        if start_date and end_date:
            data = stock.history(start=start_date, end=end_date)
        else:
            data = stock.history(period=period)
        
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        
        # Clean column names (remove any extra spaces)
        data.columns = data.columns.str.strip()
        
        # Ensure we have the required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        print(f"Successfully downloaded {len(data)} days of data for {ticker}")
        print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
        
        return data
        
    except Exception as e:
        print(f"Error downloading data for {ticker}: {str(e)}")
        raise


def validate_data(data, ticker):
    """
    Validate the downloaded stock data for completeness and quality.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Stock price data
    ticker : str
        Stock ticker symbol for error messages
    
    Returns:
    --------
    pandas.DataFrame
        Validated and cleaned data
    """
    if data.empty:
        raise ValueError(f"No data available for {ticker}")
    
    # Check for minimum data points (need at least 200 days for 200-day MA)
    if len(data) < 250:
        print(f"Warning: Only {len(data)} days of data available for {ticker}. "
              f"200-day moving average may not be reliable.")
    
    # Check for missing values
    missing_data = data.isnull().sum()
    if missing_data.any():
        print(f"Warning: Missing data found in {ticker}:")
        for col, count in missing_data.items():
            if count > 0:
                print(f"  {col}: {count} missing values")
        
        # Forward fill missing values
        data = data.fillna(method='ffill')
        print("Missing values have been forward-filled.")
    
    # Check for zero or negative prices
    price_columns = ['Open', 'High', 'Low', 'Close']
    for col in price_columns:
        if col in data.columns:
            invalid_prices = (data[col] <= 0).sum()
            if invalid_prices > 0:
                print(f"Warning: {invalid_prices} invalid prices found in {col} column")
    
    return data


def save_data_to_csv(data, ticker, results_dir="results"):
    """
    Save stock data to CSV file in the results directory.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Stock price data
    ticker : str
        Stock ticker symbol
    results_dir : str
        Directory to save the file
    
    Returns:
    --------
    str
        Path to the saved file
    """
    # Create results directory if it doesn't exist
    os.makedirs(results_dir, exist_ok=True)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ticker}_data_{timestamp}.csv"
    filepath = os.path.join(results_dir, filename)
    
    # Save to CSV
    data.to_csv(filepath)
    print(f"Data saved to: {filepath}")
    
    return filepath


def get_stock_info(ticker):
    """
    Get basic information about a stock ticker.
    
    Parameters:
    -----------
    ticker : str
        Stock ticker symbol
    
    Returns:
    --------
    dict
        Dictionary containing stock information
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract key information
        stock_info = {
            'symbol': info.get('symbol', ticker),
            'longName': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'marketCap': info.get('marketCap', 'N/A'),
            'currency': info.get('currency', 'USD')
        }
        
        return stock_info
        
    except Exception as e:
        print(f"Warning: Could not retrieve info for {ticker}: {str(e)}")
        return {'symbol': ticker, 'longName': 'N/A'}


if __name__ == "__main__":
    # Example usage
    print("Testing data download functionality...")
    
    # Test with Apple stock
    ticker = "AAPL"
    try:
        data = download_stock_data(ticker, period="1y")
        validated_data = validate_data(data, ticker)
        
        print(f"\nFirst 5 rows of {ticker} data:")
        print(validated_data.head())
        
        print(f"\nLast 5 rows of {ticker} data:")
        print(validated_data.tail())
        
        # Get stock info
        info = get_stock_info(ticker)
        print(f"\nStock Info for {ticker}:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        # Save data
        save_data_to_csv(validated_data, ticker)
        
    except Exception as e:
        print(f"Error in data module test: {str(e)}")
