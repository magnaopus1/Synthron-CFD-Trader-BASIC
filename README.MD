```

SYNTHRON CFD Trader
BY MAGNA OPUS TECHNOLOGIES

```

Welcome to the **SYNTHRON CFD Trader**, a cutting-edge platform designed for seamless Contract for Difference (CFD) trading. This system combines world-class technologies with advanced trading strategies to empower traders and institutions.

---

## 🚀 **About the Application**

The SYNTHRON CFD Trader integrates:
- **Live Trading:** Executes single-asset and pairwise trading strategies in real-time.
- **Backtesting:** Simulates historical trading scenarios for performance evaluation.
- **Performance Monitoring:** Tracks and analyzes trading results using advanced metrics.

This application is built with Python, leveraging the **MetaTrader 5 API**, and implements the latest strategies for trend-following, mean reversion, breakout trading, momentum trading, scalping, and cointegration.

---

## 🛠 **Features**

### 🎯 **Core Functionalities**
1. **Live Trading**
   - Implements advanced trading strategies for single assets and asset pairs.
   - Monitors live market data and executes trades based on calculated signals.
   - Includes robust risk management, position scaling, and exposure control.

2. **Backtesting**
   - Simulates trading strategies on historical market data.
   - Evaluates performance metrics such as Sharpe Ratio, Maximum Drawdown, and Win Rate.
   - Exports results to detailed reports for analysis.

3. **Performance Metrics**
   - Provides a comprehensive summary of trades, balance history, and overall performance.
   - Generates performance reports in `.xlsx` format for easy sharing and documentation.

### 🧠 **Strategies**
- **Trend Following**: Uses moving averages to capture market trends.
- **Mean Reversion**: Identifies overbought or oversold conditions using Z-score and RSI.
- **Breakout Strategy**: Detects volatility-driven price breakouts using Bollinger Bands and EMA.
- **Momentum Strategy**: Capitalizes on market momentum confirmed by RSI and Z-score.
- **Scalping**: Executes fast trades based on short-term EMAs and RSI.
- **Cointegration Strategy**: Exploits statistical relationships between pairs of assets.

### 🔒 **Risk Management**
- Configurable maximum drawdown, per-trade risk, and leverage settings.
- Automatically calculates stop-loss and take-profit levels.
- Validates trading conditions to avoid overexposure and high spreads.

---

## 💻 **How to Use**

### 1️⃣ **Run the Application**
Execute the main script in the terminal:
```bash
python main.py
```

### 2️⃣ **Menu Options**
1: **Start Live Trading**  
   Initiates real-time trading based on configured strategies and market data.  

2: **Run Backtesting**  
   Simulates historical trading scenarios to evaluate strategy performance.  

3: **View Performance Metrics**  
   Displays a summary of trading performance in logs and reports.  

4: **Exit**  
   Safely shuts down the system.  

---

## 📂 **Directory Structure**
- **`config/`**: Manages configurations and MetaTrader 5 API integration.  
- **`data/`**: Handles data fetching, preprocessing, and indicator calculations.  
- **`strategies/`**: Implements trading strategies, position management, and risk control.  
- **`performance/`**: Provides backtesting, performance metrics, and reporting tools.  
- **`utils/`**: Contains helper functions, logging, and exception handling.  

---

## 🛡 **System Requirements**
- Python 3.8+  
- MetaTrader 5 account  
- Dependencies installed using:
  ```bash
  pip install -r requirements.txt
  ```

---

## 🧩 **Technologies Used**
- **MetaTrader 5 API**: Real-time market data and trading execution.
- **Pandas**: Data manipulation and analysis.
- **NumPy**: Numerical operations.
- **Matplotlib**: Data visualization.
- **Scikit-learn**: Machine learning utilities.
- **Statsmodels**: Statistical modeling.

---

## 📖 **Contributing**
Feel free to contribute to **SYNTHRON CFD Trader**! Fork the repository, make your improvements, and submit a pull request.

---

## 📬 **Support**
For any queries, contact **Magna Opus Technologies**  
Twitter: @MagnaOpusTech  
Instagram: @MagnaOpusTech

---

## ⚖ **License**
This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

> **Disclaimer:**  
> This application does not provide financial advice; it is a tool deployed solely by the user. No guarantee of monetary gain is provided, and users assume all risks, including potential loss of capital. Ensure legal compliance within your jurisdiction before use.

