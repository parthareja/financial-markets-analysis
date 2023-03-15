import yfinance as yf
import pandas as pd


class Data:
    def __init__(self, index, period, interval = None):
        self.period = period
        self.interval = interval
        self.index = index


    def _getTickers(self):
        if self.index == 'NIFTY50':
            _url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
        elif self.index == 'BANKNIFTY':
            _url = 'https://www1.nseindia.com/content/indices/ind_niftybanklist.csv'
        elif self.index == 'FINNIFTY':
            _url = 'https://www1.nseindia.com/content/indices/ind_niftyfinancelist.csv'
        # elif self.index == 'MIDCAPNIFTY': #####???????????????????????????????????????
            # _url = 'https://www1.nseindia.com/content/indices/ind_niftymidcapselect_list.csv'
        else:
            exit()
        _df = pd.read_csv(_url)
        _tickers = []
        for symbol in _df['Symbol']:
            _tickers.append(f'{symbol}.NS')

        return _tickers


    def _fetchData(self):
        _tickers = self._getTickers()

        if self.interval != None: 
            data = yf.download(_tickers, period = self.period, interval = self.interval, threads = True, group_by = 'ticker', progress = False)
        else:
            data = yf.download(_tickers, period = self.period, threads = True, group_by = 'ticker', progress = False)

        return data, _tickers


    def getData(self): 
        # transform as per requirements, the pandas dataframe
        data, _tickers = self._fetchData()
        
        return data, _tickers
    

 