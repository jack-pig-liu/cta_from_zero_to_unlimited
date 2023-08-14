from realtime_class import RealTimeKLine
from utils import line_print

symbol = 'BTCBUSD'.lower()
interval = '5m'
realtime_kline = RealTimeKLine(symbol, interval)


time_format = '%Y/%m/%d %H:%M'
for data in realtime_kline.update_data():
    latest_close = data['close'].iloc[-1]
    latest_time = data.index[-1].strftime(time_format)
    line_print(f"\n{symbol}\n時間:{latest_time}\n收盤價:{latest_close}")
