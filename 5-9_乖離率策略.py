from backtest_class import Backtest
from talib.abstract import MACD


def run_strategy(self,):
    self.data['position'] = None
    self.data[['macd', 'macdsignal', 'macdhist']] = MACD(self.data,
                                                         fastperiod=20,
                                                         slowperiod=40,
                                                         signalperiod=9)
    self.data.loc[(self.data['macdhist'] > 0) & (self.data['macdsignal'] < 0),
                  'position'] = 1
    self.data.loc[(self.data['macdhist'] < 0) & (self.data['macdsignal'] > 0),
                  'position'] = -1
    self.data['position'].fillna(method='ffill', inplace=True)


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)
backtest.run_strategy()
backtest.performance()
backtest.trade_info.to_csv('a.csv')
backtest.equity_curve()
backtest.plot_order()
