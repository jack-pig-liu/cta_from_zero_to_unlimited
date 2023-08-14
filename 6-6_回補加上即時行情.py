from realtime_class import RealTimeKLine

symbol = 'BTCBUSD'
interval = '5m'
realtime_kline = RealTimeKLine(symbol, interval)


for data in realtime_kline.update_data():
    print(data)
