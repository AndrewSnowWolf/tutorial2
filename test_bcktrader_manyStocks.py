from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import yfinance as yf

import backtrader as bt # 引入backtrader框架
import pandas as pd

stk_num = 5  # 回测股票数目
# 创建策略
class SmaCross(bt.Strategy):
    # 可配置策略参数
    params = dict(
        pfast=5,  # 短期均线周期
        pslow=60,   # 长期均线周期
        poneplot = False,  # 是否打印到同一张图
        pstake = 10 # 单笔交易股票数目
    )
    def __init__(self):
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            self.inds[d]['sma1'] = bt.ind.SMA(d.close, period=self.p.pfast)  # 短期均线
            self.inds[d]['sma2'] = bt.ind.SMA(d.close, period=self.p.pslow)  # 长期均线
            self.inds[d]['cross'] = bt.ind.CrossOver(self.inds[d]['sma1'], self.inds[d]['sma2'], plot = False)  # 交叉信号
            # 跳过第一只股票data，第一只股票data作为主图数据
            if i > 0:
                if self.p.poneplot:
                    d.plotinfo.plotmaster = self.datas[0]
    def next(self):
        for i, d in enumerate(self.datas):
            #dt, dn = self.datetime.date(), d._name           # 获取时间及股票代码
            pos = self.getposition(d).size
            if not pos:                                      # 不在场内，则可以买入
                if self.inds[d]['cross'] > 0:                # 如果金叉
                    self.buy(data = d, size = self.p.pstake) # 买买买
            elif self.inds[d]['cross'] < 0:                  # 在场内，且死叉
                self.close(data = d)                         # 卖卖卖

if __name__ == '__main__':
    cerebro = bt.Cerebro()  # 创建cerebro
# 读入股票代码

    ticker_list = ['1346.T']
    st_date = '2010-09-01'
    end_date = '2022-11-30'
    for ticker in ticker_list:
        data_name = yf.download(tickers=ticker, start=st_date, end=end_date, interval="1d")
        data = bt.feeds.PandasData(dataname = data_name)
        cerebro.adddata(data, name=ticker)

# 设置启动资金
cerebro.broker.setcash(10000000.0)
# 设置交易单位大小
#cerebro.addsizer(bt.sizers.FixedSize, stake = 5000)
# 设置佣金为千分之一
cerebro.broker.setcommission(commission=0.001)
cerebro.addstrategy(SmaCross, poneplot = False)  # 添加策略
cerebro.run()  # 遍历所有数据
# 打印最后结果
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot(style = "candlestick")  # 绘图
