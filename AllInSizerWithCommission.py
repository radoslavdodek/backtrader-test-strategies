from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

__all__ = ['AllInSizerWithCommission']


class AllInSizerWithCommission(bt.Sizer):
    '''This sizer tries to use all available cash (also counts with the commission)

    Params:
      - ``commission`` (default: ``0.002``)
    '''

    params = (
        ('commission', 0.002),  # 0.2%
        ('retint', False),  # return an int size or rather the float value
    )

    def __init__(self):
        pass

    def _getsizing(self, comminfo, cash, data, isbuy):
        position = self.broker.getposition(data)
        if not position:
            # Here we use (cash - 1) just to avoid rounding issues:
            size = (cash - 1) / ((1 + self.params.commission) * data.close[0])
        else:
            size = position.size

        if self.p.retint:
            size = int(size)

        self.log('Number of coins to buy/sell: %.9f' % size)
        return size

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        print('%s' % (txt))
