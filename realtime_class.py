from historical_data import get_klines_df
from datetime import datetime, timezone
import websocket
import threading
import time
import json
import pandas as pd


class RealTimeKLine():
    def __init__(self, symbol, interval):
        self.wssurl = f'wss://fstream.binance.com/ws/{symbol.lower()}_perpetual@continuousKline_{interval}'
        self.data = get_klines_df(symbol, interval)
        self.ws = None
        self.quote = []
        self.connection_ws()

    def on_message(self, ws, message):
        msg = json.loads(message)
        ckt = msg['k']['t']
        cki = datetime.fromtimestamp(ckt/1000, timezone.utc)

        if cki in self.data.index:
            print('update', cki)
            self.data.loc[self.data.index == cki, ['open',
                                                   'high',
                                                   'low',
                                                   'close',
                                                   'volume',
                                                   'quote_asset_volume',
                                                   'number_of_trades',
                                                   'taker_buy_base_asset_volume',
                                                   'taker_buy_quote_asset_volume',
                                                   ]] = [float(msg['k']['o']),
                                                         float(msg['k']['h']),
                                                         float(msg['k']['l']),
                                                         float(msg['k']['c']),
                                                         float(msg['k']['v']),
                                                         float(msg['k']['q']),
                                                         float(msg['k']['n']),
                                                         float(msg['k']['V']),
                                                         float(msg['k']['Q']), ]
        else:
            print('change', cki)
            self.quote.append(self.data.copy())
            new_row = pd.DataFrame([[float(msg['k']['t']),
                                     float(msg['k']['T']),
                                     float(msg['k']['o']),
                                     float(msg['k']['h']),
                                     float(msg['k']['l']),
                                     float(msg['k']['c']),
                                     float(msg['k']['v']),
                                     float(msg['k']['q']),
                                     float(msg['k']['n']),
                                     float(msg['k']['V']),
                                     float(msg['k']['Q']),
                                     float(msg['k']['B']),
                                     cki]],
                                   columns=['open_time',
                                            'close_time',
                                            'open',
                                            'high',
                                            'low',
                                            'close',
                                            'volume',
                                            'quote_asset_volume',
                                            'number_of_trades',
                                            'taker_buy_base_asset_volume',
                                            'taker_buy_quote_asset_volume',
                                            'ignore',
                                            'time'])
            new_row.set_index('time', inplace=True)
            self.data = pd.concat([self.data, new_row])

    def on_close(self, ):
        print("### closed ###")

    def on_error(self, ws, error):
        print(f"### error ### {error} 嘗試重連")
        time.sleep(2)
        self.connection_ws()

    def connection_ws(self):
        while True:
            self.ws = websocket.WebSocketApp(self.wssurl,
                                             on_message=self.on_message,
                                             on_close=self.on_close,
                                             on_error=self.on_error)
            try:
                t1 = threading.Thread(target=self.ws.run_forever)
                t1.start()
            except Exception as e:
                print(e)
                continue
            break

    # def connection_ws(self):
    #     # websocket.enableTrace(True)
    #     self.ws = websocket.WebSocketApp(self.wssurl,
    #                                      on_message=self.on_message,
    #                                      on_close=self.on_close,
    #                                      on_error=self.on_error)
    #     try:
    #         t1 = threading.Thread(target=self.ws.run_forever)
    #         t1.start()
    #     except Exception as e:
    #         print(e)
    #         self.ws.close()

    def update_data(self):
        while True:
            if self.quote:
                return_data = self.quote.pop(0)
                yield return_data
            else:
                time.sleep(0.02)
