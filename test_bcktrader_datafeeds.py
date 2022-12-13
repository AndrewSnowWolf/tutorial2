from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import yfinance as yf
import pandas_datareader as pda

#Strategy Create
class MyStrategy(bt.Strategy):
    def __init__(self):
        #print datas???
        print("--------------------self.datas--------------------")
        print(self.datas)

        print(self.datas[-2]._name, self.datas[-2])

        print("----------------------self.lines--------------------")
        print(self.lines.getlinealiases())

        print("----------------------self.datas.lines--------------------")
        print(self.datas[0].lines.getlinealiases())

        print("----------------------self.datas.lines.close--------------------")
        print(self.datas[0].lines[6][0])

        self.count = 0
        print("-----------init中のINDEX位置--------------")
        print("0 index: ",'datetime', self.datas[0].lines.datetime.date(0), 'close', self.datas[0].lines.close[0])
        print("-1 index: ",'datetime', self.datas[0].lines.datetime.date(-1), 'close', self.datas[0].lines.close[-1])
        print("1 索引: ",'datetime', self.datas[0].lines.datetime.date(1), 'close', self.datas[0].lines.close[1])
        print("0から3日前までのclose価格: ", self.datas[0].lines.close.get(ago=0, size=3))
        print("-1から5日前までのopen価格: ", self.datas[0].lines.open.get(ago=-1, size=5))
        print("lineの長さ", self.datas[0].buflen())

    def next(self):
        print(f"------------------nextの第{self.count+1}回のLoop---------------------------")
        print("今日: ", 'datetime', self.datas[0].lines.datetime.date(0), 'close ', self.datas[0].lines.close[0])
        print("昨日: ", 'datetime', self.datas[0].lines.datetime.date(-1), 'close ', self.datas[0].lines.close[-1])
        print("明日: ", 'datetime', self.datas[0].lines.datetime.date(1), 'close ', self.datas[0].lines.close[1])
        print("今日から3日前までのclose price: ", self.datas[0].lines.close.get(ago=0, size=3))
        print("処理しましたデータの長さ: ", len(self.datas[0]))
        print("lineの長さ", self.datas[0].buflen())
        self.count += 1

if __name__ == '__main__':
    #cerebro
    cerebro = bt.Cerebro()
    #data feeds
    ##TickersNames = 'aapl goog tsla'
    startdate = '2022-12-01'
    enddate = '2022-12-12'
    ##datanames = yf.download(tickers=TickersNames, start= startdate, end= enddate, interval= '1d', back_adjust=True)
    data1 = bt.feeds.PandasData(dataname = yf.download(tickers='aapl', start= startdate, end= enddate, interval= '1d', back_adjust=True))
    data2 = bt.feeds.PandasData(dataname = yf.download(tickers='tsla', start= startdate, end= enddate, interval= '1d', back_adjust=True))
    cerebro.adddata(data1, name='aapl')
    cerebro.adddata(data2, name='tsla')

    
    #set cash

    #set sizer

    #set commission

    #strategy feed
    cerebro.addstrategy(MyStrategy)
    #analyzer add

    #observer add

    #cerebro run
    cerebro.run()
    #plot

