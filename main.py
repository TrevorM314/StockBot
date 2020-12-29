import alpaca_trade_api as tradeapi

alpacaLogin = open("creds.txt", "r")
alpacaKeyID = alpacaLogin.readline()
alpacaKeyID = alpacaKeyID[:-1]
alpacaSecretKey = alpacaLogin.readline()
alpacaSecretKey = alpacaSecretKey[:-1]
alpacaLogin.close()

api = tradeapi.REST(alpacaKeyID, alpacaSecretKey, base_url="https://paper-api.alpaca.markets")
account = api.get_account()

api.submit_order(
    symbol='SPY',
    side='buy',
    type='market',
    qty='1',
    time_in_force='day',
    order_class='bracket',
    take_profit=dict(
        limit_price='500',
    ),
    stop_loss=dict(
        stop_price='295.5',
        limit_price='295.5',
    )
)
print("Success?")