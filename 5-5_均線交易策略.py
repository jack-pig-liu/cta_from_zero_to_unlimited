from backtest_class import Backtest
from talib.abstract import EMA


def run_strategy(self,):
    self.data['position'] = None
    self.data['short_ema'] = EMA(self.data, timeperiod=20)
    self.data['long_ema'] = EMA(self.data, timeperiod=60)

    self.data.loc[self.data['short_ema'] >= self.data['long_ema'],
                  'position'] = 1
    self.data.loc[self.data['short_ema'] < self.data['long_ema'],
                  'position'] = -1


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)
backtest.run_strategy()
backtest.performance()
backtest.equity_curve()
backtest.plot_order()
