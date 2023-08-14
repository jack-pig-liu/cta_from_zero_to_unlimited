from historical_data import get_klines_df
import pandas as pd
from talib.abstract import RSI

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 繪製K線圖
data = klines.copy()
data['rsi'] = RSI(data, timeperiod=20)
data['upper'] = 80
data['lower'] = 20

addp = []
addp.append(mpf.make_addplot(data['rsi'], panel=1))
addp.append(mpf.make_addplot(data['upper'], panel=1, color='grey'))
addp.append(mpf.make_addplot(data['lower'], panel=1, color='grey'))

mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
mpf.plot(data, style=mstyle, addplot=addp, type='candle')
