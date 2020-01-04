import csv
import json
from datetime import datetime

# This script converts JSON file into supported CSV file
# JSON file can be fetched from https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=EUR&allData=true

SOURCE_JSON_FILE_PATH = 'btc-eur-history.json'
TARGET_CSV_FILE_PATH = 'btc-eur-history.csv'

with open(SOURCE_JSON_FILE_PATH) as json_file:
    data = json.load(json_file)
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
