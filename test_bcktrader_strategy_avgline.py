from __future__ import (absolute_import, division, unicode_literals,print_function)
import backtrader as bt
import yfinance as yf

#strategy
class MySignal(bt.Indicator):
    lines = ('signal',)
    params = dict(
        short_period = 5,
        median_period = 20,
        long_period = 60
    )

    def __init__(self):
        self.s_ma = bt.ind.SMA(period=self.p.short_period)
        self.m_ma = bt.ind.SMA(period=self.p.median_period)
        self.l_ma = bt.ind.SMA(period=self.p.long_period)

        self.signal1 = bt.And(self.m_ma > self.l_ma, self.s_ma > self.m_ma)

        self.buy_signal = bt.If((self.signal1-self.signal1(-1))>0, 1, 0)

        self.sell_signal = bt.ind.CrossDown(self.s_ma, self.m_ma)

        self.lines.signal = bt.Sum(self.buy_signal, self.sell_signal*(-1))
    
    def next(self):
        pass

#cerebro
if __name__ == '__main__':
    cerebro = bt.Cerebro()

#data feeds
    ticker_list = ['tsla', 'aapl', 'goog', 'amzn', 'amd', 'bac','f']
    st_date = '2020-01-01'
    end_date = '2022-11-30'
    for ticker in ticker_list:
        data_name = yf.download(tickers=ticker, start=st_date, end=end_date, interval="1d")
        data = bt.feeds.PandasData(dataname = data_name)
        cerebro.adddata(data, name=ticker)

cerebro.broker.setcash(1000000.0)
cerebro.broker.setcommission(commission=0.0003)
cerebro.addsizer(bt.sizers.FixedSize, stake = 5)

cerebro.add_signal(bt.SIGNAL_LONG, MySignal)

cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
#add strategy

#cerebro run
cerebro.run()
#plot
cerebro.plot()