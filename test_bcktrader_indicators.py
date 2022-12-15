from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import yfinance as yf
import backtrader.indicators as btind

#strategy vreate
class MyStrategy (bt.Strategy):
    def __init__(self):
        self.sma5 = btind.SMA(period =5)
        self.sma10 = btind.SMA(period = 10)
        self.buy_sig = self.sma5 > self.sma10
        
        print("lineの長さ: ", self.datas[0].buflen())
        

    def next(self):
        print('datetime: ', self.datas[0].datetime.date(0))
        print('close: ',self.datas[0].lines.close[0], self.datas[0].close )
        print('sma5: ', self.sma5[0], self.sma5)
        print('sma10: ', self.sma10[0], self.sma10)
        print('buy_sig: ', self.buy_sig[0], self.buy_sig)
        

        if self.data.close > self.sma5:
            print('-------------------close cross over sma5---------------------')
        if self.datas[0].close[0] > self.sma10:
            print('-------------------close cross over sma10--------------------')
        if self.buy_sig:
            print('--------------------buy buy buy!----------------')

if __name__ == '__main__':

#cerebro
    cerebro = bt.Cerebro()
#datafeeds
    ticker_name = '7203.T'
    st_date = '2022-10-01'
    ed_date = '2022-12-12'
    data_name1 = yf.download(tickers='7203.T', start=st_date, end=ed_date, interval="1d", back_adjust=True)
    data1 = bt.feeds.PandasData(dataname = data_name1)
    data_name2 = yf.download(tickers='^N225', start=st_date, end=ed_date, interval="1d", back_adjust=True)
    data2 = bt.feeds.PandasData(dataname = data_name2)
    cerebro.adddata(data1, name='トヨタ自動車')
    cerebro.adddata(data2, name='NI225')
#set cash

#set sizer

#set commission

#strategy feed
    cerebro.addstrategy(MyStrategy)
#indicator feed

#observer feed

#cerebro run
    cerebro.run()
#cerebro plot
    cerebro.plot(iplot=False,
                numfigs=2,
                style='candel',
                grid=False)