import numpy as np 
import pandas as pd
from data import Data
from scan import Scan
from volumes import VolumeAnalysis
import datetime
import math


class Backtest:
    def __init__(self, index, period, interval, entry, exit, notAnIndex = False):
        self.index = index
        self.period = period
        self.interval = interval
        self.entry = entry
        self.exit = exit
        self.notAnIndex = notAnIndex

    
    def _decodeConditions(self):

        # JSON TO DICT (IF REQD.)
        #     # import json
        #     # some JSON:
        #     x =  '{ "name":"John", "age":30, "city":"New York"}'
        #     # parse x:
        #     y = json.loads(x)
        #     # the result is a Python dictionary

        # print(type(self.entry))

        conditions = []
        for cond in self.entry:
            if cond in conditions:
                continue 
            else:
                conditions.append(cond)

        indTemp = None
        for cond in self.exit:
            if cond in conditions:
                continue 
            else:
                conditions.append(cond)
                if indTemp == None:
                    indTemp = conditions.index(cond)

        _entryConds = conditions[:indTemp]
        _exitConds = conditions[indTemp:]

        return _entryConds, _exitConds
    

    def _createConditionFeatures(self, _df, _entryConds, _exitConds, _ticker = None):
        
        for cond in _entryConds:
            if cond == 'MACD':
                _df = self._condMACD(_df, self.entry['MACD']['fastEMALength'], self.entry['MACD']['slowEMALength'], self.entry['MACD']['signalEMALength'])
            elif cond == 'MACross':
                _df = self._condMACross(_df, self.entry['MACross']['fastMALength'], self.entry['MACross']['slowMALength'], self.entry['MACross']['MAType'])
            elif cond == 'BollingerBands':
                _df = self._condBollingerBands(_df, self.entry['BollingerBands']['SMALength'], self.entry['BollingerBands']['multiple'])
            elif cond == 'RSI':
                _df = self._condRSI(_df, self.entry['RSI']['SMALength'])
            elif cond == 'CandlestickPatterns':
                _df = self._condCandlestickPatterns(_df, [i for i in self.entry['CandlestickPatterns'] if self.entry['CandlestickPatterns'][i] != False])
            elif cond == 'SMAVolume':
                _df = self._condSMAVolume(_df, self.entry['SMAVolume']['SMALength'], self.entry['SMAVolume']['indexNature'], self.entry['SMAVolume']['operator'], _ticker)

        for cond in _exitConds:
            if cond == 'MACD':
                _df = self._condMACD(_df, self.exit['MACD']['fastEMALength'], self.exit['MACD']['slowEMALength'], self.exit['MACD']['signalEMALength'])
            elif cond == 'MACross':
                _df = self._condMACross(_df, self.exit['MACross']['fastMALength'], self.exit['MACross']['slowMALength'], self.exit['MACross']['MAType'])
            elif cond == 'BollingerBands':
                _df = self._condBollingerBands(_df, self.exit['BollingerBands']['SMALength'], self.exit['BollingerBands']['multiple'])
            elif cond == 'RSI':
                _df = self._condRSI(_df, self.exit['RSI']['SMALength'])
            elif cond == 'CandlestickPatterns':
                _df = self._condCandlestickPatterns(_df, [i for i in self.exit['CandlestickPatterns'] if self.exit['CandlestickPatterns'][i] != False])
            elif cond == 'SMAVolume':
                _df = self._condSMAVolume(_df, self.exit['SMAVolume']['SMALength'], self.exit['SMAVolume']['indexNature'], _ticker)

        return _df


    def _condMACD(self, _df, _fastEMALength, _slowEMALength, _signalEMALength):
        _df['MACD'] = _df['Close'].ewm(span = _fastEMALength, adjust = False, min_periods = _slowEMALength).mean() - _df['Close'].ewm(span = _slowEMALength, adjust = False, min_periods = _slowEMALength).mean()
        _df['signalMACD'] = _df['MACD'].ewm(span = _signalEMALength, adjust = True, min_periods = _signalEMALength).mean()

        return _df
    

    def _condMACross(self, _df, _fastMALength, _slowMALength, _MAType):
        if _MAType == "simple":
            _df['fastMA'] = _df['Close'].rolling(_fastMALength).mean()
            _df['slowMA'] = _df['Close'].rolling(_slowMALength).mean()

        elif _MAType == "weighted":
            _df['fastMA'] = _df['Close'].ewm(span = _fastMALength, min_periods = _slowMALength).mean()
            _df['slowMA'] = _df['Close'].ewm(span = _slowMALength, min_periods = _slowMALength).mean()

        return _df


    def _condBollingerBands(self, _df, _SMALength, _multiple):
        _df['upperBolBand'] = _df['Close'].rolling(_SMALength).mean() + (_multiple * (_df['Close'].rolling(_SMALength).std(ddof=0)))
        _df['lowerBolBand'] = _df['Close'].rolling(_SMALength).mean() - (_multiple * (_df['Close'].rolling(_SMALength).std(ddof=0)))

        return _df


    def _condRSI(self, _df, _SMALength):
        delta = _df['Close'].diff()
        gain = delta.clip(lower = 0)
        loss = -delta.clip(upper = 0)

        _df['RSI'] = 100 - (100 / (1 + (gain.ewm(com = _SMALength - 1, adjust = False, min_periods = _SMALength).mean() / loss.ewm(com = _SMALength - 1, adjust = False, min_periods = _SMALength).mean())))
        
        return _df

     
    def _condCandlestickPatterns(self, _df, _patterns):
        _df['candlestickPatterns'] = np.nan

        for n, i in enumerate(_df.index):
            if n < 7:
                continue 

            _slicedDF = _df[_df.index <= i].tail(8)

            _scanObj = Scan(_slicedDF)
            _candleObj = _scanObj.getCandleObject()

            _existingPatternsArr = []
            for _pattern in _patterns:
                _patternName = False

                if _pattern == 'Bullish Marubozu':
                    _patternName = _scanObj.ptBullishMarubozu(_candleObj)

                elif _pattern == 'Bearish Marubozu':
                    _patternName = _scanObj.ptBearishMarubozu(_candleObj)
                    
                elif _pattern == 'Spinning Top':
                    _patternName = _scanObj.ptSpinningTop(_candleObj)
                    
                elif _pattern == 'Doji':
                    _patternName = _scanObj.ptDoji(_candleObj)
                    
                elif _pattern == 'Dragonfly Doji':
                    _patternName = _scanObj.ptDragonflyDoji(_candleObj)
                    
                elif _pattern == 'Gravestone Doji':
                    _patternName = _scanObj.ptGravestoneDoji(_candleObj)
                    
                elif _pattern == 'Paper Umbrella':
                    _patternName = _scanObj.ptPaperUmbrella(_candleObj)
                    
                elif _pattern == 'Inverted Paper Umbrella':
                    _patternName = _scanObj.ptInvertedPaperUmbrella(_candleObj)
                    
                elif _pattern == 'Bullish Engulfing':
                    _patternName = _scanObj.ptBullishEngulfing(_candleObj)
                    
                elif _pattern == 'Bearish Engulfing':
                    _patternName = _scanObj.ptBearishEngulfing(_candleObj)
                    
                elif _pattern == 'Piercing':
                    _patternName = _scanObj.ptPiercing(_candleObj)
                    
                elif _pattern == 'Dark Cloud Cover':
                    _patternName = _scanObj.ptDarkCloudCover(_candleObj)
                    
                elif _pattern == 'Bullish Harami':
                    _patternName = _scanObj.ptBullishHarami(_candleObj)
                    
                elif _pattern == 'Bearish Harami':
                    _patternName = _scanObj.ptBearishHarami(_candleObj)
                    
                elif _pattern == 'Morning Star':
                    _patternName = _scanObj.ptMorningStar(_candleObj)
                    
                elif _pattern == 'Evening Star':
                    _patternName = _scanObj.ptEveningStar(_candleObj)

                if _patternName != False:
                    _existingPatternsArr.append(_pattern)

                if len(_existingPatternsArr) > 0:
                    _df['candlestickPatterns'].at[i] = _existingPatternsArr

        return _df
    
    
    def _condSMAVolume(self, _df, _SMALength, _indexNature, _ticker):
        _df['SMAVolume'] = np.nan

        if _ticker[0] != '^':
            _df['SMAVolume'] = round((_df['Volume'] / _df['Volume'].rolling(20).mean()) * 100, 2)

        else: 
            for n, i in enumerate(_df.index):
                if n < (_SMALength - 1):
                    continue 

                _slicedDF = _df[_df.index <= i].tail(_SMALength)

                if _ticker == '^NSEI':
                    _index = 'NIFTY50'
                elif _ticker == '^NSEBANK':
                    _index = 'BANKNIFTY'

                if self.interval == '1d' or self.interval == None:
                    _dates = [i.date() for i in _slicedDF.index]
                    _start = _dates[0]
                    _start = _dates[0] - datetime.timedelta(days = 1)
                    _end = _dates[-1] + datetime.timedelta(days = 1)

                    simple, weighted, _dictCoVolPercentages = VolumeAnalysis(index=_index, smaLength=_SMALength, interval='1d').getVolumeAnalysis(start=_start, end=_end, SMALen=_SMALength)
                    if _indexNature == 'simple':
                        _df['SMAVolume'].loc[i] = simple

                    elif _indexNature == 'weighted':
                        _df['SMAVolume'].loc[i] = weighted

                # else: # YET TO BE HANDLED FOR INTERVALS OTHER THAN '1d'
                    # _dates = [i for i in _slicedDF.index]
                    # _start = _dates[0] - datetime.timedelta(minutes=15)
                    # _end = _dates[-1] + datetime.timedelta(minutes=15)

        return _df


    def _can_buy(self, dataframe):
        dataframe['CAN_BUY'] = np.nan

        for i in dataframe.index:
            satisfied = 0

            for j in self.entry:
                if j == 'CandlestickPatterns':
                    pts = []
                    for pt in self.entry[j]:
                        pts.append(pt)
                    
                    total_patterns = 0
                    for pattern in pts:
                        if type(dataframe['candlestickPatterns'].at[i]) != float:
                            if pattern in dataframe['candlestickPatterns'].at[i]:
                                total_patterns += 1

                    if total_patterns == len(self.entry[j]):
                        satisfied += 1

                elif j == 'MACD':
                    if math.isnan(dataframe['MACD'].at[i]) is False and math.isnan(dataframe['signalMACD'].at[i]) is False:
                        
                        if dataframe['signalMACD'].at[i] < dataframe['MACD'].at[i]:
                            satisfied += 1

                elif j == 'RSI':
                    if math.isnan(dataframe['RSI'].at[i]) is False:
                        if dataframe['RSI'].at[i] <= 25:
                            satisfied += 1

                elif j == 'SMAVolume':
                    if math.isnan(dataframe['SMAVolume'].at[i]) is False:
                        if self.entry[j]['operator'] == '>=':
                            if dataframe['SMAVolume'].at[i] >= self.entry[j]['volPercent']:
                                satisfied += 1

                        elif self.entry[j]['operator'] == '<=':
                            if dataframe['SMAVolume'].at[i] <= self.entry[j]['volPercent']:
                                satisfied += 1

                        ## add other operators as well—<, >, =? 

                elif j == 'MACross':
                    if math.isnan(dataframe['fastMA'].at[i]) is False and math.isnan(dataframe['slowMA'].at[i]) is False:

                        if dataframe['fastMA'].at[i] > dataframe['slowMA'].at[i]:
                            satisfied += 1

                elif j == 'BollingerBands':
                    if math.isnan(dataframe['lowerBolBand'].at[i]) is False:

                        if  dataframe['Close'].at[i] < dataframe['lowerBolBand'].at[i]:
                            satisfied += 1

                ## other conditions
                
            if satisfied == len(self.entry):
                dataframe['CAN_BUY'].at[i] = True
            else:
                dataframe['CAN_BUY'].at[i] = False

        return dataframe
    

    def _can_sell(self, dataframe):
        dataframe['CAN_SELL'] = np.nan

        for i in dataframe.index:
            satisfied = 0

            for j in self.exit:
                if j == 'CandlestickPatterns':
                    pts = []
                    for pt in self.exit[j]:
                        pts.append(pt)
                    
                    total_patterns = 0
                    for pattern in pts:
                        if type(dataframe['candlestickPatterns'].at[i]) != float:
                            if pattern in dataframe['candlestickPatterns'].at[i]:
                                total_patterns += 1

                    if total_patterns == len(self.exit[j]):
                        satisfied += 1

                elif j == 'MACD':
                    if math.isnan(dataframe['MACD'].at[i]) is False and math.isnan(dataframe['signalMACD'].at[i]) is False:
                        
                        if dataframe['signalMACD'].at[i] > dataframe['MACD'].at[i]:
                            satisfied += 1

                elif j == 'RSI':
                    if math.isnan(dataframe['RSI'].at[i]) is False:
                        if dataframe['RSI'].at[i] >= 75:
                            satisfied += 1

                elif j == 'SMAVolume':
                    if math.isnan(dataframe['SMAVolume'].at[i]) is False:
                        if self.exit[j]['operator'] == '>=':
                            if dataframe['SMAVolume'].at[i] >= self.exit[j]['volPercent']:
                                satisfied += 1

                        elif self.exit[j]['operator'] == '<=':
                            if dataframe['SMAVolume'].at[i] <= self.exit[j]['volPercent']:
                                satisfied += 1

                        ## add other operators as well—<, >, =? 

                elif j == 'MACross':
                    if math.isnan(dataframe['fastMA'].at[i]) is False and math.isnan(dataframe['slowMA'].at[i]) is False:

                        if dataframe['fastMA'].at[i] < dataframe['slowMA'].at[i]:
                            satisfied += 1

                elif j == 'BollingerBands':
                    if math.isnan(dataframe['upperBolBand'].at[i]) is False:

                        if  dataframe['Close'].at[i] > dataframe['upperBolBand'].at[i]:
                            satisfied += 1

                ## other conditions
                
            if satisfied == len(self.exit):
                dataframe['CAN_SELL'].at[i] = True
            else:
                dataframe['CAN_SELL'].at[i] = False

        return dataframe


    def _dataframeParser(self, dataframe):
        returns = 0

        position = None 
        buying_price, selling_price = 0, 0
        for i in dataframe.index:
            
            if position == 1:
                if dataframe['CAN_BUY'].at[i] == True:
                    buying_price = dataframe['Close'].at[i]
                    returns += selling_price - buying_price
                    position = 0

            elif position == 0:
                if dataframe['CAN_SELL'].at[i] == True:
                    selling_price = dataframe['Close'].at[i]
                    returns += selling_price - buying_price
                    position = 1

            elif position == None:
                if dataframe['CAN_BUY'].at[i] == True:
                    buying_price = dataframe['Close'].at[i]
                    position = 0
                elif dataframe['CAN_SELL'].at[i] == True:
                    selling_price = dataframe['Close'].at[i]
                    position = 1

        return returns
    

    def getBacktest(self):      
        if self.notAnIndex != True:
            dataObj = Data(symbol = self.index, period = self.period, returnTickers = True, interval = self.interval, periodInStr = True, cleanData = True, noIndexTicker = False)
            
            _dataframe, _tickers = dataObj.getData()
            _entryConds, _exitConds = self._decodeConditions()

            for i in _tickers:
                _openDF = _dataframe[(i, 'Open')]
                _highDF = _dataframe[(i, 'High')]
                _lowDF = _dataframe[(i, 'Low')]
                _closeDF = _dataframe[(i, 'Close')]
                
                if (i[0] != '^'):
                    _volumeDF = _dataframe[(i, 'Volume')]
                    _df = pd.concat([_openDF, _highDF, _lowDF, _closeDF, _volumeDF], axis = 1)
                else:
                    _df = pd.concat([_openDF, _highDF, _lowDF, _closeDF], axis = 1)

                _df = self._createConditionFeatures(_df[i], _entryConds, _exitConds, i)

                break

        else:
            dataObj = Data(symbol = self.index, period = self.period, returnTickers = False, interval = self.interval, periodInStr = True, cleanData = True, noIndexTicker = False)
            _dataframe = dataObj.getData()
            _dataframe.drop(columns = ['Adj Close'], inplace = True)

            if (self.index[-2], self.index[-1]) == ('=', 'X'):
                _dataframe.drop(columns = ['Volume'], inplace = True)
            
            _entryConds, _exitConds = self._decodeConditions()

            _df = self._createConditionFeatures(_dataframe, _entryConds, _exitConds)

        _df = self._can_buy(_df)
        _df = self._can_sell(_df)

        returns = self._dataframeParser(_df)
        average_close_price = _df['Close'].mean()

        return average_close_price, returns 


