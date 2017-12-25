#!/usr/bin/python
import requests
import time

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
    SEPARATOR_CHAR='='
    wallet = {}
    with open(wallet_file, 'r') as f:
        for line in f:
            if line.startswith("#") or line.find(SEPARATOR_CHAR)==-1:
                continue
            currency, address = line.strip().split(SEPARATOR_CHAR)
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
    currenciesBlockCypher = ['BTC','LTC','ETH']
    currenciesBlockDozer  = ['BCH']
    balance_per_currency = {}
    """
    Go through the supported coins and retrieve for each of them the balance
    from the corresponding blockchain explorer.
    """

    for currency in addresses.keys():
        balance = 0
        for address in addresses[currency]:
            if currency in currenciesBlockCypher:
                balance += getBalanceFromBlockCypher(address,currency)
            elif currency in currenciesBlockDozer:
                balance += getBalanceFromBlockDozer(address)
            else:
                print("[WARN] Currency not supported, skipping...")
        balance_per_currency[currency] = balance
    return balance_per_currency


"""
Function to retrieve the balance from one address, using the API
provided by BlockCypher, which currently supports BTC, LTC and ETH.

    https://www.blockcypher.com/dev/bitcoin/?shell#address

For simplicity, and to avoid using different names, I will use `bit` to refer
to the minimum amount for each crypto-currency:
    
    - Satoshi for BTC.
    - "Litoshi" (although this seems not official) for LTC.
    - Wei for ETH.
"""
def getBalanceFromBlockCypher(address,currency):
    url_template = 'https://api.blockcypher.com/v1/{:s}/main/addrs/{:s}'

    """
    The BlockCypher API requires that the URL contains the currency ticker
    symbol in lower case, hence the `.lower()` call.
    """
    url = url_template.format(currency.lower(),address)
    r = requests.get(url)
    """
    Balance of this address in bits.
    """
    balance_bits = r.json()['final_balance']
    """
    For BTC and LTC, each "bit" is 1e-8 parts of the currency.
    """
    if currency in ['BTC','LTC']:
        return 1e-8 * balance_bits
    """
    For ETH, each "bit" is 1e-18 parts of the currency.
    """
    if currency in ['ETH']:
        return 1e-18 * balance_bits


"""
Function to retrieve the balance from one address, using the API
provided by BlockDozer, which currently supports BCH.

    https://blockdozer.com/insight-api/addr/#address/balance
"""
def getBalanceFromBlockDozer(address):
    url_template = 'https://blockdozer.com/insight-api/addr/{:s}/balance'
    url = url_template.format(address)

    for i in range(0,2):
        r = requests.get(url)
        if not isinstance(r.json(), int):
            if r.json()["status"]==429:
                #Time limit exceeded, retrying after a pause
                time.sleep(1)
        else:
            balance_bits=r.json()
            break

    """
    For BCH each "bit" is 1e-8 parts of the currency.
    """
    return 1e-8 * balance_bits


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
    addresses = getWalletAddresses('./wallet.properties')
    numberOfCoins=getNumberOfCoins(addresses)
    mycoins=numberOfCoins.keys()
    changeRate=getChangeRate(mycoins)
    calcValue(numberOfCoins,changeRate)

if __name__ == "__main__":
    main()
