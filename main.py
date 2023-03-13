from data import Data
from candle import Candle
from scan import Scan




# def main(tickers):
# tickers = ['HDFCBANK.NS', 'TCS.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS']

dataObj = Data('NIFTY50', '1mo')
dataframe, _tickers = dataObj.getData()
# data = data.fetchData()

# data = Data.transformData(data)

objCandle = []
for ticker in _tickers:
    objCandle.append(Candle(dataframe, ticker))
    # objCandle.append(Candle(dataframe[ticker], ticker))


    
print()
print()
print()
print(Scan(objCandle).scan())



# main(tickers)



class Main:
    def __init__():
        pass

    
    def getCandlestickPatternAnalysis():
        dataObj = Data('NIFTY50', '1mo')
        dataframe, _tickers = dataObj.getData()
        objCandle = []
        for ticker in _tickers:
            objCandle.append(Candle(dataframe, ticker))
        Scan(objCandle).scan()

        pass

    def getVolAnalysis():
        pass