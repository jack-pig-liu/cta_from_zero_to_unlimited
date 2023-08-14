from backtest_class import Backtest
import pandas as pd


def run_strategy(self, a1, a2):
    self.data['position'] = None
    self.data['ceil'] = self.data.rolling(a1)['high'].max().shift(a2)
    self.data['floor'] = self.data.rolling(a1)['low'].min().shift(a2)
    self.data.loc[self.data['close'] > self.data['ceil'], 'position'] = 1
    self.data.loc[self.data['close'] < self.data['floor'], 'position'] = -1
    self.data['position'].fillna(method='ffill', inplace=True)


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)

pfs = []
for a1 in range(5, 100):
    for a2 in range(1, 11):
        backtest.run_strategy(a1, a2)
        backtest.performance()
        pfs.append([symbol, interval, a1, a2]+backtest.performance())

pfs_df = pd.DataFrame(pfs)
