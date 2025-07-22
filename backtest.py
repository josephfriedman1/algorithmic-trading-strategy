"""
Backtesting Engine Module

This module implements a backtesting engine for trading strategies.
It calculates portfolio performance, tracks trades, and compares
strategy returns against buy-and-hold performance.

Author: Stock Trading Strategy Project
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


class Backtest:
    """
    A simple backtesting engine for trading strategies.
    """
    
    def __init__(self, initial_capital=10000, commission=0.001):
        """
        Initialize the backtesting engine.
        
        Parameters:
        -----------
        initial_capital : float
            Starting capital for the backtest (default: $10,000)
        commission : float
            Commission rate per trade as decimal (default: 0.1% = 0.001)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.trades = []
        self.portfolio_values = []
        
    def run_backtest(self, data, price_column='Close'):
        """
        Run the backtest on strategy data with signals.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Data with 'Signal' and 'Position' columns
        price_column : str
            Column name for price data
        
        Returns:
        --------
        dict
            Backtest results including performance metrics
        """
        df = data.copy()
        
        # Initialize portfolio tracking
        cash = self.initial_capital
        shares = 0
        portfolio_value = self.initial_capital
        
        # Track daily portfolio values
        portfolio_values = []
        trade_log = []
        
        print(f"Starting backtest with ${self.initial_capital:,.2f} initial capital")
        print(f"Commission rate: {self.commission*100:.2f}% per trade")
        
        for i, (date, row) in enumerate(df.iterrows()):
            price = row[price_column]
            signal = row['Signal']
            
            # Execute trades based on signals
            if signal == 1 and shares == 0:  # Buy signal and not already holding
                # Buy as many shares as possible with available cash
                commission_cost = cash * self.commission
                available_cash = cash - commission_cost
                shares_to_buy = int(available_cash / price)
                
                if shares_to_buy > 0:
                    cost = shares_to_buy * price
                    cash -= (cost + commission_cost)
                    shares += shares_to_buy
                    
                    trade_log.append({
                        'Date': date,
                        'Action': 'BUY',
                        'Shares': shares_to_buy,
                        'Price': price,
                        'Cost': cost,
                        'Commission': commission_cost,
                        'Cash_After': cash,
                        'Shares_After': shares
                    })
            
            elif signal == -1 and shares > 0:  # Sell signal and holding shares
                # Sell all shares
                proceeds = shares * price
                commission_cost = proceeds * self.commission
                cash += (proceeds - commission_cost)
                
                trade_log.append({
                    'Date': date,
                    'Action': 'SELL',
                    'Shares': shares,
                    'Price': price,
                    'Proceeds': proceeds,
                    'Commission': commission_cost,
                    'Cash_After': cash,
                    'Shares_After': 0
                })
                
                shares = 0
            
            # Calculate current portfolio value
            portfolio_value = cash + (shares * price)
            portfolio_values.append({
                'Date': date,
                'Cash': cash,
                'Shares': shares,
                'Price': price,
                'Portfolio_Value': portfolio_value
            })
        
        # Store results
        self.trades = trade_log
        self.portfolio_values = portfolio_values
        
        # Calculate performance metrics
        results = self._calculate_performance_metrics(df, price_column)
        
        print(f"Backtest completed. Final portfolio value: ${portfolio_value:,.2f}")
        print(f"Total trades executed: {len(trade_log)}")
        
        return results
    
    def _calculate_performance_metrics(self, data, price_column):
        """
        Calculate comprehensive performance metrics.
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Original data with prices
        price_column : str
            Price column name
        
        Returns:
        --------
        dict
            Performance metrics
        """
        if not self.portfolio_values:
            return {}
        
        # Convert portfolio values to DataFrame
        portfolio_df = pd.DataFrame(self.portfolio_values)
        portfolio_df.set_index('Date', inplace=True)
        
        # Strategy performance
        final_value = portfolio_df['Portfolio_Value'].iloc[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital
        
        # Buy and hold performance
        start_price = data[price_column].iloc[0]
        end_price = data[price_column].iloc[-1]
        buy_hold_return = (end_price - start_price) / start_price
        buy_hold_final_value = self.initial_capital * (1 + buy_hold_return)
        
        # Calculate daily returns for additional metrics
        portfolio_df['Daily_Return'] = portfolio_df['Portfolio_Value'].pct_change()
        
        # Risk metrics
        volatility = portfolio_df['Daily_Return'].std() * np.sqrt(252)  # Annualized
        sharpe_ratio = (total_return * 252) / (volatility * 252) if volatility > 0 else 0
        
        # Drawdown calculation
        portfolio_df['Peak'] = portfolio_df['Portfolio_Value'].expanding().max()
        portfolio_df['Drawdown'] = (portfolio_df['Portfolio_Value'] - portfolio_df['Peak']) / portfolio_df['Peak']
        max_drawdown = portfolio_df['Drawdown'].min()
        
        # Win rate calculation
        if self.trades:
            profitable_trades = 0
            total_trades = len(self.trades) // 2  # Buy-sell pairs
            
            for i in range(0, len(self.trades) - 1, 2):
                if i + 1 < len(self.trades):
                    buy_trade = self.trades[i]
                    sell_trade = self.trades[i + 1]
                    if sell_trade['Proceeds'] > buy_trade['Cost']:
                        profitable_trades += 1
            
            win_rate = profitable_trades / total_trades if total_trades > 0 else 0
        else:
            win_rate = 0
            total_trades = 0
        
        # Compile results
        results = {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return_pct': total_return * 100,
            'buy_hold_return_pct': buy_hold_return * 100,
            'buy_hold_final_value': buy_hold_final_value,
            'excess_return_pct': (total_return - buy_hold_return) * 100,
            'volatility_pct': volatility * 100,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown_pct': max_drawdown * 100,
            'total_trades': len(self.trades),
            'trade_pairs': total_trades,
            'win_rate_pct': win_rate * 100,
            'portfolio_df': portfolio_df,
            'trades_df': pd.DataFrame(self.trades) if self.trades else pd.DataFrame()
        }
        
        return results
    
    def print_performance_summary(self, results):
        """
        Print a formatted performance summary.
        
        Parameters:
        -----------
        results : dict
            Results from run_backtest()
        """
        print("\n" + "="*50)
        print("BACKTEST PERFORMANCE SUMMARY")
        print("="*50)
        
        print(f"Initial Capital: ${results['initial_capital']:,.2f}")
        print(f"Final Value: ${results['final_value']:,.2f}")
        print(f"Total Return: {results['total_return_pct']:.2f}%")
        print(f"Buy & Hold Return: {results['buy_hold_return_pct']:.2f}%")
        print(f"Excess Return: {results['excess_return_pct']:.2f}%")
        
        print(f"\nRisk Metrics:")
        print(f"Volatility: {results['volatility_pct']:.2f}%")
        print(f"Sharpe Ratio: {results['sharpe_ratio']:.3f}")
        print(f"Max Drawdown: {results['max_drawdown_pct']:.2f}%")
        
        print(f"\nTrading Activity:")
        print(f"Total Trades: {results['total_trades']}")
        print(f"Trade Pairs: {results['trade_pairs']}")
        print(f"Win Rate: {results['win_rate_pct']:.1f}%")
        
        # Performance comparison
        if results['excess_return_pct'] > 0:
            print(f"\n✅ Strategy OUTPERFORMED buy-and-hold by {results['excess_return_pct']:.2f}%")
        else:
            print(f"\n❌ Strategy UNDERPERFORMED buy-and-hold by {abs(results['excess_return_pct']):.2f}%")
    
    def save_results(self, results, ticker, results_dir="results"):
        """
        Save backtest results to CSV files.
        
        Parameters:
        -----------
        results : dict
            Backtest results
        ticker : str
            Stock ticker symbol
        results_dir : str
            Directory to save results
        
        Returns:
        --------
        dict
            Paths to saved files
        """
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        saved_files = {}
        
        # Save portfolio values
        if 'portfolio_df' in results and not results['portfolio_df'].empty:
            portfolio_file = os.path.join(results_dir, f"{ticker}_portfolio_{timestamp}.csv")
            results['portfolio_df'].to_csv(portfolio_file)
            saved_files['portfolio'] = portfolio_file
            print(f"Portfolio values saved to: {portfolio_file}")
        
        # Save trades
        if 'trades_df' in results and not results['trades_df'].empty:
            trades_file = os.path.join(results_dir, f"{ticker}_trades_{timestamp}.csv")
            results['trades_df'].to_csv(trades_file, index=False)
            saved_files['trades'] = trades_file
            print(f"Trades saved to: {trades_file}")
        
        # Save summary
        summary_file = os.path.join(results_dir, f"{ticker}_summary_{timestamp}.txt")
        with open(summary_file, 'w') as f:
            f.write(f"Backtest Summary for {ticker}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Initial Capital: ${results['initial_capital']:,.2f}\n")
            f.write(f"Final Value: ${results['final_value']:,.2f}\n")
            f.write(f"Total Return: {results['total_return_pct']:.2f}%\n")
            f.write(f"Buy & Hold Return: {results['buy_hold_return_pct']:.2f}%\n")
            f.write(f"Excess Return: {results['excess_return_pct']:.2f}%\n")
            f.write(f"Volatility: {results['volatility_pct']:.2f}%\n")
            f.write(f"Sharpe Ratio: {results['sharpe_ratio']:.3f}\n")
            f.write(f"Max Drawdown: {results['max_drawdown_pct']:.2f}%\n")
            f.write(f"Total Trades: {results['total_trades']}\n")
            f.write(f"Win Rate: {results['win_rate_pct']:.1f}%\n")
        
        saved_files['summary'] = summary_file
        print(f"Summary saved to: {summary_file}")
        
        return saved_files


if __name__ == "__main__":
    # Example usage
    print("Testing backtest module...")
    
    # This would normally be called with real strategy data
    # For testing, we'll create a simple example
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    sample_data = pd.DataFrame({
        'Close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
        'Signal': [1 if i % 50 == 0 else (-1 if i % 50 == 25 else 0) for i in range(len(dates))],
        'Position': 0
    }, index=dates)
    
    # Run backtest
    bt = Backtest(initial_capital=10000)
    results = bt.run_backtest(sample_data)
    bt.print_performance_summary(results)
