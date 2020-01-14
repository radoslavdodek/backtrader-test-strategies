# Backtrader Test Strategies

Test bitcoin trading strategies using Backtrader framework (see https://backtrader.com).

Current implementation contains simple MACD based strategy (see `MACDStrategy.py`).


## Prerequisites

- Python 3.6+: https://www.python.org/downloads/
- Backtrader module: 
    ```
    pip install backtrader
    ```
- Matplotlib module: 
    ```
    pip install matplotlib
    ``` 
    
    Note: On Ubuntu 18 you might need:
    ```
    sudo apt-get install -y python-matplotlib
    sudo apt-get install -y python3-matplotlib
    ```


## How to run

Execute this command:

```
python Main.py 
``` 
 
 
## Folders

### data

- `btc-eur-history.csv`: CSV file which contains BTC to EUR data since 2011-08-27 until 2020-01-13 (on daily basis).

### helpers

- `FetchHistoricalData.py`: Script which fetches historical data and updates `data/btc-eur-history.csv` file. 
   Data are fetched from:

    https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=EUR&allData=true 