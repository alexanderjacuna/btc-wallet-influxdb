from urllib.request import urlopen
import json
import blockcypher
from influxdb import InfluxDBClient

def btcConvert(amount):
    data = urlopen("http://api.bitcoincharts.com/v1/weighted_prices.json")
    bitcoin = json.loads(data.read())
    usd = float(bitcoin["USD"]["24h"]) * amount
    return usd

def balance(address):
    total = (blockcypher.get_total_balance(address) / 100000000)
    return total


if __name__ == '__main__':

    # INFLUXDB SETTINGS
    host = "xxx.xxx.xxx.xxx"
    port = 8086
    user = "admin"
    password = "XXXXXXXXXXXXXX"
    dbname = "XXXXXXX"

    # BTC ADDRESSES
    addresses = [
        ["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "wallet_btc", "wallet_usd"]
    ]

    # CREATE CLIENT OBJECT
    client = InfluxDBClient(host, port, user, password, dbname)

    for address in addresses:
        addressTotal = balance(address[0])
        usdValue = round(btcConvert(addressTotal), 2)

        btcData = [
            {
                "measurement": address[1],
                "fields": {
                    "field": addressTotal
                }
            }
        ]

        usdData = [
            {
                "measurement": address[2],
                "fields": {
                    "field": usdValue
                }
            }
        ]

        client.write_points(btcData)
        client.write_points(usdData)
