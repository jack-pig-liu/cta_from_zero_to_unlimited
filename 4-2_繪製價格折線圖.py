from historical_data import get_klines_df
import pandas as pd

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 繪製價格折線圖
data = klines.copy()
data['close'].plot()
