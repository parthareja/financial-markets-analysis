from data import Data
from candle import Candle
from scan import Scan
from volumes import VolumeAnalysis
from backtest import Backtest


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


    def getVolAnalysis(index, smaLength, interval):

        return VolumeAnalysis(index, smaLength, interval).getVolumeAnalysis()


    def getBacktest(index, period, interval): # period in string
        
        return Backtest(index, period, interval).getBacktest()


    def getStrategyOptimization():
        pass


Main.getBacktest('NIFTY50', '2y', None)

# period: int (in days)
# interval: string (in [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo])