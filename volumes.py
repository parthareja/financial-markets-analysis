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


    def _getPercentageWRTSimpleVolAnalysis(self, _dictVolumes, _dictSMAVolumes):
        _indexVol = 0 
        _indexSMAVol = 0

        for value in _dictVolumes.values():
            _indexVol += value

        for valueSMA in _dictSMAVolumes.values():
            _indexSMAVol += valueSMA

        _percentage = (_indexVol / _indexSMAVol) * 100

        return _percentage
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
    

# for viewing in terminal: pls delet when tested OK
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)


obj = VolumeAnalysis("BANKNIFTY", 20)
a = obj.getVolumeAnalysis()
print(a)