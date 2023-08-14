from backtest_class import Backtest


def run_strategy(self,):
    self.data['position'] = None
    self.data['ceil'] = self.data.rolling(20)['high'].max().shift(1)
    self.data['floor'] = self.data.rolling(20)['low'].min().shift(1)
    self.data.loc[self.data['close'] > self.data['ceil'], 'position'] = 1
    self.data.loc[self.data['close'] < self.data['floor'], 'position'] = -1
    self.data['position'].fillna(method='ffill', inplace=True)


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)
backtest.run_strategy()
backtest.performance(cost=0.001)
backtest.equity_curve()
backtest.plot_order()
