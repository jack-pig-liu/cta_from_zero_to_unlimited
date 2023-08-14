import websocket
import json
import time

symbol = 'ethusdt'
sockname = f'wss://fstream.binance.com/ws/{symbol}_perpetual@continuousKline_12h'


def on_message(ws, message):
    msg = json.loads(message)
    print(msg)


def on_close(ws):
    print("### closed ###")


def on_error(ws, error):
    print("### error ###")
    print(error)
    print("正在嘗試重連")
    time.sleep(5)
    connection_tmp()


def connection_tmp():
    while True:
        ws = websocket.WebSocketApp(sockname,
                                    on_message=on_message,
                                    on_close=on_close,
                                    on_error=on_error)
        try:
            ws.run_forever()
        except Exception as e:
            print(e)
            ws.close()
            continue
        break


connection_tmp()

# {
#   "e":"continuous_kline",   // Event type
#   "E":1607443058651,        // Event time
#   "ps":"BTCUSDT",           // Pair
#   "ct":"PERPETUAL"          // Contract type
#   "k":{
#     "t":1607443020000,      // Kline start time
#     "T":1607443079999,      // Kline close time
#     "i":"1m",               // Interval
#     "f":116467658886,       // First trade ID
#     "L":116468012423,       // Last trade ID
#     "o":"18787.00",         // Open price
#     "c":"18804.04",         // Close price
#     "h":"18804.04",         // High price
#     "l":"18786.54",         // Low price
#     "v":"197.664",          // volume
#     "n": 543,               // Number of trades
#     "x":false,              // Is this kline closed?
#     "q":"3715253.19494",    // Quote asset volume
#     "V":"184.769",          // Taker buy volume
#     "Q":"3472925.84746",    //Taker buy quote asset volume
#     "B":"0"                 // Ignore
#   }
# }
