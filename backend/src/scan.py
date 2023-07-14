from candle import Candle

class Scan:
    def __init__(self, df):
        self.df = df


    def ptBullishMarubozu(self, candle, tolerance = 0.07):
        '''
        Bullish irrespective of ongoing trend
        '''
        patternName = False

        if candle.colour(0) == 'GREEN': 
            _body = abs(candle.open(0) - candle.close(0))
            _range = candle.high(0) - candle.low(0)

            if _range > max(abs(candle.high(-1) - candle.low(-1)), abs(candle.high(-2) - candle.low(-2)), abs(candle.high(-3) - candle.low(-3)), abs(candle.high(-4) - candle.low(-4)), abs(candle.high(-5) - candle.low(-5))):
                _wick = candle.high(0) - candle.close(0)
                _shadow = candle.open(0) - candle.low(0)

                if _wick / _body <= tolerance and _shadow / _body <= tolerance:
                    patternName = 'Bullish Marubozu'
        
        return patternName


    def ptBearishMarubozu(self, candle, tolerance = 0.07):
        '''
        Bearish irrespective of ongoing trend
        '''
        patternName = False

        if candle.colour(0) == 'RED': 
            _body = abs(candle.open(0) - candle.close(0))
            _range = candle.high(0) - candle.low(0)

            if _range > max(abs(candle.high(-1) - candle.low(-1)), abs(candle.high(-2) - candle.low(-2)), abs(candle.high(-3) - candle.low(-3)), abs(candle.high(-4) - candle.low(-4)), abs(candle.high(-5) - candle.low(-5))):
                _wick = candle.high(0) - candle.open(0)
                _shadow = candle.close(0) - candle.low(0)

                if _wick / _body <= tolerance and _shadow / _body <= tolerance:
                    patternName = 'Bearish Marubozu'
        
        return patternName
    

    def ptSpinningTop(self, candle):
        '''
        Signals indecision
        '''
        patternName = False
        
        # _body = abs(candle.open(0) - candle.close(0))
        # _range = candle.high(0) - candle.low(0)

        # # if _body <= _range * 0.5

        # if candle.colour(0) == 'RED': 
        #     if abs(((candle.high(0) - candle.open(0)) / _body) - ((candle.close(0) - candle.low(0)) / _body)) <= tolerance:
        #         # wick ~ shadow
        #         # body: small????????????????????
        #         patternName = 'Spinning Top'

        # elif candle.colour(0) == 'GREEN':
        #     if abs(((candle.high(0) - candle.close(0)) / _body) - ((candle.open(0) - candle.low(0)) / _body)) <= tolerance:
        #         # wick ~ shadow
        #         # body: small????????????????????
        #         patternName = 'Spinning Top'

        return patternName
    

    def ptDoji(self, candle):
        '''
        Signals indecision
        '''
        patternName = False

        _body = abs(candle.open(0) - candle.close(0))
        _range = candle.high(0) - candle.low(0)

        if _body / _range <= 0.1:
            _bodyMidPoint = (candle.open(0) + candle.close(0)) / 2

            if _bodyMidPoint > candle.low(0) + _range * 0.25 and _bodyMidPoint < candle.low(0) + _range * 0.75: 
                patternName = 'Doji'

        return patternName


    def ptDragonflyDoji(self, candle):
        '''
        Signals indecision with a slightly bullish bias
        '''
        patternName = False

        _body = abs(candle.open(0) - candle.close(0))
        _range = candle.high(0) - candle.low(0)

        if _body / _range <= 0.1:
            _bodyMidPoint = (candle.open(0) + candle.close(0)) / 2

            if _bodyMidPoint >= candle.low(0) + _range * 0.75:
                patternName = 'Dragonfly Doji'

        return patternName


    def ptGravestoneDoji(self, candle):
        '''
        Signals indecision with a slightly bearish bias
        '''
        patternName = False

        _body = abs(candle.open(0) - candle.close(0))
        _range = candle.high(0) - candle.low(0)

        if _body / _range <= 0.1:
            _bodyMidPoint = (candle.open(0) + candle.close(0)) / 2

            if _bodyMidPoint <= candle.low(0) + _range * 0.25:
                patternName = 'Gravestone Doji'

        return patternName
    

    def ptPaperUmbrella(self, candle, tolerance = 0.07):
        '''
        After a downtrend: Hammer (Bullish)
        After an uptrend: Hanging Man (Bearish)
        '''
        patternName = False

        _body = abs(candle.open(0) - candle.close(0))

        _wick = min((candle.high(0) - candle.open(0)), (candle.high(0) - candle.close(0)))
        _shadow = min((candle.open(0) - candle.low(0)), (candle.close(0) - candle.low(0)))

        if (_shadow / _body) >= 2 and (_wick / _body) <= tolerance:
            patternName = 'Paper Umbrella'

        return patternName
    

    def ptInvertedPaperUmbrella(self, candle, tolerance = 0.07):
        '''
        After a downtrend: Inverted Hammer (Bullish)
        After an uptrend: Shooting Star (Bearish)
        '''
        patternName = False

        _body = abs(candle.open(0) - candle.close(0))

        _wick = min((candle.high(0) - candle.open(0)), (candle.high(0) - candle.close(0)))
        _shadow = min((candle.open(0) - candle.low(0)), (candle.close(0) - candle.low(0)))

        if (_wick / _body) >= 2 and (_shadow / _body) <= tolerance:
            patternName = 'Inverted Paper Umbrella'

        return patternName


    def ptBullishEngulfing(self, candle):
        '''
        After a downtrend: Bullish
        '''
        patternName = False

        if candle.colour(-1) == 'RED' and candle.colour(0) == 'GREEN':
            if (candle.open(0) < candle.close(-1)) and (candle.close(0) > candle.open(-1)):
                patternName = 'Bullish Engulfing'

        return patternName
        

    def ptBearishEngulfing(self, candle):
        '''
        After an uptrend: Bearish
        '''
        patternName = False

        if candle.colour(-1) == 'GREEN' and candle.colour(0) == 'RED':
            if (candle.open(0) > candle.close(-1)) and (candle.close(0) < candle.open(-1)):
                patternName = 'Bearish Engulfing'

        return patternName
    

    def ptPiercing(self, candle):
        '''
        After a downtrend: Bullish
        '''
        patternName = False

        if candle.colour(-1) == 'RED' and candle.colour(0) == 'GREEN':
            if (candle.open(0) < candle.close(-1)) and (candle.close(0) < candle.open(-1)) and (candle.close(0) >= candle.open(-1) - (0.5 * (candle.open(-1) - candle.close(-1)))):
                patternName = 'Piercing'

        return patternName


    def ptDarkCloudCover(self, candle):
        '''
        After an uptrend: Bearish
        '''
        patternName = False
        
        if candle.colour(-1) == 'GREEN' and candle.colour(0) == 'RED':
            if (candle.open(0) > candle.close(-1)) and (candle.close(0) > candle.open(-1)) and (candle.close(0) <= candle.close(-1) - (0.5 * (candle.close(-1) - candle.open(-1)))):
                patternName = 'Dark Cloud Cover'

        return patternName

    
    def ptBullishHarami(self, candle):
        '''
        After a downtrend: Bullish
        '''
        patternName = False
        
        if candle.colour(-1) == 'RED' and candle.colour(0) == 'GREEN':
            if (candle.open(0) > candle.close(-1)) and (candle.close(0) < candle.open(-1)):
                patternName = 'Bullish Harami'

        return patternName


    def ptBearishHarami(self, candle):
        '''
        After an uptrend: Bearish
        '''
        patternName = False
        
        if candle.colour(-1) == 'GREEN' and candle.colour(0) == 'RED':
            if (candle.open(0) < candle.close(-1)) and (candle.close(0) > candle.open(-1)):
                patternName = 'Bearish Harami'

        return patternName


    def ptMorningStar(self, candle):
        '''
        After a downtrend: Bullish
        '''
        patternName = False

        if candle.colour(-2) == 'RED' and (candle.high(-2) - candle.low(-2)) > max(abs(candle.high(-3) - candle.low(-3)), abs(candle.high(-4) - candle.low(-4)), abs(candle.high(-5) - candle.low(-5)), abs(candle.high(-6) - candle.low(-6)), abs(candle.high(-7) - candle.low(-7))):
            minus_one_doji = False

            if abs(candle.open(-1) - candle.close(-1)) / candle.high(-1) - candle.low(-1) <= 0.1:
                    minus_one_doji = True

            minus_one_spinning_top = False ##  yet to be included

            if minus_one_doji == True or minus_one_spinning_top == True: 
                if candle.colour(0) == 'GREEN' and (candle.open(0) > max(candle.open(-1), candle.close(-1))) and (candle.close(0) >= candle.open(-2)):
                    patternName = 'Morning Star'

        return patternName
    

    def ptEveningStar(self, candle):
        '''
        After an uptrend: Bearish
        '''
        patternName = False

        if candle.colour(-2) == 'GREEN' and (candle.high(-2) - candle.low(-2)) > max(abs(candle.high(-3) - candle.low(-3)), abs(candle.high(-4) - candle.low(-4)), abs(candle.high(-5) - candle.low(-5)), abs(candle.high(-6) - candle.low(-6)), abs(candle.high(-7) - candle.low(-7))):
            minus_one_doji = False

            if abs(candle.open(-1) - candle.close(-1)) / candle.high(-1) - candle.low(-1) <= 0.1:
                    minus_one_doji = True

            minus_one_spinning_top = False ## yet to be included

            if minus_one_doji == True or minus_one_spinning_top == True: 
                if candle.colour(0) == 'RED' and (candle.open(0) < min(candle.open(-1), candle.close(-1))) and (candle.close(0) <= candle.open(-2)):
                    patternName = 'Evening Star'

        return patternName
    

    def getCandleObject(self):
        candleObj = Candle(self.df)

        return candleObj


    def getScanAnalysis(self):
        candleObj = self.getCandleObject()

        patterns = []
        
        _pattern = self.ptBullishMarubozu(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptBearishMarubozu(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
            
        _pattern = self.ptSpinningTop(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptDoji(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptDragonflyDoji(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptGravestoneDoji(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)

        _pattern = self.ptPaperUmbrella(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptInvertedPaperUmbrella(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptBullishEngulfing(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptBearishEngulfing(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)

        _pattern = self.ptPiercing(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptDarkCloudCover(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)

        _pattern = self.ptBullishHarami(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptBearishHarami(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)

        _pattern = self.ptMorningStar(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)
        
        _pattern = self.ptEveningStar(candleObj)
        if _pattern is not False:
            patterns.append(_pattern)

        return patterns