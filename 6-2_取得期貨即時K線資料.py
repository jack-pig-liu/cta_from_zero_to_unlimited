import websocket
import json


def on_message(ws, message):
    msg = json.loads(message)
    print(msg)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_error(ws, error):
    print("### error ###")
    print(error)


symbol = 'ETHUSDT'
interval = '12h'
sockname = f'wss://fstream.binance.com/ws/{symbol.lower()}_perpetual@continuousKline_{interval}'

ws = websocket.WebSocketApp(sockname,
                            on_message=on_message,
                            on_close=on_close,
                            on_error=on_error)
ws.run_forever()
