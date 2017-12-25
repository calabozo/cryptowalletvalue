Simple Python script to retrieve the crypto-currencies balance of addresses
stored in a CSV file, and convert it to fiat currency value. Just for the sake
of keeping track of how much "money" we "have".

```
usage: cryptowalletvalue.py [-h] [--wallets WALLET_FILE] [--log LEVEL]

Simple Python script to retrieve the crypto-currencies balance.

optional arguments:
  -h, --help            show this help message and exit
  --wallets file        Properties file with wallets public addresses. If not
                        given it search for a wallet.properties file.
  --log LEVEL           Set log level. ERROR, WARNING, INFO, DEBUG
```
