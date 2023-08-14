from backtest_class import Backtest
import pandas as pd
from talib.abstract import MACD
import threading
import time


def run_strategy(self, a1, a2, a3):
    self.data['position'] = None
    self.data[['macd', 'macdsignal', 'macdhist']] = MACD(self.data,
                                                         fastperiod=a1,
                                                         slowperiod=a1+a2,
                                                         signalperiod=a3)
    乖離率大於0 = (self.data['macdhist'] > 0)
    長短價差小於0 = (self.data['macdsignal'] < 0)
    乖離率小於0 = (self.data['macdhist'] < 0)
    長短價差大於0 = (self.data['macdsignal'] > 0)
    最低大於過去最高 = self.data['low'] > self.data['high'].shift(2)  # 1
    最高小於過去最低 = self.data['high'] < self.data['low'].shift(2)  # 1
    多單 = 乖離率大於0 & 長短價差小於0 & 最低大於過去最高
    空單 = 乖離率小於0 & 長短價差大於0 & 最高小於過去最低

    self.data.loc[多單,
                  'position'] = 1
    self.data.loc[空單,
                  'position'] = -1
    self.data['position'].fillna(method='ffill', inplace=True)


def run(Backtest, symbol, interval):
    global pfs
    backtest = Backtest(symbol, interval)
    backtest.data = backtest.data.loc[backtest.data.index.strftime(
        '%Y').isin(['2021', '2022']), ]
    for a1 in range(5, 60, 5):
        for a2 in range(1, 26, 5):
            for a3 in range(1, 16, 3):
                backtest.run_strategy(a1, a2, a3)
                backtest.performance()
                pfs.append([symbol, interval, a1, a2, a3] +
                           backtest.performance())


pfs = []
threads = []
Backtest.run_strategy = run_strategy
st = time.time()

for symbol in ["BTCBUSD", "ETHBUSD", "BNBBUSD", "XRPBUSD"]:
    for interval in ['5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d']:
        threads.append(threading.Thread(
            target=run, args=(Backtest, symbol, interval,)))
        threads[-1].start()

for i in range(len(threads)):
    threads[i].join()

print(time.time() - st)

pfs_df = pd.DataFrame(pfs)
pfs_df.to_csv('log/pf_macd_改良_windows.log')

pfs2 = []
best_pf = pfs_df[pfs_df.groupby([0, 1])[5].transform(max) == pfs_df[5]]
best_pf = best_pf[best_pf[6] > 45]
best_pf = best_pf.sort_values(5, ascending=False)
for index, row in best_pf.iterrows():
    print(row)
    backtest = Backtest(row[0], row[1])
    backtest.run_strategy(row[2], row[3], row[4])
    # backtest.equity_curve([row[0], row[1]])
    pfs2.append([row[0], row[1], row[2], row[3], row[4]] +
                backtest.performance())

best_pf2 = pd.DataFrame(pfs2)
