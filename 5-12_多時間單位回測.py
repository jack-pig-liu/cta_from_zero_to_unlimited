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
pfs = []
for interval in ['5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d']:
    Backtest.run_strategy = run_strategy
    backtest = Backtest(symbol, interval)
    for a1 in range(5, 100):
        for a2 in range(1, 11):
            backtest.run_strategy(a1, a2)
            backtest.performance()
            pfs.append([symbol, interval, a1, a2]+backtest.performance())

pfs_df = pd.DataFrame(pfs)

# 取出各時間週期的最佳參數
best_pf = pfs_df[pfs_df.groupby([1])[4].transform(max) == pfs_df[4]]
