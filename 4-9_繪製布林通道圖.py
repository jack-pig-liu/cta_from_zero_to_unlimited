from historical_data import get_klines_df
import pandas as pd
from talib.abstract import BBANDS

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 繪製K線圖
data = klines.copy()
data[['upper', 'middle', 'lower']] = BBANDS(data, timeperiod=20)

addp = []
addp.append(mpf.make_addplot(data['upper'], color='orange'))
addp.append(mpf.make_addplot(data['lower'], color='orange'))

mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
mpf.plot(data, style=mstyle, addplot=addp, type='candle')
