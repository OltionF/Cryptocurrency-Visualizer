# Cryptocurrency Visualizer

![Cryptocurrency Visualizer Banner](https://via.placeholder.com/1200x400.png?text=Cryptocurrency+Visualizer)

## Overview
The **Cryptocurrency Visualizer** is a Python-based application that helps users monitor cryptocurrency trends, visualize price data, and calculate key technical indicators. The dashboard is built using [Streamlit](https://streamlit.io/) and utilizes Binance's API via the [ccxt library](https://github.com/ccxt/ccxt) for real-time data retrieval.

## Features
- **Real-time Data Monitoring**: Fetches current prices and trends for selected cryptocurrencies.
- **Interactive Charts**: Visualize historical price data using candlestick charts.
- **Technical Indicators**:
  - Relative Strength Index (RSI)
  - Simple Moving Averages (SMA)
- **Custom Price Alerts**: Set alert thresholds and receive notifications in the dashboard.
- **Crypto Screener**: Quickly compare multiple cryptocurrencies based on price changes and RSI.
- **Downloadable Reports**: Export historical data as CSV files.

## Technologies Used
- **Python**
  - Libraries: `streamlit`, `ccxt`, `plotly`, `pandas`, `datetime`
- **Binance API** via `ccxt`
- **Streamlit Auto-refresh** for live updates

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cryptocurrency-visualizer.git
   cd cryptocurrency-visualizer
