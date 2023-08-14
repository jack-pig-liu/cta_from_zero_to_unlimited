from realtime_class import RealTimeKLine
from utils import line_print


def strategy_breakout(data_new):
    data = data_new.copy()
    data['position'] = None
    data['ceil'] = data.rolling(20)['high'].max().shift(1)
    data['floor'] = data.rolling(20)['low'].min().shift(1)
    data.loc[data['close'] > data['ceil'], 'position'] = 1
    data.loc[data['close'] < data['floor'], 'position'] = -1
    data['position'].fillna(method='ffill', inplace=True)
    return data['position'].iloc[-1]


symbol = 'BTCBUSD'
interval = '5m'
realtime_kline = RealTimeKLine(symbol, interval)


time_format = '%Y/%m/%d %H:%M'
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(time_format)
    position = strategy_breakout(data)
    line_print(
        f"\n{symbol}\n時間:{latest_time}\n收盤價:{latest_close}\n突破策略當前部位:{position}")
