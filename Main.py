from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths

import backtrader as bt

from AllInSizerWithCommission import AllInSizerWithCommission
from MACDStrategy import MACDStrategy

COMMISSION = 0.002  # 0.2% commission

class MyCSVData(bt.feeds.GenericCSVData):
    params = (
        ('dtformat', '%Y-%m-%d'),
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1),
    )


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(MACDStrategy)
    # cerebro.addstrategy(MA_CrossOver)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    datapath = os.path.abspath('./data/btc-eur-history.csv')

    # Create a Data Feed
    data = MyCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2019, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2020, 1, 13),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(10000.0)

    # Add a the Sizer
    cerebro.addsizer(AllInSizerWithCommission, commission=COMMISSION)

    # Set the commission
    cerebro.broker.setcommission(commission=COMMISSION)

    # Run over everything
    cerebro.run(maxcpus=1)

    # Plot the result
    cerebro.plot()
