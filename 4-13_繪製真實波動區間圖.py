from historical_data import get_klines_df
import pandas as pd
from talib.abstract import SMA, ATR

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 繪製K線圖 
data = klines.copy()
data['atr_short'] = ATR(data, timeperiod=20)
data['atr_long'] = ATR(data, timeperiod=40)
data['atr_upper'] = SMA(data, timeperiod=20) + ATR(data, timeperiod=20)
data['atr_lower'] = SMA(data, timeperiod=20) - ATR(data, timeperiod=20)

addp = []
addp.append(mpf.make_addplot(data['atr_short'], secondary_y=True, panel=1))
addp.append(mpf.make_addplot(data['atr_long'], secondary_y=True, panel=1))
addp.append(mpf.make_addplot(data['atr_upper']))
addp.append(mpf.make_addplot(data['atr_lower']))

mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
mpf.plot(data, style=mstyle, addplot=addp, type='candle')
