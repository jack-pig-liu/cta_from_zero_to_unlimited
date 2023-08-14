from backtest_class import Backtest
from talib.abstract import RSI


def run_strategy(self,):
    self.data['position'] = None
    self.data['rsi'] = RSI(self.data, timeperiod=10)
    self.data['rsi_upper'] = self.data.rolling(
        20)['rsi'].mean() + self.data.rolling(20)['rsi'].std()
    self.data['rsi_lower'] = self.data.rolling(
        20)['rsi'].mean() - self.data.rolling(20)['rsi'].std()

    self.data.loc[self.data['rsi'] > self.data['rsi_upper'],
                  'position'] = 1
    self.data.loc[self.data['rsi'] < self.data['rsi_lower'],
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
