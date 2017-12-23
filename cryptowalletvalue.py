#!/usr/bin/python
import requests

"""
Get the balance of the addresses contained in a wallet file.

The input should be a CSV file, where each row contains two columns:

    - Ticker symbol for the currency
    - Address for that currency

For Example:

    BTC,1JshKmUXJt8Hqu14HYRP91WzeDqfv7fw42
    BTC,1LEmBwtv1WZ24SPL3Mk3z6hNCSBbRgmiSg

It returns a dictionary where the keys are the ticker symbol for the currency,
and the content of each entry of the dictionary is a list of addresses for that
particula currency. The output for the above example would be:

    {'BTC': ['1JshKmUXJt8Hqu14HYRP91WzeDqfv7fw42', '1LEmBwtv1WZ24SPL3Mk3z6hNCSBbRgmiSg']}

"""
def getWalletAddresses(wallet_file):
    wallet = {}
    with open(wallet_file, 'r') as f:
        for line in f:
            currency, address = line.strip().split(',')
            if currency in wallet:
                wallet[currency].append(address)
            else:
                wallet[currency] = [address]
    return wallet

def getChangeRate(coins):
    url='https://min-api.cryptocompare.com/data/pricemulti?fsyms=%s&tsyms=EUR'%','.join(coins)
    r = requests.get(url)
    outputDict=dict({})
    if (r.status_code==200):
        val=r.json()
        for coin in coins:
            if val.get(coin)!=None:
                outputDict[coin]=val.get(coin).get("EUR")
    return outputDict

"""
Get the balance of the addresses stored in the wallet file.
Limited support as of yet, only:

    BTC,LTC,ETH,BCH
"""
def getNumberOfCoins(addresses):
    supportedCurrencies = ['BTC','LTC','ETH','BCH']
    balance_per_currency = {}
    """
    Go through the supported coins and retrieve for each of them the balance
    from the corresponding blockchain explorer.
    """
    for currency in supportedCurrencies:
        if currency in addresses:
            if currency == 'BTC':
                balance_per_currency['BTC'] = getBalanceBTC(addresses[currency])
            elif currency == 'LTC':
                # TODO
                continue
            elif currency == 'ETH':
                # TODO
                continue
            elif currency == 'BCH':
                # TODO
                continue
            else:
                print("[WARN] Currency not supported, skipping...")

    """
    outputDict["BTC"] = 0.02556957
    outputDict["ETH"] = 0.29592191
    outputDict["LTC"] = 1.10527932
    outputDict["BCH"] = 0.01454478
    """
    return balance_per_currency

"""
Function to retrieve the balance of a series of Bitcoin addresses.

It makes use of the blockchain.info API:

    https://blockchain.info/api/blockchain_api
"""
def getBalanceBTC(addresses):
    template = 'https://blockchain.info/rawaddr/{:s}'
    final_balance_satoshi = 0
    for address in addresses:
        url = template.format(address)
        r = requests.get(url)
        """
        Balance of this address in Satoshis, that is how Blockchain.info returns
        it.
        """
        this_balance = r.json()['final_balance']
        final_balance_satoshi += this_balance
    """
    Return the value in BTC, i.e., `satoshis * 1e-8`
    """
    return 1e-8 * final_balance_satoshi

def calcValue(numberOfCoins,changeRate):
    totalValue=0
    for coin in numberOfCoins.keys():
        if (changeRate[coin] is not None):
            coinValue=numberOfCoins[coin] * changeRate[coin]
            totalValue+=coinValue
            print("{:.8f} {:s} at {:.2f} EUR/{:s} : {:.2f} EUR".format(
                numberOfCoins[coin],
                coin,
                changeRate[coin],
                coin,
                coinValue))
    print("\tTotal: {:.2f} EUR".format(totalValue))

def main():
    addresses = getWalletAddresses('./wallet.csv')
    numberOfCoins=getNumberOfCoins(addresses)
    mycoins=numberOfCoins.keys()
    changeRate=getChangeRate(mycoins)
    calcValue(numberOfCoins,changeRate)

if __name__ == "__main__":
    main()
