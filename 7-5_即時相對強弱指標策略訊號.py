from realtime_class import RealTimeKLine
from utils import line_print
from talib.abstract import RSI


def strategy_rsi(data_new):
    data = data_new.copy()
    data['position'] = None
    data['rsi'] = RSI(data, timeperiod=10)
    data['rsi_upper'] = data.rolling(
        20)['rsi'].mean() + data.rolling(20)['rsi'].std()
    data['rsi_lower'] = data.rolling(
        20)['rsi'].mean() - data.rolling(20)['rsi'].std()

    data.loc[data['rsi'] > data['rsi_upper'],
             'position'] = 1
    data.loc[data['rsi'] < data['rsi_lower'],
             'position'] = -1
    data['position'].fillna(method='ffill', inplace=True)
    return data['position'].iloc[-1]


symbol = 'BTCBUSD'.lower()
interval = '5m'
realtime_kline = RealTimeKLine(symbol, interval)

time_format = '%Y/%m/%d %H:%M'
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(time_format)
    position = strategy_rsi(data)
    line_print(
        f"\n{symbol}\n時間:{latest_time}\n收盤價:{latest_close}\nRSI策略當前部位:{position}")
