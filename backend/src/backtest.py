from data import Data


class Backtest:
    def __init__(self, index, period, interval):
        self.index = index
        self.period = period
        self.interval = interval


    def _addSMAColumn(dataframe, smaLength):
        dataframe[f'{smaLength}-d SMA (Close)'] = dataframe['Close'].rolling(smaLength).mean()

        return dataframe


    def _getTicker(self):
        if self.index == 'NIFTY50':
            _ticker = '^NSEI'
        if self.index == 'BANKNIFTY':
            _ticker = '^NSEBANK'

        return _ticker
    

    def getBacktest(self):
        _ticker = self._getTicker()
        dataObj =  Data(symbol = _ticker, period = self.period, returnTickers = False, interval = self.interval, periodInStr = True, cleanData = True, noIndexTicker = False)
        dataframe = dataObj.getData()

        print(dataframe)
        pass



## add for currency as well*********

        
# period in string, 
# interval: string (in [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo])

#  INTERVAL        -------------        PERIOD
#### 1m --------------------------------> 7d
#### 2m, 5m, 15m, 30m, 60m, 90m --------> 60d
#### 1h --------------------------------> 730d (2y: OK)
#### 1h, 1d, 5d, 1wk, 1mo --------------> ALL