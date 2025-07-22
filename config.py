"""
Configuration File for Stock Trading Strategy

This file contains all the settings you can easily modify to customize
your trading strategy analysis. Edit the values below and run main.py.

Author: Stock Trading Strategy Project
"""

# =============================================================================
# STOCK SELECTION
# =============================================================================

# Primary stock to analyze
TICKER = "AAPL"

# Alternative stocks to try (uncomment one and comment out AAPL above):
# TICKER = "MSFT"    # Microsoft
# TICKER = "GOOGL"   # Google/Alphabet
# TICKER = "TSLA"    # Tesla
# TICKER = "AMZN"    # Amazon
# TICKER = "NVDA"    # NVIDIA
# TICKER = "SPY"     # S&P 500 ETF
# TICKER = "QQQ"     # NASDAQ ETF
# TICKER = "VTI"     # Total Stock Market ETF

# =============================================================================
# TIME PERIOD
# =============================================================================

# Date range for analysis (format: "YYYY-MM-DD")
START_DATE = "2022-01-01"
END_DATE = "2024-01-01"

# Alternative time periods (uncomment to use):
# START_DATE = "2020-01-01"  # Longer period (includes COVID crash)
# START_DATE = "2023-01-01"  # Recent year only
# END_DATE = None            # Use None for current date

# =============================================================================
# STRATEGY PARAMETERS
# =============================================================================

# Moving Average periods (in days)
SHORT_MA = 50    # Short-term moving average
LONG_MA = 200    # Long-term moving average

# Popular alternative combinations:
# SHORT_MA, LONG_MA = 20, 50    # More sensitive (more trades)
# SHORT_MA, LONG_MA = 10, 30    # Very sensitive (many trades)
# SHORT_MA, LONG_MA = 100, 300  # Less sensitive (fewer trades)

# =============================================================================
# BACKTESTING PARAMETERS
# =============================================================================

# Starting capital for backtest
INITIAL_CAPITAL = 10000  # $10,000

# Commission rate per trade (as decimal)
COMMISSION = 0.001  # 0.1% commission

# Alternative commission rates:
# COMMISSION = 0.0    # No commission (unrealistic but good for testing)
# COMMISSION = 0.005  # 0.5% commission (higher cost)
# COMMISSION = 0.0025 # 0.25% commission (moderate cost)

# =============================================================================
# OUTPUT SETTINGS
# =============================================================================

# Directory to save results
RESULTS_DIR = "results"

# File naming options
INCLUDE_TIMESTAMP = True  # Add timestamp to filenames
SAVE_PLOTS = True         # Save plot images
SAVE_DATA = True          # Save CSV data files
SHOW_PLOTS = False        # Display plots on screen (set to False for testing)

# Plot settings
PLOT_DPI = 300           # Image resolution (300 is high quality)
PLOT_FORMAT = "png"      # Image format: "png", "jpg", "pdf"

# =============================================================================
# ADVANCED SETTINGS (for experienced users)
# =============================================================================

# Price column to use for calculations
PRICE_COLUMN = "Close"   # Options: "Close", "Adj Close", "Open"

# Data validation settings
MIN_DATA_POINTS = 250    # Minimum days of data required
FILL_MISSING_DATA = True # Forward-fill missing data points

# Risk-free rate for Sharpe ratio calculation (annual rate as decimal)
RISK_FREE_RATE = 0.02    # 2% annual risk-free rate

# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================

def get_conservative_config():
    """Conservative strategy with longer moving averages."""
    return {
        'SHORT_MA': 100,
        'LONG_MA': 300,
        'COMMISSION': 0.001
    }

def get_aggressive_config():
    """Aggressive strategy with shorter moving averages."""
    return {
        'SHORT_MA': 10,
        'LONG_MA': 30,
        'COMMISSION': 0.001
    }

def get_classic_config():
    """Classic golden cross strategy."""
    return {
        'SHORT_MA': 50,
        'LONG_MA': 200,
        'COMMISSION': 0.001
    }

# =============================================================================
# POPULAR STOCK LISTS
# =============================================================================

# Technology stocks
TECH_STOCKS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX"]

# Blue chip stocks
BLUE_CHIP_STOCKS = ["AAPL", "MSFT", "JNJ", "PG", "KO", "DIS", "WMT", "V"]

# ETFs for diversified analysis
POPULAR_ETFS = ["SPY", "QQQ", "VTI", "IWM", "EFA", "VWO", "BND", "GLD"]

# Crypto-related stocks
CRYPTO_STOCKS = ["COIN", "MSTR", "RIOT", "MARA", "SQ", "PYPL"]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def apply_preset(preset_name):
    """Apply a preset configuration."""
    global SHORT_MA, LONG_MA, COMMISSION
    
    if preset_name.lower() == "conservative":
        config = get_conservative_config()
    elif preset_name.lower() == "aggressive":
        config = get_aggressive_config()
    elif preset_name.lower() == "classic":
        config = get_classic_config()
    else:
        print(f"Unknown preset: {preset_name}")
        return
    
    SHORT_MA = config['SHORT_MA']
    LONG_MA = config['LONG_MA']
    COMMISSION = config['COMMISSION']
    
    print(f"Applied {preset_name} preset:")
    print(f"  Short MA: {SHORT_MA} days")
    print(f"  Long MA: {LONG_MA} days")
    print(f"  Commission: {COMMISSION*100:.2f}%")

def validate_config():
    """Validate the current configuration."""
    errors = []
    
    if SHORT_MA >= LONG_MA:
        errors.append("SHORT_MA must be less than LONG_MA")
    
    if INITIAL_CAPITAL <= 0:
        errors.append("INITIAL_CAPITAL must be positive")
    
    if COMMISSION < 0 or COMMISSION > 0.1:
        errors.append("COMMISSION should be between 0 and 0.1 (10%)")
    
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("Configuration is valid ✅")
    return True

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

if __name__ == "__main__":
    print("Stock Trading Strategy Configuration")
    print("="*40)
    print(f"Current settings:")
    print(f"  Ticker: {TICKER}")
    print(f"  Period: {START_DATE} to {END_DATE}")
    print(f"  Strategy: {SHORT_MA}/{LONG_MA} day MA crossover")
    print(f"  Capital: ${INITIAL_CAPITAL:,}")
    print(f"  Commission: {COMMISSION*100:.2f}%")
    print()
    
    # Validate configuration
    validate_config()
    
    print("\nTo use different presets, run:")
    print("  from config import apply_preset")
    print("  apply_preset('conservative')")
    print("  apply_preset('aggressive')")
    print("  apply_preset('classic')")
    
    print("\nPopular stocks to try:")
    print(f"  Tech: {', '.join(TECH_STOCKS[:5])}")
    print(f"  ETFs: {', '.join(POPULAR_ETFS[:5])}")
    print(f"  Blue Chip: {', '.join(BLUE_CHIP_STOCKS[:5])}")
