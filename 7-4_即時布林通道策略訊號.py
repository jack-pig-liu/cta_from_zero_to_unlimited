from realtime_class import RealTimeKLine
from utils import line_print
from talib.abstract import BBANDS


def strategy_bbands(data_new):
    data = data_new.copy()
    data['position'] = None
    data[['upper', 'middle', 'lower']] = BBANDS(data, timeperiod=20)
    data.loc[data['close'] > data['upper'],
             'position'] = -1
    data.loc[data['close'] < data['lower'],
             'position'] = 1
    data['position'].fillna(method='ffill', inplace=True)
    return data['position'].iloc[-1]


symbol = 'BTCBUSD'.lower()
interval = '5m'
realtime_kline = RealTimeKLine(symbol, interval)

time_format = '%Y/%m/%d %H:%M'
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(time_format)
    position = strategy_bbands(data)
    line_print(
        f"\n{symbol}\n時間:{latest_time}\n收盤價:{latest_close}\n布林通道策略當前部位:{position}")
