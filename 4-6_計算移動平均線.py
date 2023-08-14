from historical_data import get_klines_df
import pandas as pd
from talib.abstract import SMA, EMA, WMA, KAMA

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 計算技術指標
data = klines.copy()
data['sma'] = SMA(data, timeperiod=20)
data['ema'] = EMA(data, timeperiod=20)
data['wma'] = WMA(data, timeperiod=20)
data['kama'] = KAMA(data, timeperiod=20)
