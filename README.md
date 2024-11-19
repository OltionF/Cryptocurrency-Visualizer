# Cryptocurrency Visualizer

![Cryptocurrency Visualizer Banner](https://via.placeholder.com/1200x400.png?text=Cryptocurrency+Visualizer)

## Overview
The **Cryptocurrency Visualizer** is a powerful tool for monitoring, analyzing, and visualizing cryptocurrency data in real-time. This interactive dashboard provides a range of features for crypto enthusiasts, traders, and analysts, including technical indicators, price alerts, and a crypto screener. Built with Python, this tool leverages the Binance API (via `ccxt`) and modern visualization libraries to deliver an engaging user experience.

## Features
### **Real-Time Data Monitoring**
- Fetches current prices for selected cryptocurrencies (e.g., BTC/USDT, ETH/USDT).
- Displays the current trend (Buy, Sell, or Hold) based on RSI (Relative Strength Index).

### **Historical Data Fetching**
- Retrieves historical OHLCV (Open, High, Low, Close, Volume) data from Binance.
- Supports various timeframes: 1 minute, 5 minutes, 1 hour, 1 day, etc.
- Allows users to define a custom date range for analysis.

### **Interactive Charts**
- Generates candlestick charts using Plotly for visualizing price trends.
- Includes moving averages (SMA10, SMA20) overlaid on the charts.
- Offers downloadable CSV reports of historical data.

### **Technical Indicators**
- **RSI Calculation**: Measures market momentum to identify overbought or oversold conditions.
- **Moving Averages**: Calculates SMA for short- and long-term trend analysis.

### **Custom Price Alerts**
- Allows users to set target price alerts for selected cryptocurrencies.
- Triggers alerts when the current price meets or exceeds the alert threshold.

### **Crypto Screener**
- Compares top cryptocurrencies based on:
  - Current price
  - 24-hour percentage change
  - RSI value
- Displays results in a tabular format.

### **User Interface Features**
- Sidebar controls for:
  - Selecting cryptocurrencies
  - Setting date ranges
  - Choosing timeframes
  - Defining refresh intervals (10–300 seconds)
- Auto-refresh functionality for live updates.

### **Educational Insights**
- Provides in-dashboard explanations of technical indicators like RSI for beginners.

### **Error Handling**
- Displays user-friendly error messages when data cannot be fetched.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - `ccxt` for interacting with Binance API
  - `streamlit` for building the interactive web application
  - `pandas` for data manipulation
  - `plotly` for data visualization
  - `streamlit-autorefresh` for auto-refreshing the dashboard

---

## Installation

### Prerequisites
- Python 3.8+ installed on your system.
- pip (Python package manager) installed.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cryptocurrency-visualizer.git
   cd cryptocurrency-visualizer
