from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import yfinance as yf
import backtrader as bt
import pandas_datareader as pda

import collections
collections.Iterable = collections.abc.Iterable

import datetime  # For datetime objects

# Import the backtrader platform
import backtrader as bt


# Create a Stratey
class TestStrategy(bt.Strategy):

    params = (
        ('exitbars', 5),
        ('stake', 1),
        ('maperiod', 15),
        ('printlog', False),
        
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
       
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
           

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.sizer.setsizing(self.params.stake)

        self.sma = bt.indicators.MovingAverageSimple(self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
                                            subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                 (order.executed.price,
                 order.executed.value,
                 order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price:  %.2f, Cost: %.2f, Comm: %.2f' %
                 (order.executed.price,
                 order.executed.value,
                 order.executed.comm))
            
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejedcted')
        
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                (trade.pnl, trade.pnlcomm))


            


    def next(self):
         # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                    # current close less than previous close

                    ##if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if self.dataclose[0] < self.sma[0]:
                ##if len(self) >= (self.bar_executed + self.params.exitbars):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()

    

if __name__ == '__main__':

    data = bt.feeds.PandasData(dataname = yf.download(tickers = 'aapl', start='2000-01-01', end='2022-11-30',period="max", interval="1d"))

    cerebro = bt.Cerebro()




    cerebro.adddata(data)
    cerebro.addstrategy(TestStrategy)

    ##data2 = yf.download(tickers='9984.T', start='2022-12-01', end='2022-12-07', period="1mo", interval="1m")
    ##print(data2.head(30))
    ##print('___________________________________________________________________')




    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Add a FixedSize sizer according to the stake
    ##cerebro.addsizer(bt.sizers.FixedSize, stake=20)

    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)


    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run(maxcpus=1)

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()

