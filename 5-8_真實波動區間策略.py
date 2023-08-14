from backtest_class import Backtest
from talib.abstract import SMA, ATR


def run_strategy(self,):
    self.data['position'] = None
    self.data['atr_upper'] = SMA(
        self.data, timeperiod=30) + ATR(self.data, timeperiod=30)
    self.data['atr_lower'] = SMA(
        self.data, timeperiod=30) - ATR(self.data, timeperiod=30)
    self.data.loc[self.data['close'] > self.data['atr_upper'],
                  'position'] = 1
    self.data.loc[self.data['close'] < self.data['atr_lower'],
                  'position'] = -1
    self.data['position'].fillna(method='ffill', inplace=True)


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)
backtest.run_strategy()
backtest.performance()
backtest.equity_curve()
backtest.plot_order()
