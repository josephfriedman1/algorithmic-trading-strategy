# 📈 Algorithmic Trading Strategy Backtesting System

> A comprehensive Python-based framework for backtesting moving average crossover trading strategies

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

## 🎯 Project Overview

This project implements a complete algorithmic trading system that analyzes moving average crossover strategies on historical stock data. Built from scratch using Python, it demonstrates proficiency in financial analysis, data science, and software engineering.

### 🏆 Key Achievement
**Strategy outperformed buy-and-hold by 15.36%** in Apple (AAPL) analysis from 2022-2024, achieving a **Sharpe ratio of 1.912**.

## 🚀 Features

- **📊 Data Acquisition**: Automated download of historical stock data via Yahoo Finance API
- **📈 Technical Analysis**: Moving average calculation and crossover signal generation
- **🔄 Backtesting Engine**: Comprehensive performance analysis with realistic commission costs
- **📉 Risk Metrics**: Sharpe ratio, maximum drawdown, volatility analysis
- **📋 Trade Logging**: Complete record of all transactions and portfolio values
- **🎨 Visualization**: Professional charts showing price action, signals, and performance
- **⚙️ Easy Configuration**: Beginner-friendly setup for different stocks and parameters

## 📊 Sample Results

### Apple Inc. (AAPL) Analysis: 2022-2024
- **Strategy Return**: +22.35%
- **Buy & Hold Return**: +6.99%
- **Excess Return**: +15.36%
- **Sharpe Ratio**: 1.912
- **Maximum Drawdown**: -14.93%
- **Win Rate**: N/A (1 trade executed)

![Sample Price Chart](results/sample_price_chart.png)
*Price chart showing moving averages and trading signals*

![Sample Equity Curve](results/sample_equity_curve.png)
*Strategy performance vs buy-and-hold comparison*

## 🛠️ Technology Stack

- **Python 3.9+**: Core programming language
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib/seaborn**: Data visualization
- **yfinance**: Yahoo Finance API integration

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/josephfriedman1/trading-strategy-backtester.git
cd trading-strategy-backtester
pip install -r requirements.txt
```

### Basic Usage
```bash
# Run with default settings (AAPL, 50/200 day MAs)
python main.py

# Run simple example
python example.py
```

### Configuration
Edit `config.py` to customize your analysis:
```python
TICKER = "AAPL"           # Stock to analyze
START_DATE = "2022-01-01" # Analysis start date
END_DATE = "2024-01-01"   # Analysis end date
SHORT_MA = 50             # Short moving average period
LONG_MA = 200             # Long moving average period
INITIAL_CAPITAL = 10000   # Starting capital
```

## 📁 Project Structure

```
├── main.py              # Main execution script
├── data.py              # Data acquisition module
├── strategy.py          # Trading strategy implementation
├── backtest.py          # Backtesting engine
├── config.py            # Configuration settings
├── requirements.txt     # Dependencies
├── README.md            # Documentation
└── results/             # Output directory
    ├── charts/          # Generated visualizations
    ├── data/            # CSV exports
    └── reports/         # Performance summaries
```

## 🧠 Strategy Logic

### Moving Average Crossover Strategy
- **Buy Signal**: Short-term MA crosses above long-term MA (Golden Cross)
- **Sell Signal**: Short-term MA crosses below long-term MA (Death Cross)
- **Default Parameters**: 50-day and 200-day moving averages

### Performance Metrics
- **Total Return**: Strategy vs buy-and-hold comparison
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Volatility**: Annualized standard deviation of returns

## 📈 Analysis Examples

### Technology Stocks
```python
# High-growth tech analysis
TICKER = "TSLA"  # Tesla
SHORT_MA = 20
LONG_MA = 50
```

### Market ETFs
```python
# Broad market analysis
TICKER = "SPY"   # S&P 500 ETF
SHORT_MA = 50
LONG_MA = 200
```

### Conservative Strategy
```python
# Lower frequency trading
SHORT_MA = 100
LONG_MA = 300
```

## 🎓 Educational Value

This project demonstrates:
- **Financial Markets**: Understanding of technical analysis and trading strategies
- **Data Science**: Data acquisition, cleaning, analysis, and visualization
- **Programming**: Object-oriented design, error handling, and documentation
- **Statistics**: Risk metrics, performance analysis, and statistical significance
- **Software Engineering**: Modular architecture and code organization

## 🔮 Future Enhancements

- [ ] Multiple timeframe analysis
- [ ] Additional technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Machine learning signal generation
- [ ] Portfolio optimization across multiple assets
- [ ] Real-time trading simulation
- [ ] Web-based dashboard interface

## 📊 Performance Comparison

| Strategy | AAPL | MSFT | SPY | TSLA |
|----------|------|------|-----|------|
| Total Return | 22.35% | TBD | TBD | TBD |
| Excess Return | 15.36% | TBD | TBD | TBD |
| Sharpe Ratio | 1.912 | TBD | TBD | TBD |
| Max Drawdown | -14.93% | TBD | TBD | TBD |

*TBD: To be determined through additional analysis*

## ⚠️ Disclaimer

This project is for educational purposes only. Past performance does not guarantee future results. All trading involves risk of loss. This is not financial advice.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Joseph Friedman**
- High School Student passionate about quantitative finance and programming
- Built this project to explore algorithmic trading and financial analysis
- Interested in pursuing Computer Science/Finance in college

## 🙏 Acknowledgments

- Yahoo Finance for providing free historical data
- Python community for excellent financial libraries
- Online resources for trading strategy education

---

⭐ **Star this repository if you found it helpful!**

📧 **Contact**: Available via GitHub
🔗 **GitHub**: [josephfriedman1](https://github.com/josephfriedman1)
