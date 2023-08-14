from backtest_class import Backtest


def run_strategy(self,):    # 定義回測函數
    self.data['position'] = None
    self.data.loc[self.data["close"] >
                  self.data['high'].shift(), 'signal'] = -1
    self.data.loc[self.data["close"] <
                  self.data['low'].shift(), 'signal'] = 1
    # 最重要的是 position陣列 後續的函數會抓取該陣列去進行交易明細的取得
    self.data["position"] = self.data['signal'].fillna(method='ffill')


symbol = "BTCBUSD"
interval = "6h"
Backtest.run_strategy = run_strategy  # 將回測函數定義為class函數
backtest = Backtest(symbol, interval)  # 實例化並取得回測資料
backtest.run_strategy()  # 開始回測
backtest.performance()  # 績效指標運算
backtest.equity_curve()  # 繪製權益區線
backtest.plot_order()   # 繪製下單點位
