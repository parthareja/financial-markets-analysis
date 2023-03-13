import yfinance as yf
import numpy as np
from pandas_datareader import data
import pandas as pd
import pandas_datareader as web
import pandas as pd
import requests
import sys
    



stockTic = yf.Ticker("HDFCBANK.NS")
stockTicData = stockTic.history(period = '21d')
stockTicData.drop(['Dividends', 'Stock Splits'], inplace = True, axis = 1)
stockTicData[f'{20}-day-MA-V'] = stockTicData[['Volume']].rolling(20, closed = 'left').mean()
print(stockTicData)

print('\navg')
print((4222413
+ 5888668
+ 4086058
+ 2868472
+ 5454296
+ 5719356
+ 4031250
+ 4478135
+ 4043353
+ 6194648
+ 5179551
+13941005
+ 8530870
+ 7156486
+ 9496996
+ 7068628
+ 8695907
+ 7493117
+13502355
+10049887)/20)




           