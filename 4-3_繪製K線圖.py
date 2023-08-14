from historical_data import get_klines_df
import pandas as pd
import mplfinance as mpf

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)
data = klines.copy()

# 繪製K線圖1
mpf.plot(data)
mpf.plot(data, type='candle')
mpf.plot(data, type='candle', style='yahoo')

# 繪製K線圖
mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
mpf.plot(data, style=mstyle, type='candle')

mpf.plot(data, style=mstyle, type='candle', volume=True)
