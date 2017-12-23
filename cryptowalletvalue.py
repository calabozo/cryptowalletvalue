#!/usr/bin/python
import requests



def getChangeRate(coins):
    url='https://min-api.cryptocompare.com/data/pricemulti?fsyms=%s&tsyms=EUR'%','.join(coins)
    r = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,BTC,LTC&tsyms=EUR')
    outputDict=dict({})
    if (r.status_code==200):
        val=r.json()
        for coin in coins:
            if val.get(coin)!=None:
                outputDict[coin]=val.get(coin).get("EUR")
    return outputDict

def getNumberOfCoins(wallets):
    #TODO: Get the real value from the wallet
    outputDict = dict({})
    outputDict["BTC"] = 2
    outputDict["ETH"] = 2
    outputDict["LTC"] = 2
    return outputDict

def calcValue(numberOfCoins,changeRate):
    totalValue=0
    for coin in numberOfCoins.keys():
        if (changeRate[coin] is not None):
            coinValue=numberOfCoins[coin] * changeRate[coin]
            totalValue+=coinValue
            print("%f%s at %fEUR/%s : %fEUR"%(numberOfCoins[coin],coin,changeRate[coin],coin,coinValue))
    print("\tTotal: %fEUR"%totalValue)


def main():
    numberOfCoins=getNumberOfCoins(None)
    mycoins=numberOfCoins.keys()
    changeRate=getChangeRate(mycoins)
    calcValue(numberOfCoins,changeRate)

if __name__ == "__main__":
    main()