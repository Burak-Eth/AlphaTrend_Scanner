import pandas as pd
import pandas_ta as ta
from datetime import datetime as dt
from urllib.parse import urljoin
import urllib.request
from time import sleep as slp
import requests as r
import json

# Your Telegram ID 
yourTelegramId = "YOUR TELEGRAM ID"

# Function to send a message using the Telegram Bot API
def telegram_send_message(bot_message, chat_id):
    bot_token = "YOUR TELEGRAM BOT'S TOKEN HERE"
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={bot_message}'
    response = r.get(url)
    return response

BASE_URL = "https://fapi.binance.com/"

# Function to get the current minute
def current_minute():
    return dt.now().strftime("%M")

# Function to convert timestamp to human-readable date
def timestamp_to_human_readable(timestamp):
    return dt.fromtimestamp(timestamp / 1000)

# Function to retrieve a list of all available trading symbols
def get_all_symbols():
    response = urllib.request.urlopen(f"{BASE_URL}fapi/v1/exchangeInfo").read()
    return [symbol['symbol'] for symbol in json.loads(response)['symbols']]

# Function to retrieve trading data for a specific symbol
def get_symbol_data(symbol_name, period, limit):
    params = {
        'url': BASE_URL, 'symbol': symbol_name, 'interval': period, 'limit': limit
    }
    url = urljoin(BASE_URL, "fapi/v1/klines/")
    payload = {}
    headers = {'Content-Type': 'application/json'}
    response = r.request('GET', url, headers=headers, params=params).json()
    columns = ["Opentime", "Open", "High", "Low", "Close", "volume", "Close time", "quote asset Close",
               "number of trades", "taker buy base asset volume", "taker buy quote asset volume", "can be ignored"]
    return pd.DataFrame(response, columns=columns, dtype=float)

# Function to calculate Alpha Trend values for a given coin
def at_scan(coin):
    coindata_raw = get_symbol_data(coin, "1h", "150")
    df = coindata_raw
    open_price, close, high, low, volume = df['Open'], df['Close'], df['High'], df['Low'], df['volume']
    ap, coeff = 14, 1
    noVolumeData = False
    tr, atr = ta.true_range(high, low, close), ta.sma(tr, ap)
    upt, down_t, hlc3, k1, k2, alpha_trend = [], [], [], [], [], [0.0]
    src, rsi, mfi = close, ta.rsi(src, 14), ta.mfi(high, low, close, volume, 14)
    
    for i in range(len(close)):
        hlc3.append((high[i] + low[i] + close[i]) / 3)
    
    for i in range(len(low)):
        upt.append(low[i] - (atr[i] * coeff) if not pd.isna(atr[i]) else 0)
    
    for i in range(len(high)):
        down_t.append(high[i] + (atr[i] * coeff) if not pd.isna(atr[i]) else 0)
    
    for i in range(1, len(close)):
        if (not noVolumeData and mfi[i] >= 50) or (noVolumeData and rsi[i] >= 50):
            alpha_trend.append(upt[i] if upt[i] >= alpha_trend[i - 1] else alpha_trend[i - 1])
        else:
            alpha_trend.append(down_t[i] if down_t[i] <= alpha_trend[i - 1] else alpha_trend[i - 1])
    
    for i in range(len(alpha_trend)):
        k2.append(0 if i < 2 else alpha_trend[i - 2])
        k1.append(alpha_trend[i])
    
    at = pd.DataFrame(data=k1, columns=['k1'])
    at['k2'] = k2
    return at

# Function to determine whether to Buy or Sell based on Alpha Trend values
def at_scanner(coin):
    at = at_scan(coin)
    k1, k2 = at['k1'], at['k2']
    if k1[len(k1) - 2] <= k2[len(k2) - 2] and k1[len(k1) - 1] > k2[len(k2) - 1]:
        return "Buy"
    elif k1[len(k1) - 2] >= k2[len(k2) - 2] and k1[len(k1) - 1] < k2[len(k2) - 1]:
        return "Sell"

