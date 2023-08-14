from realtime_class import RealTimeKLine
from utils import line_print
from binance.client import Client
from config import binance_key, binance_secret
import pandas as pd


def strategy_breakout(data_new):
    data = data_new.copy()
    data['position'] = None
    data['ceil'] = data.rolling(20)['high'].max().shift(1)
    data['floor'] = data.rolling(20)['low'].min().shift(1)
    data.loc[data['close'] > data['ceil'], 'position'] = 1
    data.loc[data['close'] < data['floor'], 'position'] = -1
    data['position'].fillna(method='ffill', inplace=True)
    return data['position'].iloc[-1]


client = Client(binance_key, binance_secret)
symbol = 'BTCBUSD'
interval = '5m'
realtime_kline = RealTimeKLine(symbol.lower(), interval)


time_format = '%Y/%m/%d %H:%M'
margin_unit = 0.01
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(time_format)
    position = strategy_breakout(data)
    strategy_position = margin_unit * position
    line_print(
        f"\n{symbol}\n時間:{latest_time}\n收盤價:{latest_close}\n突破策略當前部位:{position}")

    # 取得當前部位
    futures_positions = pd.DataFrame(client.futures_position_information())
    futures_position = float(
        futures_positions.loc[futures_positions['symbol'] == symbol, 'positionAmt'].iloc[0])
    # 與策略部位同步
    if strategy_position != futures_position:
        order_qty = round(strategy_position - futures_position, 8)
        if order_qty > 0:
            client.futures_create_order(
                symbol=symbol,
                type='MARKET',  # 下單(市價)
                side='BUY',
                quantity=order_qty
            )
        else:
            client.futures_create_order(
                symbol=symbol,
                type='MARKET',
                side='SELL',
                quantity=abs(order_qty)
            )
