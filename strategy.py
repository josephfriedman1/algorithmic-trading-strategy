"""
Moving Average Crossover Strategy Module

This module implements a simple moving average crossover trading strategy.
It calculates moving averages and generates buy/sell signals when the short-term
moving average crosses above or below the long-term moving average.

Strategy Rules:
- BUY when short MA crosses ABOVE long MA (Golden Cross)
- SELL when short MA crosses BELOW long MA (Death Cross)

Author: Stock Trading Strategy Project
"""

import pandas as pd
import numpy as np


def calculate_moving_averages(data, short_window=50, long_window=200, price_column='Close'):
    """
    Calculate simple moving averages for the given data.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Stock price data with DatetimeIndex
    short_window : int
        Number of periods for short-term moving average (default: 50)
    long_window : int
        Number of periods for long-term moving average (default: 200)
    price_column : str
        Column name to use for price data (default: 'Close')
    
    Returns:
    --------
    pandas.DataFrame
        Original data with additional MA columns
    """
    # Make a copy to avoid modifying original data
    df = data.copy()
    
    # Calculate moving averages
    df[f'MA_{short_window}'] = df[price_column].rolling(window=short_window).mean()
    df[f'MA_{long_window}'] = df[price_column].rolling(window=long_window).mean()
    
    print(f"Calculated {short_window}-day and {long_window}-day moving averages")
    
    return df


def generate_signals(data, short_window=50, long_window=200):
    """
    Generate buy/sell signals based on moving average crossover.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Stock data with moving averages
    short_window : int
        Short-term moving average period
    long_window : int
        Long-term moving average period
    
    Returns:
    --------
    pandas.DataFrame
        Data with additional signal columns
    """
    df = data.copy()
    
    # Column names for moving averages
    short_ma_col = f'MA_{short_window}'
    long_ma_col = f'MA_{long_window}'
    
    # Initialize signal columns
    df['Signal'] = 0  # 0 = Hold, 1 = Buy, -1 = Sell
    df['Position'] = 0  # 0 = No position, 1 = Long position
    
    # Generate signals where we have both moving averages
    valid_data = df.dropna(subset=[short_ma_col, long_ma_col])
    
    if len(valid_data) < 2:
        print("Warning: Not enough data to generate signals")
        return df
    
    # Calculate crossover signals
    # Buy signal: short MA crosses above long MA
    # Sell signal: short MA crosses below long MA
    
    for i in range(1, len(valid_data)):
        current_idx = valid_data.index[i]
        prev_idx = valid_data.index[i-1]
        
        current_short = valid_data.loc[current_idx, short_ma_col]
        current_long = valid_data.loc[current_idx, long_ma_col]
        prev_short = valid_data.loc[prev_idx, short_ma_col]
        prev_long = valid_data.loc[prev_idx, long_ma_col]
        
        # Golden Cross: Short MA crosses above Long MA (Buy signal)
        if prev_short <= prev_long and current_short > current_long:
            df.loc[current_idx, 'Signal'] = 1
        
        # Death Cross: Short MA crosses below Long MA (Sell signal)
        elif prev_short >= prev_long and current_short < current_long:
            df.loc[current_idx, 'Signal'] = -1
    
    # Calculate positions based on signals
    # Start with no position
    position = 0
    
    for idx in df.index:
        signal = df.loc[idx, 'Signal']
        
        if signal == 1:  # Buy signal
            position = 1
        elif signal == -1:  # Sell signal
            position = 0
        
        df.loc[idx, 'Position'] = position
    
    # Count signals
    buy_signals = (df['Signal'] == 1).sum()
    sell_signals = (df['Signal'] == -1).sum()
    
    print(f"Generated {buy_signals} buy signals and {sell_signals} sell signals")
    
    return df


