from historical_data import get_klines_df
from binance.client import Client
import pandas as pd
import numpy as np
import mplfinance as mpf

# 取得歷史資料
symbol = "BTCBUSD"
interval = "6h"
klines = get_klines_df(symbol, interval)

# 計算指標 並做回測
data = klines.copy()
data.loc[data["close"] > data['high'].shift(), 'signal'] = -1
data.loc[data["close"] < data['low'].shift(), 'signal'] = 1
data["position"] = data['signal'].fillna(method='ffill')


# 將策略訊號轉換為進出場明細
data["next_open"] = data["open"].shift(-1)
data['time'] = data.index
data['next_time'] = data["time"].shift(-1)
data.loc[(data["position"].shift(1) != 1) & (
    data["position"] == 1), "signal"] = 'buy_order'
data.loc[(data["position"].shift(1) == 1) & (
    data["position"] != 1), "signal"] = 'buy_cover'
order = data[data["signal"] == 'buy_order'][[
    'next_time', "next_open"]].reset_index(drop=True)
order.columns = ["order_time", "order_price"]
cover = data[data["signal"] == 'buy_cover'][[
    'next_time', "next_open"]].reset_index(drop=True)
cover.columns = ["cover_time", "cover_price"]
if order.shape[0] > 0:
    cover = cover[cover["cover_time"] > order["order_time"][0]]
trade_info_buy = pd.concat([order, cover], axis=1)
trade_info_buy.dropna(inplace=True)
trade_info_buy['bs'] = 'buy'
data.loc[(data["position"].shift(1) != -1) & (
    data["position"] == -1), "signal"] = 'sell_order'
data.loc[(data["position"].shift(1) == -1) & (
    data["position"] != -1), "signal"] = 'sell_cover'
order = data[data["signal"] == 'sell_order'][[
    'next_time', "next_open"]].reset_index(drop=True)
order.columns = ["order_time", "order_price"]
cover = data[data["signal"] == 'sell_cover'][[
    'next_time', "next_open"]].reset_index(drop=True)
cover.columns = ["cover_time", "cover_price"]
if order.shape[0] > 0:
    cover = cover[cover["cover_time"] > order["order_time"][0]]
trade_info_sell = pd.concat([order, cover], axis=1)
trade_info_sell.dropna(inplace=True)
trade_info_sell['bs'] = 'sell'

trade_info = pd.concat([trade_info_buy, trade_info_sell])
trade_info.sort_values('order_time', inplace=True)
trade_info.reset_index(drop=True, inplace=True)

# 計算報酬率並扣除成本
trade_info.loc[trade_info['bs'] == 'buy', "return"] = (
    trade_info["cover_price"] / trade_info["order_price"]) - 1
trade_info.loc[trade_info['bs'] == 'sell', "return"] = (
    trade_info["order_price"] / trade_info["cover_price"]) - 1
trade_info["net_return"] = trade_info["return"] - 0.001

# 繪製報酬率曲線圖
trade_info["return"].cumsum().plot(label='原始報酬率(單利)', legend=True)
trade_info["net_return"].cumsum().plot(label='扣除成本後報酬率(單利)', legend=True)

# 計算績效指標
total_ret = trade_info["net_return"].sum()
total_num = trade_info.shape[0]
avg_ret = trade_info["net_return"].mean()
trade_info['hold_time'] = trade_info["cover_time"] - trade_info["order_time"]
winloss_trade_info = trade_info.groupby(np.sign(trade_info["net_return"]))
t1 = winloss_trade_info["net_return"].count()
t2 = winloss_trade_info["net_return"].mean()
t3 = winloss_trade_info["net_return"].sum()
t4 = winloss_trade_info["hold_time"].mean()
if 1 not in t1:
    win_ratio = 0
    win_loss = 0
    odd = 0
    win_hold_time = np.nan
    loss_hold_time = t4.loc[-1]
elif -1 not in t1:
    win_ratio = np.nan
    win_loss = np.nan
    odd = np.nan
    win_hold_time = t4.loc[1]
    loss_hold_time = np.nan
else:
    win_ratio = t1.loc[1] / t1.sum()
    win_loss = t2.loc[1] / abs(t2.loc[-1])
    odd = t3.loc[1] / abs(t3.loc[-1])
    win_hold_time = t4.loc[1]
    loss_hold_time = t4.loc[-1]

expect_value = (win_loss*win_ratio) - (1-win_ratio)
mdd = (
    trade_info["net_return"].cumsum().cummax()
    - trade_info["net_return"].cumsum()
).max()

print(f"總績效(來回成本{0.001}):{round(total_ret,4)}")
print(f"交易次數:{total_num}")
print(f"平均績效(來回成本{0.001}):{round(avg_ret,4)}")
print(f"勝率:{round(win_ratio,4)}")
print(f"賺賠比:{round(win_loss,4)}")
print(f"賠率:{round(odd,4)}")
print(f"期望值:{round(expect_value,4)}")
print(f"獲勝持有時間:{win_hold_time}")
print(f"虧損持有時間:{loss_hold_time}")
print(f"MDD:{round(mdd,4)}")

# 繪製權益曲線圖
trade_info["net_return"].cumsum().plot(label='報酬率曲線(單利)', legend=True)
(trade_info["net_return"].cumsum() -
 trade_info["net_return"].cumsum().cummax()).plot(label='資金回落曲線', legend=True)

# 繪製下單點位圖
buy_trade_info = trade_info[trade_info['bs'] == 'buy']
sell_trade_info = trade_info[trade_info['bs'] == 'sell']
data2 = pd.concat([buy_trade_info.set_index('order_time')['order_price'],
                   buy_trade_info.set_index('cover_time')['cover_price'],
                   sell_trade_info.set_index('order_time')['order_price'],
                   sell_trade_info.set_index('cover_time')['cover_price'],
                   data], axis=1)

data2.columns = ['buy_order_price', 'buy_cover_price',
                 'sell_order_price', 'sell_cover_price'] + list(data2.columns[4:])

addp = []
if data2['buy_order_price'].dropna().shape[0] > 0:
    addp.append(mpf.make_addplot(
        data2['buy_order_price'], type='scatter', marker='^', markersize=100, color='r'))
    addp.append(mpf.make_addplot(
        data2['buy_cover_price'], type='scatter', marker='v', markersize=50, color='b'))

if data2['sell_order_price'].dropna().shape[0] > 0:
    addp.append(mpf.make_addplot(
        data2['sell_order_price'], type='scatter', marker='v', markersize=100, color='g'))
    addp.append(mpf.make_addplot(
        data2['sell_cover_price'], type='scatter', marker='^', markersize=50, color='b'))

mcolor = mpf.make_marketcolors(up='r', down='g', inherit=True)
mstyle = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mcolor)
mpf.plot(data2, style=mstyle, addplot=addp, type='candle')
