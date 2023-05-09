import yfinance as yf
import pandas as pd
import requests


class Data:
    def __init__(self, symbol, period, returnTickers, interval = None, periodInStr = False, cleanData = False, noIndexTicker = False):
        self.period = period
        self.interval = interval
        self.symbol = symbol
        self.returnTickers = returnTickers
        self.periodInStr = periodInStr
        self.cleanData = cleanData
        self.noIndexTicker = noIndexTicker


    def getData(self):
        indicesArr = ['NIFTY50', 'BANKNIFTY', 'FINNIFTY']
        if self.symbol in indicesArr:
            _tickers = self.getTickers()
        else:
            _tickers = [self.symbol]

        data = self._fetchData(_tickers)
        if self.cleanData == True:
             data = self._cleanData(data)
        data = self._transformData(data)
        
        if self.returnTickers == True:
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


    def getTickers(self):
        if self.symbol == 'NIFTY50':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
            _ownTicker = '^NSEI'
        elif self.symbol == 'BANKNIFTY':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK'
            _ownTicker = '^NSEBANK'
        elif self.symbol == 'FINNIFTY':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FINANCIAL%20SERVICES'
            _ownTicker = 0 # index symbol not added as only 1d data available fetched
        # elif self.index == 'MIDCAPNIFTY': #####???????????????????????????????????????  # add to indicesArr as well
            # _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20MIDCAP%20SELECT'
            # _ownTicker = 0 # yet to be added: index symbol
        else:
            return [self.symbol, self.symbol]

        payload = self._fetchTickersFromNSE(_url)

        _tickers = []
        for i in range(len(payload['data'])):
            _tickers.append(payload['data'][i]['symbol'] + '.NS')

        if _ownTicker != 0:
            _tickers[0] = _ownTicker
        else: 
            _tickers.pop(0)
            return _tickers

        if self.noIndexTicker == True:
            _tickers.pop(0)
      
        return _tickers


    def _fetchData(self, tickersArr):
        if self.periodInStr == True:
            prd = self.period
        else:
            prd = f'{self.period}d'

        if self.interval != None: 
            data = yf.download(tickersArr, period = prd, interval = self.interval, threads = True, group_by = 'ticker', progress = False)
        else:
            data = yf.download(tickersArr, period = prd, threads = True, group_by = 'ticker', progress = False)

        return data


    def _transformData(self, data): 
        # transform as per requirements, the pandas dataframe
        return data
    

    def _cleanData(self, data):
        for i in data:
            if data[i].isnull().sum() > 0:
                data[i].fillna(data[i].rolling(20, min_periods = 1).mean(), inplace = True)

        return data
    

    def getVolumeData(self, _tickers):
        _tickers = self.getTickers()
        _tickers.pop(0)

        if self.interval != None:
            if self.interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d']:#, 5d, 1wk, 1mo, 3mo]:\
                prd = self.period

            elif self.interval == '5d':
                prd = self.period * 5

            elif self.interval == '1wk':
                prd = self.period * 7

            elif self.interval == '1mo':
                prd = self.period * 35

            # volDF = yf.download(_tickers, threads=True, period=f'{prd + 1}d', progress=False, interval=self.interval)
            volDF = yf.download(_tickers, threads=True, period=f'{prd}d', progress=False, interval=self.interval)

        else:
            # volDF = yf.download(_tickers, threads=True, period=f'{self.period + 1}d', progress=False)
            volDF = yf.download(_tickers, threads=True, period=f'{self.period}d', progress=False)
        volDF.drop(['Adj Close', 'Close', 'High', 'Low', 'Open'], inplace = True, axis = 1)

        for i in volDF:
            volDF[(f'{self.period}d-SMA Volume', i[1])] = volDF[[i]].rolling(self.period).mean()    

        return volDF


    def getWeights(self, _tickers):
        _dictFFMC = {}
        _dictWeights = {}

        if self.symbol == 'NIFTY50':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
        elif self.symbol == 'BANKNIFTY':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20BANK'
        elif self.symbol == 'FINNIFTY':
            _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20FINANCIAL%20SERVICES'
        # elif self.index == 'MIDCAPNIFTY': #####??????????????????????????????????????? 
            # _url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%20MIDCAP%20SELECT'
        
        payload = self._fetchTickersFromNSE(_url)

        for i in payload['data']:
            _dictFFMC.update({f'''{i['symbol']}.NS''': i['ffmc']})

        _dictFFMC.pop(next(iter(_dictFFMC)))

        _sumFFMC = 0
        for i in _dictFFMC:
            _sumFFMC += _dictFFMC[i]

        for i in _dictFFMC:
            _dictWeights.update({i: _dictFFMC[i]/_sumFFMC})

        return _dictWeights
    

    def getVolDataForBacktest(self, start, end, tickers, SMALen):
        tickers.pop(0)

        volDF = yf.download(tickers, threads=True, start=start, end=end, progress=False, interval=self.interval)
        volDF.drop(['Adj Close', 'Close', 'High', 'Low', 'Open'], inplace = True, axis = 1)

        for i in volDF:
            volDF[(f'{self.period}d-SMA Volume', i[1])] = volDF[[i]].rolling(self.period).mean()    

        # print('-30950249-050-42d0-50394-')
        # print()
        # \.loc

        return volDF[-SMALen:]
