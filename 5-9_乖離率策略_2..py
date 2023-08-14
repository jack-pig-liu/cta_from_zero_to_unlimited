from backtest_class import Backtest
from talib.abstract import MACD


def run_strategy(self,):
    self.data['position'] = None
    self.data[['macd', 'macdsignal', 'macdhist']] = MACD(self.data,
                                                         fastperiod=15,
                                                         slowperiod=26,
                                                         signalperiod=7)
    乖離率大於0 = (self.data['macdhist'] > 0)
    長短價差小於0 = (self.data['macdsignal'] < 0)
    乖離率小於0 = (self.data['macdhist'] < 0)
    長短價差大於0 = (self.data['macdsignal'] > 0)
    # 乖離率大於0連續 = 乖離率大於0.rolling(2).sum() == 2
    # 乖離率小於0連續 = 乖離率小於0.rolling(2).sum() == 2
    # 長短價差小於0連續 = 長短價差小於0.rolling(2).sum() == 2
    # 長短價差大於0連續 = 長短價差大於0.rolling(2).sum() == 2
    # 最低小最高平均 = self.data['low'] < self.data['high'].rolling(8).mean().shift(2) # 2
    # 最高大最低平均 = self.data['high'] > self.data['low'].rolling(8).mean().shift(2) # 2

    # 最低大最高平均 = self.data['low'] > self.data['high'].rolling(4).mean().shift(2) # 2
    # 最高小最低平均 = self.data['high'] < self.data['low'].rolling(4).mean().shift(2) # 2

    最低大於過去最高 = self.data['low'] > self.data['high'].shift(2)  # 1
    最高小於過去最低 = self.data['high'] < self.data['low'].shift(2)  # 1

    # 最低大於過去最高連續 = 最低大於過去最高.rolling(2).sum()==2
    # 最高小於過去最低連續 = 最高小於過去最低.rolling(2).sum()==2

    # 收盤大於過去最高 = self.data['close'] > self.data['high'].shift(1)  # 1
    # 收盤小於過去最低 = self.data['close'] < self.data['low'].shift(1)  # 1

    多單 = 乖離率大於0 & 長短價差小於0 & 最低大於過去最高
    空單 = 乖離率小於0 & 長短價差大於0 & 最高小於過去最低

    self.data.loc[多單,
                  'position'] = 1
    self.data.loc[空單,
                  'position'] = -1
    self.data['position'].fillna(method='ffill', inplace=True)


symbol = "BTCBUSD"
interval = "8h"
Backtest.run_strategy = run_strategy
backtest = Backtest(symbol, interval)
backtest.run_strategy()
backtest.performance()
backtest.equity_curve('原始')
backtest.plot_order()
# backtest.trade_info.to_csv('a.csv')
