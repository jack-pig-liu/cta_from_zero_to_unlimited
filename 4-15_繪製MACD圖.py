from historical_data import get_klines_df
import pandas as pd
from talib.abstract import MACD

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 繪製K線圖
data = klines.copy()
data[['macd', 'macdsignal', 'macdhist']] = MACD(data,
                                                signalperiod=9)

addp = []
addp.append(mpf.make_addplot(data['macd'], secondary_y=True, panel=1))
addp.append(mpf.make_addplot(data['macdsignal'], secondary_y=True, panel=1))
addp.append(mpf.make_addplot(
    data['macdsignal'], secondary_y=True, panel=1, type='bar'))

mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
mpf.plot(data, style=mstyle, addplot=addp, type='candle')
