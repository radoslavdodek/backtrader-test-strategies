# backtrader-test-strategies

Test bitcoin trading strategies using Backtrader framework.

Current implementation contains simple MACD based strategy (see `Main.py`: `MACDStrategy` class).

## Prerequisites

- Python 3.6+: https://www.python.org/downloads/
- Backtrader module: 
    ```
    pip install backtrader
    ```
  
## Folders

### data

- `btc-eur-history.csv`: CSV file which contains BTC to EUR data since 2011-08-27 until 2020-01-03 (on daily basis).

### helpers

- `ConvertJson2Csv.py`: Script which converts JSON file into supported CSV file. The JSON file can be fetched from: 

    https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=EUR&allData=true 