'''
CONDITIONS: 
- "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9},
- "RSI": {"SMALength": 14},
"CandlestickPatterns": {"patternname": True, "pattern2name": True, "pattern3name": True},
"SMAVolume": {"volPercent": 130, "SMALength": 20, "indexNature": "weighted", "operator": ">="}, ## Operator: [">", "<", "=", ">=", "<="]
- "MACross": {"fastMALength": 9, "slowMALength": 26, "MAType":"simple"},
- "BollingerBands": {"SMALength": 20, "multiple": 2}
#####exit on heiken ashi also???????????
'''

# pd.options.mode.chained_assignment = None

# examples from main.py
# Main.getBacktest('NIFTY50', '5y', None, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, notAnIndex = False)
# Main.getBacktest('USDINR=X', '5y', None, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, {"MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}}, notAnIndex = True)
# Main.getBacktest('BANKNIFTY', '100d', None, {"SMAVolume": {"volPercent": 130, "SMALength": 20, "indexNature": "weighted", "operator": ">="}, "BollingerBands": {"SMALength": 20, "multiple": 2}, "MACD": {"fastEMALength": 12, "slowEMALength": 26, "signalEMALength": 9}, 'CandlestickPatterns': {'Bullish Marubozu': 1, 'Bearish Marubozu': 1, 'Doji': 1}, 'MACross':{'fastMALength': 20, 'slowMALength': 50, "MAType": "simple"}}, {'NEW':9, 'MACD':9, 'OLD':91, 'RSI':{"SMALength":14}, "SMAVolume": {"volPercent": 130, "SMALength": 20, "indexNature": "simple", "operator": ">="}}, notAnIndex = False)


# Currency
### add more currencies GOPINR wtc (from frontend)
### NO VOLUMES FOR CURRENCIES --> add more 
### volumes weighted only for indices

# period in string, 
# interval: string (in [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo])

#  INTERVAL        -------------        PERIOD
#### 1m --------------------------------> 7d
#### 2m, 5m, 15m, 30m, 60m, 90m --------> 60d
#### 1h --------------------------------> 730d (2y: OK)
#### 1h, 1d, 5d, 1wk, 1mo --------------> ALL