# https://binance-docs.github.io/apidocs/futures/en/#change-position-mode-trade
# https://python-binance.readthedocs.io/en/latest/binance.html#module-binance.client

from binance.client import Client
from config import binance_key, binance_secret

client = Client(binance_key, binance_secret)


# 取得幣安合約帳戶餘額
client.futures_account_balance()

# 取得當前期貨合約部位
futures_position = client.futures_position_information()
# 單獨取出ETHBUSD的部位
[i for i in futures_position if i['symbol'] == 'ETHBUSD']

# 開槓桿(有部位不能調整)
client.futures_change_leverage(symbol='ETHBUSD', leverage=2)

# 改變倉位模式 ISOLATED or CROSSED
client.futures_change_margin_type(symbol='ETHBUSD', marginType='CROSSED')

# 委託下單
client.futures_create_order(
    symbol="ETHBUSD",
    price=1700,
    timeInForce="GTC",
    type='LIMIT',  # LIMIT or MARKET
    side='BUY',  # BUY or SELL
    quantity=abs(0.01)
)


# 刪單
client.futures_cancel_order(symbol="ETHBUSD", orderId=35083776198)

# 取得委託資訊
client.futures_get_order(symbol="ETHBUSD", orderId=35083776198)
#
client.futures_get_all_orders(symbol="ETHBUSD")
