import csv, requests
from datetime import datetime

# This script fetches historical data from
# https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=EUR&allData=true
# and converts them into supported CSV format (stores it in "data/btc-eur-history.csv")

SOURCE_DATA_API = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=EUR&allData=true'
TARGET_CSV_FILE_PATH = '../data/btc-eur-history.csv'

data = requests.get(SOURCE_DATA_API).json()
with open(TARGET_CSV_FILE_PATH, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Open", "High", "Low", "Close", "Volume"])
    for p in data['Data']['Data']:
        print('Time: ' + datetime.utcfromtimestamp(p['time']).strftime('%Y-%m-%d') + ': ' + str(p['close']))
        writer.writerow([
            datetime.utcfromtimestamp(p['time']).strftime('%Y-%m-%d'),
            str(p['open']),
            str(p['high']),
            str(p['low']),
            str(p['close']),
            str(p['volumefrom'])
        ])

    print('')
    print(TARGET_CSV_FILE_PATH + ' was updated.')