# Function to optimize DCA strategy for a symbol
def DCA_optimizer(symbol):
    wallet, buy_count, total_coins, sell_count, commission_rate, commission = 100, 0, 0, 0, 75/10000, 0
    coin_data = get_symbol_data(symbol, "1h", "1000")
    df, close = coin_data, coin_data['Close']
    at, k1, k2, signal_sequence = at_scan(symbol), at['k1'], at['k2'], ['Sell']
    
    for i in range(1, at.shape[0]):
        if k1[i - 1] <= k2[i - 1] and k1[i] > k2[i] and signal_sequence[-1] != 'Buy':
            buy_count += 1
            total_coins = wallet / close[i]
            commission += commission_rate * wallet
            signal_sequence.append('Buy')
        elif k1[i - 1] >= k2[i - 1] and k1[i] < k2[i] and signal_sequence[-1] != 'Sell':
            sell_count += 1
            commission += commission_rate * wallet
            signal_sequence.append('Sell')
            wallet = total_coins * close[i]
            total_coins = 0
    
    return float(wallet) - 100

# Function to get the last signal (Buy/Sell) from DCA strategy
def DCA_get_list(symbol):
    coin_data = get_symbol_data(symbol, "1h", "1000") #optimizasyon
    df, close = coin_data, coin_data['Close']
    at, k1, k2, signal_sequence = at_scan(symbol), at['k1'], at['k2'], ['Sell']
    
    for i in range(1, at.shape[0]):
        if k1[i - 1] <= k2[i - 1] and k1[i] > k2[i] and signal_sequence[-1] != 'Buy':
            signal_sequence.append('Buy')
        elif k1[i - 1] >= k2[i - 1] and k1[i] < k2[i] and signal_sequence[-1] != 'Sell':
            signal_sequence.append('Sell')

    return signal_sequence[-1]

# Retrieve a list of all trading symbols
symbol_list = get_all_symbols()
successful_list = []
initial_sell_list = []
initial_buy_list = []
return_dict = {}

# Optimize DCA strategy for each symbol and build successful_list and return_dict
for symbol in symbol_list:
    if DCA_optimizer(symbol) >= 15:  # Enter the minimum percentage of profit that coins should achieve to be included in the successful list.
        return_value = DCA_optimizer(symbol)
        successful_list.append(symbol)
        print(f"{symbol}: {return_value}%")
        return_dict[symbol] = return_value

# Determine initial buy/sell list based on last signal from DCA strategy
for symbol in successful_list:
    if DCA_get_list(symbol) == "Buy":
        initial_buy_list.append(symbol)
    elif DCA_get_list(symbol) == "Sell":
        initial_sell_list.append(symbol)

# Initialize start and query flags
start = False
query = True

# Wait until the beginning of the hour if it's not the start of the hour
if int(current_minute()) != 0:
    print(f"Waiting for: {60 - int(current_minute())} minutes...")

# Main loop for scanning and sending Telegram messages
while query:
    if int(current_minute()) == 0:
        start = True
    while start:
        print("Scanning commenced...")
        buy_signal = []
        sell_signal = []

        # Scan successful_list and update buy/sell signals
        for symbol in successful_list:
            if at_scanner(symbol) == "Buy" and symbol not in initial_buy_list:
                buy_signal.append(symbol)
                initial_buy_list.append(symbol)
                initial_sell_list.remove(symbol)
            elif at_scanner(symbol) == "Sell" and symbol not in initial_sell_list:
                sell_signal.append(symbol)
                initial_sell_list.append(symbol)
                initial_buy_list.remove(symbol)

        print("Scanning Completed...")

        # Prepare and send Telegram message if buy/sell signals are present
        buy_signal_msg = str(buy_signal)
        sell_signal_msg = str(sell_signal)
        message = f"AlphaTrend Scanner\n \nBuy Signals:\n{buy_signal_msg}\nSell Signals:\n{sell_signal_msg}\n \nReturn List:\n{str(return_dict)}"

        if len(buy_signal) > 0 or len(sell_signal) > 0:
            telegram_send_message(message, yourTelegramId)

        start = False
    slp(45)  # Sleep for 45 seconds before the next iteration
