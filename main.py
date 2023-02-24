from historical_data import get_klines_df
from binance.client import Client

# main
if __name__ == '__main__':
    symbol = "ETHBUSD"
    interval = Client.KLINE_INTERVAL_30MINUTE
    klines = get_klines_df(symbol, interval)
