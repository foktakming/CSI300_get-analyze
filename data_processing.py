import pandas as pd
import numpy as np
import pandas_datareader as pdd
import datetime

from sklearn import cluster, covariance


"""
以数字货币为样本，
进行聚类分析前的数据处理
"""
data_crypto = ["BTC", "XRP", "ETH", "BCH", "LTC", "USDT", "BNB", "EOS",
               "LINK", "XMR", "XLM", "ADA", "TRX", "IOT", "DASH", "ETC",
               "NEO", "XRB", "XEM", "ZEC", "DOGE", "BAT", "DCR", "QTUM", "BTG"]

# yahoo上的代码是以“-USD”结尾，
# 例：BTC-USD
symbols_dict = {}
for name in data_crypto:
    symbols_dict[name] = name + "-USD"

quotes = []
# 在线获取数据，并答应哪一个是成功获取
for symbol in symbols_dict.values():
    try:
        data = pdd.DataReader(symbol, "yahoo",
                              datetime.datetime(2018, 1, 1), datetime.datetime(2019, 4, 1))
        quotes.append(data)
        print(f'{symbol} success')
    except:
        print(f'{symbol} failed')

# BTC的数据量
max_num = len(quotes[0])
# 确保所以币种的数据量一致
close_prices = np.vstack([q["Close"] for q in quotes if len(q) == max_num])
open_prices = np.vstack([q["Open"] for q in quotes if len(q) == max_num])
variation = close_prices - open_prices

# 排除总样本中不符合数据量要求的样本
final_list = list(symbols_dict.items())
num = 0
for q in quotes:
    if len(q) != 457:
        del final_list[num]
    num += 1

# 模型训练
edge_model = covariance.GraphLassoCV(cv=5)
X = variation.copy().T
X /= X.std(axis=0)
edge_model.fit(X)
# 确定簇的数量
_, labels = cluster.affinity_propagation(edge_model.covariance_)

"""剩下的部分为打印聚类结果，在sklearn官网上可查看"""