def analyze_signals(data, short_window=50, long_window=200):
    """
    Analyze the generated trading signals and provide summary statistics.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Data with signals
    short_window : int
        Short-term moving average period
    long_window : int
        Long-term moving average period
    
    Returns:
    --------
    dict
        Dictionary containing signal analysis
    """
    # Get signal dates
    buy_dates = data[data['Signal'] == 1].index.tolist()
    sell_dates = data[data['Signal'] == -1].index.tolist()
    
    # Calculate time in market
    total_days = len(data)
    days_in_position = (data['Position'] == 1).sum()
    time_in_market = (days_in_position / total_days) * 100 if total_days > 0 else 0
    
    # Calculate average time between signals
    all_signal_dates = sorted(buy_dates + sell_dates)
    if len(all_signal_dates) > 1:
        time_diffs = [(all_signal_dates[i] - all_signal_dates[i-1]).days 
                     for i in range(1, len(all_signal_dates))]
        avg_time_between_signals = np.mean(time_diffs)
    else:
        avg_time_between_signals = 0
    
    analysis = {
        'total_buy_signals': len(buy_dates),
        'total_sell_signals': len(sell_dates),
        'total_signals': len(buy_dates) + len(sell_dates),
        'time_in_market_pct': round(time_in_market, 2),
        'avg_days_between_signals': round(avg_time_between_signals, 1) if avg_time_between_signals > 0 else 0,
        'buy_signal_dates': [date.strftime('%Y-%m-%d') for date in buy_dates],
        'sell_signal_dates': [date.strftime('%Y-%m-%d') for date in sell_dates],
        'strategy_params': {
            'short_ma': short_window,
            'long_ma': long_window
        }
    }
    
    return analysis


def get_signal_summary(data):
    """
    Get a readable summary of the trading signals.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Data with signals
    
    Returns:
    --------
    str
        Formatted summary string
    """
    analysis = analyze_signals(data)
    
    summary = f"""
Trading Signal Summary:
======================
Total Buy Signals: {analysis['total_buy_signals']}
Total Sell Signals: {analysis['total_sell_signals']}
Time in Market: {analysis['time_in_market_pct']}%
Average Days Between Signals: {analysis['avg_days_between_signals']}

Strategy Parameters:
- Short MA: {analysis['strategy_params']['short_ma']} days
- Long MA: {analysis['strategy_params']['long_ma']} days

Recent Signals:
"""
    
    # Add recent buy signals
    if analysis['buy_signal_dates']:
        summary += f"Last Buy Signal: {analysis['buy_signal_dates'][-1]}\n"
    
    if analysis['sell_signal_dates']:
        summary += f"Last Sell Signal: {analysis['sell_signal_dates'][-1]}\n"
    
    return summary


def create_strategy_data(data, short_window=50, long_window=200, price_column='Close'):
    """
    Complete strategy implementation: calculate MAs and generate signals.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Raw stock price data
    short_window : int
        Short-term moving average period
    long_window : int
        Long-term moving average period
    price_column : str
        Price column to use for calculations
    
    Returns:
    --------
    pandas.DataFrame
        Complete dataset with MAs and signals
    """
    print(f"Implementing Moving Average Crossover Strategy...")
    print(f"Short MA: {short_window} days, Long MA: {long_window} days")
    
    # Calculate moving averages
    df_with_ma = calculate_moving_averages(data, short_window, long_window, price_column)
    
    # Generate signals
    df_with_signals = generate_signals(df_with_ma, short_window, long_window)
    
    # Print summary
    print(get_signal_summary(df_with_signals))
    
    return df_with_signals


if __name__ == "__main__":
    # Example usage with sample data
    print("Testing strategy module...")
    
    # Create sample data for testing
    dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)  # For reproducible results
    
    # Generate sample price data with trend
    price_data = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)
    
    sample_data = pd.DataFrame({
        'Close': price_data,
        'Open': price_data * 0.99,
        'High': price_data * 1.01,
        'Low': price_data * 0.98,
        'Volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    print(f"Created sample data with {len(sample_data)} days")
    
    # Test strategy
    strategy_data = create_strategy_data(sample_data, short_window=20, long_window=50)
    
    print(f"\nStrategy data shape: {strategy_data.shape}")
    print(f"Columns: {list(strategy_data.columns)}")
