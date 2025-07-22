"""
Simple Example Script for Stock Trading Strategy

This is a simplified example that demonstrates how to use the trading strategy
modules without generating plots (good for testing or headless environments).

Author: Stock Trading Strategy Project
"""

from data import download_stock_data, validate_data
from strategy import create_strategy_data
from backtest import Backtest

def run_simple_example():
    """Run a simple example analysis."""
    
    print("="*50)
    print("SIMPLE STOCK STRATEGY EXAMPLE")
    print("="*50)
    
    # Configuration
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    short_ma = 20
    long_ma = 50
    initial_capital = 10000
    
    try:
        # Step 1: Download data
        print(f"\n1. Downloading {ticker} data...")
        raw_data = download_stock_data(ticker, start_date, end_date)
        validated_data = validate_data(raw_data, ticker)
        
        # Step 2: Create strategy
        print(f"\n2. Creating strategy with {short_ma}/{long_ma} day MAs...")
        strategy_data = create_strategy_data(validated_data, short_ma, long_ma)
        
        # Step 3: Run backtest
        print(f"\n3. Running backtest with ${initial_capital:,} capital...")
        backtest_engine = Backtest(initial_capital)
        results = backtest_engine.run_backtest(strategy_data)
        
        # Step 4: Show results
        print(f"\n4. Results Summary:")
        backtest_engine.print_performance_summary(results)
        
        print(f"\n✅ Example completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_simple_example()
    if success:
        print("\n🎉 The trading strategy system is working correctly!")
        print("You can now run 'python3 main.py' for the full analysis with charts.")
    else:
        print("\n⚠️  There was an issue. Please check the error message above.")
