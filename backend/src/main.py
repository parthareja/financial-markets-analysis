from data import Data
from scan import Scan
from volumes import VolumeAnalysis
from backtest import Backtest


class Main:
    def __init__():
        pass

    
    def getScanAnalysis(index, period, interval):
        dataObj = Data(index, period, True, interval)
        dataframe, _tickers = dataObj.getData()

        ptDict = {}
        for i in _tickers:
            scanObj = Scan(dataframe[i])

            _ptArr = scanObj.getScanAnalysis()

            for j in _ptArr: 
                if j not in ptDict:
                    ptDict[j] = [i]

                else:
                    ptDict[j].append(i)

        return ptDict


    def getVolAnalysis(index, smaLength, interval):

        return VolumeAnalysis(index, smaLength, interval).getVolumeAnalysis()


    def getBacktest(index, period, interval, entry, exit, notAnIndex): # period in string
        
        return Backtest(index, period, interval, entry, exit, notAnIndex).getBacktest()


# Main.getBacktest('NIFTY50', '5y', None, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, notAnIndex = False)
# Main.getBacktest('USDINR=X', '5y', None, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, notAnIndex = True)
# Main.getBacktest('BANKNIFTY', '100d', None, {"SMAVolume": {"volPercent": 130, "SMALength": 20, "indexNature": "weighted", "operator": ">="}, "BollingerBands": {"SMALength": 20, "multiple": 2}, "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}, 'CandlestickPatterns': {'Bullish Marubozu': 1, 'Bearish Marubozu': 1, 'Doji': 1}, 'MACross':{'fastMALength': 20, 'slowMALength': 50, "MAType": "simple"}}, {'NEW':9, 'MACD':9, 'OLD':91, 'RSI':{"SMALength":14}, "SMAVolume": {"volPercent": 130, "SMALength": 20, "indexNature": "simple", "operator": ">="}}, notAnIndex = False)


# print(f"\nNIFTY50: {Main.getVolAnalysis('NIFTY50', 20, None)}")
# print(f"\nBANKNIFTY: {Main.getVolAnalysis('BANKNIFTY', 20, None)}")

# for volumes.py
# print(VolumeAnalysis('BANKNIFTY', 20).getVolumeAnalysis())
# print(VolumeAnalysis('NIFTY50', 20).getVolumeAnalysis())


# print(Main.getScanAnalysis('NIFTY50', 8, None))

# Main.getBacktest('NIFTY50', '2y', None, {"BollingerBands": {"SMALength": 20, "multiple": 2}, "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}, 'Patterns': ['Marubozu', 'Pattern 2'], 'MACross':{'fastSMALength': 9, 'slowSMALength': 50}}, {'NEW':9, 'MACD':9, 'OLD':91, 'RSI':{"SMALength":14}}, notAnIndex = False)
# Main.getBacktest('BANKNIFTY', '2y', None, {'MACD': 20, 'Patterns': ['Marubozu', 'Pattern 2'], 'MA-Cross':{'fastMoving': 50, 'slowMoving': 9}}, {'MACD': 2}, notAnIndex = False)


# Main.getBacktest('BANKNIFTY', '5y', None, {"BollingerBands": {"SMALength": 20, "multiple": 2}, "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}, 'CandlestickPatterns': {'Marubozu':1, 'someaotherpattern':1, 'NAI':0}, 'MACross':{'fastMALength': 20, 'slowMALength': 50, "MAType": "simple"}}, {'NEW':9, 'MACD':9, 'OLD':91, 'RSI':{"SMALength":14}, "SMAVolume": {"SMALength": 20, "IndexNature": "weighted", "Operator": ">="}}, notAnIndex = False)
# Main.getBacktest('BANKNIFTY', '30d', '1d', {"BollingerBands": {"SMALength": 20, "multiple": 2}, "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}, 'CandlestickPatterns': {'Marubozu':1, 'someaotherpattern':1, 'NAI':0}, 'MACross':{'fastMALength': 20, 'slowMALength': 50, "MAType": "simple"}}, {'NEW':9, 'MACD':9, 'OLD':91, 'RSI':{"SMALength":14}, "SMAVolume": {"SMALength": 20, "indexNature": "simple", "operator": ">="}}, notAnIndex = False)
# Main.getBacktest('HDFCBANK.NS', 'max', None, {"BollingerBands": {"SMALength": 20, "multiple": 2}, "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}, 'CandlestickPatterns': {'Marubozu':1, 'someaotherpattern':1, 'NAI':0}, 'MACross':{'fastMALength': 20, 'slowMALength': 50, "MAType": "simple"}}, {'NEW':9, 'MACD':9, 'OLD':91, 'RSI':{"SMALength":14}, "SMAVolume": {"SMALength": 20, "IndexNature": "weighted", "Operator": ">="}}, notAnIndex = True)


# Main.getBacktest('USDINR=X', '2y', None, {'MACD': 20, 'Patterns': ['Marubozu', 'Pattern 2'], 'MA Cross':{'fastMoving': 50, 'slowMoving': 9}}, {}, notAnIndex = True)

# period: int (in days)
# interval: string (in [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo])