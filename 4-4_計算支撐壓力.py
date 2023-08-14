from historical_data import get_klines_df
import pandas as pd

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 繪製K線圖
data = klines.copy()
data['floor'] = data.rolling(60)['low'].min().shift(1)
data['ceil'] = data.rolling(60)['high'].max().shift(1)
