# OLTION F CRYPTOCURRENCY VISUALIZER

import ccxt
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# Initialize the Binance exchange
exchange = ccxt.binance()

# Convert timeframe to milliseconds
def timeframe_to_milliseconds(timeframe):
    unit = timeframe[-1]
    value = int(timeframe[:-1])
    if unit == 'm':
        return value * 60 * 1000
    elif unit == 'h':
        return value * 60 * 60 * 1000
    elif unit == 'd':
        return value * 24 * 60 * 60 * 1000
    elif unit == 'w':
        return value * 7 * 24 * 60 * 60 * 1000
    else:
        return None

# Fetch historical data with pagination to ensure data up to current time
def fetch_historical_data(symbol, timeframe='1d', since=None, limit=None):
    try:
        all_ohlcv = []
        since_timestamp = int(pd.to_datetime(since).timestamp() * 1000) if since else None
        end_timestamp = int(pd.to_datetime(end_date).timestamp() * 1000)
        timeframe_ms = timeframe_to_milliseconds(timeframe)
        while True:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since_timestamp, limit=1000)
            if not ohlcv:
                break
            all_ohlcv.extend(ohlcv)
            last_timestamp = ohlcv[-1][0]
            # Increment since_timestamp to the last timestamp plus one timeframe
            since_timestamp = last_timestamp + timeframe_ms
            if since_timestamp >= end_timestamp:
                break
            # Avoid infinite loops
            if len(ohlcv) < 1000:
                break
        df = pd.DataFrame(all_ohlcv, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df.drop_duplicates(subset='Timestamp', inplace=True)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        # Filter data between start_date and end_date
        mask = (df['Timestamp'] >= pd.to_datetime(since)) & (df['Timestamp'] <= pd.to_datetime(end_date))
        df = df.loc[mask]
        df.sort_values('Timestamp', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

# Fetch current price without caching
def fetch_current_price(symbol):
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.error(f"Error fetching current price for {symbol}: {e}")
        return None

# Calculate RSI
def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, -0.0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Determine the trend based on RSI
def determine_trend(rsi):
    if rsi < 30:
        return "Buy"
    elif rsi > 70:
        return "Sell"
    else:
        return "Hold"

# Streamlit UI
st.title("Advanced Cryptocurrency Trend Visualizer")

# Sidebar for Settings
st.sidebar.title("Settings")

# Select cryptocurrencies
crypto_symbols = st.sidebar.multiselect(
    "Select Cryptocurrencies",
    ["BTC/USDT", "ETH/USDT", "BNB/USDT", "ADA/USDT", "XRP/USDT", "DOGE/USDT"],
    ["BTC/USDT"]
)

# Select timeframe
timeframe = st.sidebar.selectbox("Select Timeframe", ['1m', '5m', '15m', '30m', '1h', '4h', '1d'], index=6)

# Date range selection
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime('today'))

# Refresh interval
interval = st.sidebar.slider("Refresh Interval (seconds)", min_value=10, max_value=300, value=60)

# Start and Stop buttons
start_button = st.sidebar.button("Start Monitoring")
stop_button = st.sidebar.button("Stop Monitoring")

# Sidebar for Price Alerts
st.sidebar.header("Price Alerts")
alerts = {}
for symbol in crypto_symbols:
    alert_price = st.sidebar.number_input(f"Set alert price for {symbol}", min_value=0.0, value=0.0)
    if alert_price > 0:
        alerts[symbol] = alert_price

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state['monitoring'] = False

if start_button:
    st.session_state['monitoring'] = True
if stop_button:
    st.session_state['monitoring'] = False

if st.session_state['monitoring']:
    # Auto-refresh the page every 'interval' seconds
    st_autorefresh(interval=interval * 1000, key="crypto_autorefresh")

    # Fetch and display current price and trend
    st.subheader("Current Prices and Trends")

    for symbol in crypto_symbols:
        current_price = fetch_current_price(symbol)
        if current_price is not None:
            # Fetch recent data for RSI calculation
            df_recent = fetch_historical_data(symbol, timeframe='1h', since=pd.to_datetime('now') - timedelta(days=7))
            if not df_recent.empty:
                df_recent['RSI'] = calculate_rsi(df_recent['Close'], period=14)
                current_rsi = df_recent['RSI'].iloc[-1]
                trend = determine_trend(current_rsi)
            else:
                trend = "No Data"

            # Display current price and trend in large text
            st.markdown(f"""
                <div style='text-align: center;'>
                    <h1>{symbol}</h1>
                    <h2>Current Price: ${current_price:,.2f}</h2>
                    <h3>Trend: {trend}</h3>
                </div>
                <hr>
            """, unsafe_allow_html=True)
        else:
            st.write(f"Could not fetch current price for {symbol}")

    # Tabs for organizing content
    tab1, tab2, tab3 = st.tabs(["Charts", "Indicators", "Screener"])

    with tab1:
        st.subheader("Price Charts")

        for symbol in crypto_symbols:
            # Fetch historical data
            df = fetch_historical_data(symbol, timeframe=timeframe, since=start_date)

            if df.empty:
                continue

            # Plot interactive chart
            fig = go.Figure()

            # Price Candlesticks
            fig.add_trace(go.Candlestick(
                x=df['Timestamp'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ))

            # Update layout
            fig.update_layout(
                title=f"{symbol} Price Chart",
                xaxis_title="Time",
                yaxis_title="Price (USDT)",
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Include Downloadable Reports
            csv = df.to_csv(index=False)
            st.download_button(
                label=f"Download {symbol} Data as CSV",
                data=csv,
                file_name=f'{symbol.replace("/", "_")}_data.csv',
                mime='text/csv',
            )

    with tab2:
        st.subheader("Technical Indicators")

        for symbol in crypto_symbols:
            # Fetch historical data
            df = fetch_historical_data(symbol, timeframe=timeframe, since=start_date)

            if df.empty:
                continue

            # Calculate indicators
            df['SMA_10'] = df['Close'].rolling(window=10).mean()
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['RSI'] = calculate_rsi(df['Close'], period=14)

            # Plot indicators
            fig = go.Figure()

            # Price Line
            fig.add_trace(go.Scatter(
                x=df['Timestamp'],
                y=df['Close'],
                line=dict(color='black', width=1),
                name='Close Price'
            ))

            # Add Moving Averages
            fig.add_trace(go.Scatter(
                x=df['Timestamp'],
                y=df['SMA_10'],
                line=dict(color='blue', width=1),
                name='SMA 10'
            ))
            fig.add_trace(go.Scatter(
                x=df['Timestamp'],
                y=df['SMA_20'],
                line=dict(color='orange', width=1),
                name='SMA 20'
            ))

            # Update layout
            fig.update_layout(
                title=f"{symbol} Moving Averages",
                xaxis_title="Time",
                yaxis_title="Price (USDT)",
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Plot RSI
            fig_rsi = go.Figure()

            fig_rsi.add_trace(go.Scatter(
                x=df['Timestamp'],
                y=df['RSI'],
                line=dict(color='green', width=1),
                name='RSI'
            ))

            # Add overbought/oversold lines
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="blue")

            # Update layout
            fig_rsi.update_layout(
                title=f"{symbol} RSI Indicator",
                xaxis_title="Time",
                yaxis_title="RSI",
                yaxis=dict(range=[0, 100])
            )

            st.plotly_chart(fig_rsi, use_container_width=True)

            # Educational Resources
            with st.expander("What is RSI?"):
                st.write("""
                The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
                RSI oscillates between zero and 100. Traditionally, RSI is considered overbought when above 70 and oversold when below 30.
                """)

    with tab3:
        st.subheader("Crypto Screener")

        top_symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "ADA/USDT", "XRP/USDT", "DOGE/USDT", "SOL/USDT", "DOT/USDT", "LTC/USDT"]

        screener_data = []
        for symbol in top_symbols:
            df = fetch_historical_data(symbol, timeframe='1d', since=pd.to_datetime('now') - timedelta(days=2))
            if not df.empty and len(df) >= 2:
                current_price = df['Close'].iloc[-1]
                previous_price = df['Close'].iloc[-2]
                change_pct = ((current_price - previous_price) / previous_price) * 100
                rsi = calculate_rsi(df['Close'], period=14).iloc[-1]
                screener_data.append({
                    'Symbol': symbol,
                    'Price': f"${current_price:,.2f}",
                    '24h Change (%)': f"{change_pct:.2f}%",
                    'RSI': f"{rsi:.2f}"
                })

        screener_df = pd.DataFrame(screener_data)
        st.dataframe(screener_df)

    # Check for alerts
    for symbol, alert_price in alerts.items():
        current_price = fetch_current_price(symbol)
        if current_price is not None and current_price >= alert_price:
            st.warning(f"🚨 **Alert:** {symbol} has reached or exceeded your alert price of ${alert_price:,.2f}!")

    # Display last updated time
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
else:
    st.write("Click **Start Monitoring** to begin fetching data.")
