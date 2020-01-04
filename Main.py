from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths

import backtrader as bt
from backtrader.indicators import MovAv

from AllInSizerWithCommission import AllInSizerWithCommission

COMMISSION = 0.002  # 0.2% commission


class MACD2(bt.indicators.MACDHisto):
    ''' MACD2 uses Simple moving average instead of Exponential one '''
    params = (('period_me1', 12), ('period_me2', 26), ('period_signal', 9),
              ('movav', MovAv.Simple),)


class MACDStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" and "volume" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume

        # Indicators
        self.macd = MACD2()

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.steps_after_up_cross = 0
        self.last_macd_histo = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        macd_macd = self.macd.lines.macd[0]
        macd_signal = self.macd.lines.signal[0]
        self.log('MACD       , %.2f' % macd_macd)
        self.log('MACD-SIGNAL, %.2f' % macd_signal)

        min_diff = 0
        macd_going_up = False
        macd_going_down = False

        if self.last_macd_histo is not None:
            # grow_rate = (macd_macd - self.macd_last_macd) - (macd_signal - self.macd_last_signal)
            grow_rate = self.macd.lines.histo[0] - self.last_macd_histo
            histo = self.macd.lines.histo[0]

            self.log('Grow Rate,  %s' % grow_rate)

            if (histo > 0) and (grow_rate > 20):
                macd_going_up = True
                macd_going_down = False
                self.steps_after_up_cross = self.steps_after_up_cross + 1
            elif histo < 1:
                macd_going_up = False
                macd_going_down = True
                self.steps_after_up_cross = 0

        self.macd_last_macd = macd_macd
        self.macd_last_signal = macd_signal
        self.last_macd_histo = self.macd.lines.histo[0]

        if macd_going_up:
            self.log('steps_after_up_cross, %s' % self.steps_after_up_cross)
            self.log('GOING UP, grow rate: %s' % grow_rate)
        if macd_going_down:
            self.log('GOING DOWN, grow rate: %s' % grow_rate)

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if macd_going_up and self.steps_after_up_cross > 0:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % (self.dataclose[0]))

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if macd_going_down:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


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
        # Do not pass values before this date
        todate=datetime.datetime(2019, 12, 31),
        # Do not pass values after this date
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
