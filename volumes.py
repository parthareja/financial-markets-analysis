import yfinance as yf
# import numpy as np
# from pandas_datareader import data
import pandas as pd
import pandas_datareader as web
# import pandas as pd
import requests
# import sys
from data import Data

    

class VolumeAnalysis:
    def __init__(self, index, smaLength):
        self.index = index
        self.period = smaLength


    # def _fetchTickersFromNSE(self, payload):
    #     headers = {
    #     'Connection': 'keep-alive',
    #     'Cache-Control': 'max-age=0',
    #     'DNT': '1',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    #     'Sec-Fetch-User': '?1',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'Sec-Fetch-Site': 'none',
    #     'Sec-Fetch-Mode': 'navigate',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    #     }
    #     try:
    #         output = requests.get(payload,headers=headers).json()
    #     except ValueError:
    #         s =requests.Session()
    #         output = s.get("http://nseindia.com",headers=headers)
    #         output = s.get(payload,headers=headers).json()
        
    #     return output 


    # def _getTickers(self):
    #     if self.index == 'NIFTY50':
    #         _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
    #     elif self.index == 'BANKNIFTY':
    #         _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK'
    #     elif self.index == 'FINNIFTY':
    #         _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FINANCIAL%20SERVICES'
    #     # elif self.index == 'MIDCAPNIFTY': #####???????????????????????????????????????  
    #         # _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20MIDCAP%20SELECT'

    #     payload = self._fetchTickersFromNSE(_url)

    #     _tickers = []
    #     for i in range(len(payload['data'])):
    #         _tickers.append(payload['data'][i]['symbol'] + '.NS')

    #     _tickers.pop(0)

    #     return _tickers
    

    # def _getVolumes(self, _tickers):
    #     _dictVolumes = {}
    #     _dictSMAVolumes = {}
        
    #     _df = yf.download(_tickers, threads=True, period=f'{self.period}d', progress=False)
    #     _df.drop(['Adj Close', 'Close', 'High', 'Low', 'Open'], inplace = True, axis = 1)

    #     for i in _df:
    #         _df[(f'{self.period}d-SMA Volume', i[1])] = _df[[i]].rolling(self.period).mean()

    #     for i in _df:
    #         if i[0] == 'Volume':
    #             _dictVolumes.update({i[1]: _df[i].iat[-1]})
    #         else:
    #             _dictSMAVolumes.update({i[1]: _df[i].iat[-1]})        
        
    #     return _dictVolumes, _dictSMAVolumes
    

    # def _getWeights(self, _tickers):
    #     _dictWeights = {}

    #     return _dictWeights
    

    def _getPercentageWRTSimpleVolAnalysis(self, _dictVolumes, _dictSMAVolumes):
        _indexVol = 0 
        _indexSMAVol = 0

        for value in _dictVolumes.values():
            _indexVol += value

        for valueSMA in _dictSMAVolumes.values():
            _indexSMAVol += valueSMA

        _percentage = (_indexVol / _indexSMAVol) * 100

        return round(_percentage, 2)


    def _getPercentageWRTWeightedVolAnalysis(self, _dictVolumes, _dictSMAVolumes):
        pass


    def getVolumeAnalysis(self):
        dataObj = Data(self.index, self.period, False, None)
        _tickers = dataObj._getTickers()

        _dictVolumes, _dictSMAVolumes = dataObj._getVolumes(_tickers)
        _dictWeights = dataObj._getWeights(_tickers)

        simple = self._getPercentageWRTSimpleVolAnalysis(_dictVolumes, _dictSMAVolumes)
        weighted = self._getPercentageWRTWeightedVolAnalysis(_dictVolumes, _dictSMAVolumes)

        return simple, weighted
    

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

a = VolumeAnalysis("BANKNIFTY", 4)
b = a.getVolumeAnalysis()
print(b)