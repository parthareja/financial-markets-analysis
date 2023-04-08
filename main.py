from data import Data
from candle import Candle
from scan import Scan


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

        dataObj = Data(index, period, False, interval)
        df = dataObj.getData()


        # return df
        pass


    def getPrediction():
        pass


    def getBacktest():
        pass

    def getStrategyOptimization():
        pass