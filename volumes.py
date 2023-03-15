import yfinance as yf
import numpy as np
from pandas_datareader import data
import pandas as pd
import pandas_datareader as web
import pandas as pd
import requests
import sys
    

class VolumesAnalysis():
    def __init__():
        pass

    def getVolumeAnalysis():
        pass

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




########################################################
# ########################################################
# import yfinance as yf
# import numpy as np
# from pandas_datareader import data
# import pandas as pd
# import pandas_datareader as web
# import pandas as pd
# import requests
# import sys


# def simpleAvgVolDiff(stockTicker, lengthVolMA, periodVar):

#     stockTic = yf.Ticker(stockTicker)
#     stockTicData = stockTic.history(period = periodVar)
#     stockTicData.drop(['Dividends', 'Stock Splits'], inplace = True, axis = 1)
#     stockTicData[f'{lengthVolMA}-day-MA-V'] = stockTicData[['Volume']].rolling(lengthVolMA, closed = 'left').mean()
#     stockTicData.dropna(inplace = True)
#     volCurrent = stockTicData.iat[-1, -2]
#     volMA = stockTicData.iat[-1, -1]
#     print(round((volCurrent / volMA) * 100, 2), stockTicker)
#     return volCurrent, volMA


# def weightedAvgVolDiff(arrTickers, periodVar, lengthVolMA):

#     marketCapArr = []
#     volCurrentArr = []
#     volMAArr = []
#     for i in arrTickers:
#         marketCap = web.get_quote_yahoo(i)['marketCap']
#         marketCapArr.append(marketCap[0])
#         stockTic = yf.Ticker(i)
#         stockTicData = stockTic.history(period = periodVar)
#         stockTicData.drop(['Dividends', 'Stock Splits'], inplace = True, axis = 1)
#         stockTicData[f'{lengthVolMA}-VMA'] = stockTicData[['Volume']].rolling(lengthVolMA, closed = 'left').mean()
#         stockTicData.dropna(inplace = True)
#         volCurrent = stockTicData.iat[-1, -2]
#         volMA = stockTicData.iat[-1, -1]
#         volCurrentArr.append(volCurrent)
#         volMAArr.append(volMA)

#     summ = 0
#     weightInIndex = 0
#     for i in range(len(marketCapArr)):
#         weightInIndex = (marketCapArr[i] / sum(marketCapArr)) * 100
#         summ += ((volCurrentArr[i] / volMAArr[i]) * 100) * weightInIndex

#     return summ/100


# lengthVolMA = 20
# indexName = int(input('\Select index:\n1. Nifty 50    2. Nifty Bank    3. Both\n> '))
# print()

# if indexName == 1:
#     url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
#     df = pd.read_csv(url)
#     arrTickers = []
#     for i in df['Symbol']:
#         arrTickers.append(f'{i}.NS')
    
#     indexName = 'Nifty 50'
    
# elif indexName == 2:
#     url = 'https://www1.nseindia.com/content/indices/ind_niftybanklist.csv'
#     df = pd.read_csv(url)
#     arrTickers = []
#     for i in df['Symbol']:
#         arrTickers.append(f'{i}.NS')
   
#     indexName = 'Nifty Bank'

# elif indexName == 3:
#     url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
#     df = pd.read_csv(url)
#     arrTickers = []
#     for i in df['Symbol']:
#         arrTickers.append(f'{i}.NS')
#     indexName = 'Nifty 50'

#     arrTemp = []
#     for tickerSymbol in arrTickers:
#         vTempArr = simpleAvgVolDiff(tickerSymbol, lengthVolMA, '21d')
#         arrTemp.append((vTempArr[0] / vTempArr[1]) * 100)
#     print(f'\nSimple Average Method: Volume w.r.t. {lengthVolMA}-day MA Volume (%) - {indexName}: {round((sum(arrTemp)) / len(arrTemp), 2)}%')
#     print(f'Weighted Average Method: Volume w.r.t. {lengthVolMA}-day MA Volume (%) - {indexName}: {round(weightedAvgVolDiff(arrTickers, "1y", lengthVolMA), 2)}%\n')
#     print()
#     print()

#     url = 'https://www1.nseindia.com/content/indices/ind_niftybanklist.csv'
#     df = pd.read_csv(url)
#     arrTickers = []
#     for i in df['Symbol']:
#         arrTickers.append(f'{i}.NS')
#     indexName = 'Nifty Bank'

#     arrTemp = []
#     for tickerSymbol in arrTickers:
#         vTempArr = simpleAvgVolDiff(tickerSymbol, lengthVolMA, '21d')
#         arrTemp.append((vTempArr[0] / vTempArr[1]) * 100)
#     print(f'\nSimple Average Method: Volume w.r.t. {lengthVolMA}-day MA Volume (%) - {indexName}: {round((sum(arrTemp)) / len(arrTemp), 2)}%')
#     print(f'Weighted Average Method: Volume w.r.t. {lengthVolMA}-day MA Volume (%) - {indexName}: {round(weightedAvgVolDiff(arrTickers, "1y", lengthVolMA), 2)}%\n')

#     sys.exit()

# else:
#     print('Error: invalid input')
#     sys.exit()

# arrTemp = []
# for tickerSymbol in arrTickers:
#     vTempArr = simpleAvgVolDiff(tickerSymbol, lengthVolMA, '21d')
#     arrTemp.append((vTempArr[0] / vTempArr[1]) * 100)
# print(f'\nSimple Average Method: Volume w.r.t. {lengthVolMA}-day MA Volume (%) - {indexName}: {round((sum(arrTemp)) / len(arrTemp), 2)}%')
# print(f'Weighted Average Method: Volume w.r.t. {lengthVolMA}-day MA Volume (%) - {indexName}: {round(weightedAvgVolDiff(arrTickers, "1y", lengthVolMA), 2)}%\n')