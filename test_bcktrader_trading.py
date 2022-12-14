##多因子选股策略
from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import yfinance as yf




#strategy create
class StockSelectStrategy(bt.Strategy):
    params = dict(
        selnum = 30, #selected stocks nums
        rperiod = 1, #return period
        vperiod = 6, #volatility period
        mperiod = 2, #momentum period
        reserver = 0.05, #reserver percent
    )
    def __init__(self):
        #holding percent per stocks
        self.perctarget = (1.0 - self.p.reserver) / self.p.selnum
        #cal volatility of return
        self.rs = {d:bt.ind.PercentChange(d, period=self.p.rperiod) for d in self.datas}
        self.vs = {d:1/(bt.ind.StdDev(ret, period=self.p.vperiod)+0.000001) for d,ret in self.rs.items()}

        #cal momentum
        self.ms = {d:bt.ind.ROC(d, period= self.p.mperiod) for d in self.datas}



        self.all_factors = [self.rs, self.vs, self.ms]


    def next(self):
        stocks = list(self.datas)
        ranks = {d:0 for d in stocks}
        # cal factor's ranks and then sum it
        for factor in self.all_factors:
            stocks.sort(key=lambda x: factor[x][0], reverse=True)

            ranks = {d:i+ranks[d] for d, i in zip(stocks, range(1,len(stocks)+1))}

        ranks = sorted(ranks.items(), key=lambda x:x[1], reverse=False)


if __name__ =='__main__':
#data feeds
    cerebro = bt.Cerebro()

    st_date = '2022-01-01'
    end_date = '2022-11-30'
    ticker_list = ['aapl', 'goog', 'amzn']


    for ticker in ticker_list:
        data_name = yf.download(tickers=ticker, start=st_date, end=end_date, interval="1d", back_adjust=True)
        data = bt.feeds.PandasData(dataname=data_name)
        cerebro.adddata(data, name=ticker)
    

#data feeds
    #cerebro.adddata(data, name='Tesla')

#set cash
    cerebro.broker.setcash(10000000.0)
#set sizer
    cerebro.addsizer(bt.sizers.FixedSize, stake=20)
#set commission
    cerebro.broker.setcommission(commission = 0.0003)
#add indictor
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl')
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name= 'AnnualReturn')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='SharpeRatio')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='DrawDown')
#add observer

#strategy feeds
    cerebro.addstrategy(StockSelectStrategy)

#cerebro run
    cerebro.run()
#plot
    cerebro.plot(numfigs=3)