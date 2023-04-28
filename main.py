from data import Data
from candle import Candle
from scan import Scan
from volumes import VolumeAnalysis


class Main:
    def __init__():
        pass

    
    def getScanAnalysis(index, period, interval):

        dataObj = Data(index, period, True, interval)
        dataframe, _tickers = dataObj.getData()
        
        objCandle = []
        for ticker in _tickers:
            objCandle.append(Candle(dataframe, ticker))
        
        return Scan(objCandle).scan()


    def getVolAnalysis(index, period, interval):

        return VolumeAnalysis(index, period, interval).getVolumeAnalysis()


    def getBacktest():
        pass


    def getStrategyOptimization():
        pass


# period: int (in days)
# interval: string (in [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo])