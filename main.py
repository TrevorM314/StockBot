import alpaca_trade_api as tradeapi

# Read in Alpaca keyID and secret Key from file
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

# Function Definitions
def calculateMovingAverages(symbols, dayCount):
    movingAvgs = {}
    barset = api.get_barset(symbols, "1D", limit=dayCount)
    for symbol in symbols:
        runningTotal = 0
        for barEntry in barset[symbol]:
            close = barEntry.c
            runningTotal += close
        movingAvgs[symbol] = runningTotal / dayCount
    return movingAvgs


def main():
    while(True):
        clock = api.get_clock()
        # Open Market
        marketIsOpen = clock.is_open
        movingAvg5Day = calculateMovingAverages(watchlist, 5)
        boughtToday = []
        while(marketIsOpen):
            account = api.get_account()
            barset = api.get_barset(watchlist, "1Min")

            # Look to Buy
            for symbol in watchlist:
                if (barset[symbol][-1].c > movingAvg5Day[symbol] > barset[symbol][-2].c):
                    budget = account.cash / 5
                    price = barset[-1].c
                    numStocks = int( budget / price )
                    api.submit_order(
                        symbol,
                        side='buy',
                        type='limit',
                        qty=numStocks,
                        time_in_force='day',
                        order_class='simple',
                        limit_price=str(price + .02*price)
                    )
                    boughtToday.append(symbol)

            #Look to Sell
            currentPositions = api.list_positions()
            for position in currentPositions:
                symbol = position.symbol
                if (barset[symbol][-1].c < movingAvg5Day[symbol] < barset[symbol][-2].c):
                    api.submit_order(
                        symbol,
                        side='sell',
                        type='limit',
                        qty=position.qty,
                        time_in_force='day',
                        order_class='simple',
                        limit_price=str(barset[symbol][-2].c)
                    )
        #Use clock here to sleep program until the next market day

main()

"""
api.submit_order(
    'SPY',
    side='buy',
    order_class='simple',
    type='limit',
    qty=2,
    time_in_force='day',
    limit_price='300.1234'
)
"""