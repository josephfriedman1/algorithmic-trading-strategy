"""
Stock Trading Strategy - Main Execution Script

This is the main script that orchestrates the entire stock trading strategy analysis.
It downloads data, calculates moving averages, generates signals, runs backtests,
and creates visualizations.

Easy Configuration for Beginners:
- Change TICKER to analyze different stocks
- Modify START_DATE and END_DATE for different time periods
- Adjust SHORT_MA and LONG_MA for different moving average periods
- Change INITIAL_CAPITAL for different starting amounts

Author: Stock Trading Strategy Project
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from data import download_stock_data, validate_data, get_stock_info, save_data_to_csv
from strategy import create_strategy_data, analyze_signals
from backtest import Backtest

# Import configuration (you can edit config.py to customize settings)
from config import (
    TICKER, START_DATE, END_DATE, SHORT_MA, LONG_MA,
    INITIAL_CAPITAL, COMMISSION, RESULTS_DIR, SHOW_PLOTS
)

# =============================================================================
# PLOTTING FUNCTIONS
# =============================================================================

def create_price_and_ma_plot(data, ticker, short_ma, long_ma):
    """Create a plot showing price, moving averages, and signals."""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # Main price chart
    ax1.plot(data.index, data['Close'], label='Close Price', linewidth=1, alpha=0.8)
    ax1.plot(data.index, data[f'MA_{short_ma}'], label=f'{short_ma}-day MA', linewidth=2)
    ax1.plot(data.index, data[f'MA_{long_ma}'], label=f'{long_ma}-day MA', linewidth=2)
    
    # Add buy/sell signals
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    
    ax1.scatter(buy_signals.index, buy_signals['Close'], 
               color='green', marker='^', s=100, label='Buy Signal', zorder=5)
    ax1.scatter(sell_signals.index, sell_signals['Close'], 
               color='red', marker='v', s=100, label='Sell Signal', zorder=5)
    
    ax1.set_title(f'{ticker} - Price Chart with Moving Average Crossover Strategy', fontsize=16)
    ax1.set_ylabel('Price ($)', fontsize=12)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Volume chart
    ax2.bar(data.index, data['Volume'], alpha=0.6, color='gray')
    ax2.set_title(f'{ticker} - Trading Volume', fontsize=14)
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def create_equity_curve_plot(results, ticker):
    """Create an equity curve comparing strategy vs buy-and-hold."""
    
    portfolio_df = results['portfolio_df']
    
    # Calculate buy-and-hold portfolio value
    initial_price = portfolio_df['Price'].iloc[0]
    shares_bh = results['initial_capital'] / initial_price
    portfolio_df['Buy_Hold_Value'] = shares_bh * portfolio_df['Price']
    
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot both equity curves
    ax.plot(portfolio_df.index, portfolio_df['Portfolio_Value'], 
           label='Strategy', linewidth=2, color='blue')
    ax.plot(portfolio_df.index, portfolio_df['Buy_Hold_Value'], 
           label='Buy & Hold', linewidth=2, color='orange')
    
    # Add horizontal line at initial capital
    ax.axhline(y=results['initial_capital'], color='gray', 
              linestyle='--', alpha=0.7, label='Initial Capital')
    
    ax.set_title(f'{ticker} - Strategy Performance vs Buy & Hold', fontsize=16)
    ax.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    return fig

def create_performance_summary_plot(results, ticker):
    """Create a summary plot with key performance metrics."""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Returns comparison
    returns = [results['total_return_pct'], results['buy_hold_return_pct']]
    labels = ['Strategy', 'Buy & Hold']
    colors = ['blue', 'orange']
    
    bars = ax1.bar(labels, returns, color=colors, alpha=0.7)
    ax1.set_title('Total Returns Comparison', fontsize=14)
    ax1.set_ylabel('Return (%)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, returns):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{value:.1f}%', ha='center', va='bottom')
    
    # 2. Drawdown chart
    portfolio_df = results['portfolio_df']
    ax2.fill_between(portfolio_df.index, portfolio_df['Drawdown'] * 100, 0, 
                    color='red', alpha=0.3)
    ax2.plot(portfolio_df.index, portfolio_df['Drawdown'] * 100, color='red')
    ax2.set_title('Portfolio Drawdown', fontsize=14)
    ax2.set_ylabel('Drawdown (%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # 3. Key metrics
    metrics = ['Sharpe Ratio', 'Max Drawdown (%)', 'Win Rate (%)']
    values = [results['sharpe_ratio'], abs(results['max_drawdown_pct']), results['win_rate_pct']]
    
    bars = ax3.bar(metrics, values, color=['green', 'red', 'purple'], alpha=0.7)
    ax3.set_title('Risk & Performance Metrics', fontsize=14)
    ax3.set_ylabel('Value', fontsize=12)
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.2f}', ha='center', va='bottom')
    
    # 4. Monthly returns heatmap (if enough data)
    try:
        monthly_returns = portfolio_df['Daily_Return'].resample('M').apply(lambda x: (1 + x).prod() - 1) * 100
        monthly_returns.index = monthly_returns.index.strftime('%Y-%m')
        
        if len(monthly_returns) > 1:
            # Reshape for heatmap
            monthly_data = monthly_returns.values.reshape(-1, 1)
            sns.heatmap(monthly_data, annot=True, fmt='.1f', cmap='RdYlGn', 
                       center=0, ax=ax4, cbar_kws={'label': 'Return (%)'})
            ax4.set_title('Monthly Returns Heatmap', fontsize=14)
            ax4.set_ylabel('Month', fontsize=12)
            ax4.set_yticklabels(monthly_returns.index, rotation=0)
        else:
            ax4.text(0.5, 0.5, 'Insufficient data\nfor monthly analysis', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Monthly Returns', fontsize=14)
    except:
        ax4.text(0.5, 0.5, 'Monthly analysis\nnot available', 
                ha='center', va='center', transform=ax4.transAxes, fontsize=12)
        ax4.set_title('Monthly Returns', fontsize=14)
    
    plt.tight_layout()
    return fig

def save_plots(data, results, ticker, results_dir):
    """Save all plots to the results directory."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create and save price chart
    fig1 = create_price_and_ma_plot(data, ticker, SHORT_MA, LONG_MA)
    price_chart_path = os.path.join(results_dir, f"{ticker}_price_chart_{timestamp}.png")
    fig1.savefig(price_chart_path, dpi=300, bbox_inches='tight')
    plt.close(fig1)
    
    # Create and save equity curve
    fig2 = create_equity_curve_plot(results, ticker)
    equity_curve_path = os.path.join(results_dir, f"{ticker}_equity_curve_{timestamp}.png")
    fig2.savefig(equity_curve_path, dpi=300, bbox_inches='tight')
    plt.close(fig2)
    
    # Create and save performance summary
    fig3 = create_performance_summary_plot(results, ticker)
    summary_plot_path = os.path.join(results_dir, f"{ticker}_performance_summary_{timestamp}.png")
    fig3.savefig(summary_plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig3)
    
    return {
        'price_chart': price_chart_path,
        'equity_curve': equity_curve_path,
        'performance_summary': summary_plot_path
    }

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main function that runs the complete analysis."""
    
    print("="*60)
    print("STOCK TRADING STRATEGY ANALYSIS")
    print("="*60)
    print(f"Analyzing: {TICKER}")
    print(f"Period: {START_DATE} to {END_DATE}")
    print(f"Strategy: {SHORT_MA}-day MA vs {LONG_MA}-day MA crossover")
    print(f"Initial Capital: ${INITIAL_CAPITAL:,}")
    print("="*60)
    
    try:
        # Step 1: Download and validate data
        print("\n1. Downloading stock data...")
        raw_data = download_stock_data(TICKER, START_DATE, END_DATE)
        validated_data = validate_data(raw_data, TICKER)
        
        # Get stock info
        stock_info = get_stock_info(TICKER)
        print(f"Company: {stock_info.get('longName', 'N/A')}")
        print(f"Sector: {stock_info.get('sector', 'N/A')}")
        
        # Step 2: Implement strategy
        print("\n2. Implementing trading strategy...")
        strategy_data = create_strategy_data(validated_data, SHORT_MA, LONG_MA)
        
        # Step 3: Run backtest
        print("\n3. Running backtest...")
        backtest_engine = Backtest(INITIAL_CAPITAL, COMMISSION)
        results = backtest_engine.run_backtest(strategy_data)
        
        # Step 4: Display results
        print("\n4. Performance Analysis:")
        backtest_engine.print_performance_summary(results)
        
        # Step 5: Create and save visualizations
        print("\n5. Creating visualizations...")
        os.makedirs(RESULTS_DIR, exist_ok=True)
        
        plot_paths = save_plots(strategy_data, results, TICKER, RESULTS_DIR)
        print(f"Charts saved to {RESULTS_DIR}/ directory")
        
        # Step 6: Save data and results
        print("\n6. Saving results...")
        save_data_to_csv(strategy_data, f"{TICKER}_strategy_data", RESULTS_DIR)
        backtest_engine.save_results(results, TICKER, RESULTS_DIR)
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE!")
        print("="*60)
        print(f"All results saved to: {RESULTS_DIR}/")
        print("Files created:")
        for plot_type, path in plot_paths.items():
            print(f"  - {plot_type}: {os.path.basename(path)}")
        
        return strategy_data, results
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        print("Please check your configuration and try again.")
        return None, None

if __name__ == "__main__":
    # Run the complete analysis
    data, results = main()
    
    # Optional: Display plots (controlled by config.py SHOW_PLOTS setting)
    if data is not None and results is not None and SHOW_PLOTS:
        print("\nDisplaying charts...")

        # Show price chart
        fig1 = create_price_and_ma_plot(data, TICKER, SHORT_MA, LONG_MA)
        plt.show()

        # Show equity curve
        fig2 = create_equity_curve_plot(results, TICKER)
        plt.show()

        # Show performance summary
        fig3 = create_performance_summary_plot(results, TICKER)
        plt.show()
    elif data is not None and results is not None:
        print("\nCharts saved to results/ directory (SHOW_PLOTS=False in config.py)")
