import yfinance as yf
import pandas as pd
import requests


class Data:
    def __init__(self, symbol, period, getTickers, interval = None):
        self.period = period
        self.interval = interval
        self.symbol = symbol
        self.getTickers = getTickers


    def getData(self):
        indicesArr = ['NIFTY50', 'BANKNIFTY', 'FINNIFTY']
        if self.symbol in indicesArr:
            _tickers = self._getTickers()
        else:
            _tickers = [self.symbol]

        data = self._fetchData(_tickers)
        data = self._transformData(data)
        
        if self.getTickers == True:
            return data, _tickers
        else: 
            return data
        

    def _fetchTickersFromNSE(self, payload):
        headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        }
        try:
            output = requests.get(payload,headers=headers).json()
        except ValueError:
            s =requests.Session()
            output = s.get("http://nseindia.com",headers=headers)
            output = s.get(payload,headers=headers).json()
        
        return output 


    def _getTickers(self):
        if self.symbol == 'NIFTY50':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
            _ownTicker = '^NSEI'
        elif self.symbol == 'BANKNIFTY':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK'
            _ownTicker = '^NSEBANK'
        elif self.symbol == 'FINNIFTY':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FINANCIAL%20SERVICES'
            _ownTicker = 0 # yet to be added: index symbol
        # elif self.index == 'MIDCAPNIFTY': #####???????????????????????????????????????  # add to indicesArr as well
            # _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20MIDCAP%20SELECT'
            # _ownTicker = 0 # yet to be added: index symbol
        else:
            exit()

        payload = self._fetchTickersFromNSE(_url)

        _tickers = []
        for i in range(len(payload['data'])):
            _tickers.append(payload['data'][i]['symbol'] + '.NS')

        if _ownTicker != 0:
            _tickers[0] = _ownTicker
        else: 
            _tickers.pop(0)

        return _tickers


    def _fetchData(self, tickersArr):
        if self.interval != None: 
            data = yf.download(tickersArr, period = self.period, interval = self.interval, threads = True, group_by = 'ticker', progress = False)
        else:
            data = yf.download(tickersArr, period = self.period, threads = True, group_by = 'ticker', progress = False)

        return data


    def _transformData(self, data): 
        # transform as per requirements, the pandas dataframe
        return data