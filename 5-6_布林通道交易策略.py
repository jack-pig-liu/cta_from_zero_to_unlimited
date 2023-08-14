from backtest_class import Backtest
from talib.abstract import BBANDS


def run_strategy(self,):
    self.data['position'] = None
    self.data[['upper', 'middle', 'lower']] = BBANDS(self.data, timeperiod=20)
    self.data.loc[self.data['close'] > self.data['upper'],
                  'position'] = -1
    self.data.loc[self.data['close'] < self.data['lower'],
                  'position'] = 1
    self.data['position'].fillna(method='ffill', inplace=True)


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)
backtest.run_strategy()
backtest.performance()
backtest.equity_curve()
backtest.plot_order()
