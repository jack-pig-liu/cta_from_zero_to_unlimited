from realtime_class import RealTimeKLine
from utils import line_print
from talib.abstract import EMA


def strategy_ma(data_new):
    data = data_new.copy()
    data['position'] = None
    data['short_ema'] = EMA(data, timeperiod=20)
    data['long_ema'] = EMA(data, timeperiod=60)

    data.loc[data['short_ema'] >= data['long_ema'],
             'position'] = 1
    data.loc[data['short_ema'] < data['long_ema'],
             'position'] = -1
    return data['position'].iloc[-1]


symbol = 'BTCBUSD'.lower()
interval = '5m'
realtime_kline = RealTimeKLine(symbol, interval)

time_format = '%Y/%m/%d %H:%M'
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(time_format)
    position = strategy_ma(data)
    line_print(
        f"\n{symbol}\n時間:{latest_time}\n收盤價:{latest_close}\n均線策略當前部位:{position}")
