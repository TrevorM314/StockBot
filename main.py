import alpaca_trade_api as tradeapi

# Collect Alpaca keyID and secret Key from file
inFile = open("alpacaKey.txt", "r")
alpacaKeyID = inFile.readline().rstrip("\n")
alpacaSecretKey = inFile.readline().rstrip("\n")
inFile.close()

# Connect to Alpaca account
api = tradeapi.REST(alpacaKeyID, alpacaSecretKey, base_url="https://paper-api.alpaca.markets")
account = api.get_account()

watchlist = []
inFile = open("watchlist.txt", "r")
for line in inFile:
    watchlist.append(line.rstrip("\n"))
inFile.close()
