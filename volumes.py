from data import Data


class VolumeAnalysis:
    def __init__(self, index, smaLength):
        self.index = index
        self.period = smaLength


    def _getVolCurrent(self, _volDF, _dictWeights):
        _volCur = 0
        _denominator = 0

        for i in _volDF[f'Volume']:
            _volN = _volDF[f'Volume'][i][-1]
            _weightN = _dictWeights[_volDF[f'Volume'][i].name]

            _volCur += _volN * _weightN
            _denominator += 1

        _volCur /= _denominator

        return _volCur
    

    def _getVolSMA(self, _volDF, _dictWeights, _dictCurrentVolumes = False):
        _volSMA = 0
        _denominator1 = 0

        if _dictCurrentVolumes == True:
            _dictCurrentVolumes = {}

            for i in _volDF['Volume']:
                _num = 0
                _denominator = 0

                for j in _volDF['Volume'][i]:
                    _num += j * _dictWeights[i]
                    _denominator += 1
                _dictCurrentVolumes.update({i: j})

                _volSMA += _num
                _denominator1 += 1

            _volSMA /= _denominator1
            _volSMA /= _denominator

            return _volSMA, _dictCurrentVolumes

        else:
            for i in _volDF['Volume']:
                _num = 0
                _denominator = 0

                for j in _volDF['Volume'][i]:
                    _num += j * _dictWeights[i]
                    _denominator += 1

                _volSMA += _num
                _denominator1 += 1

            _volSMA /= _denominator1
            _volSMA /= _denominator

            return _volSMA


    def _getPercentageWRTSimpleVolAnalysis(self, _volDF):
        _dictWeights = {}

        for i in _volDF['Volume']:
            _dictWeights.update({i: 1/len(_volDF['Volume'].columns)})

        _volCurrent = self._getVolCurrent(_volDF, _dictWeights)
        _volSMA, _dictCurrentVolumes = self._getVolSMA(_volDF, _dictWeights, True)
        
        _percentage = (_volCurrent / _volSMA) * 100

        return round(_percentage, 2), _dictCurrentVolumes
        

    def _getPercentageWRTWeightedVolAnalysis(self, _volDF, _dictWeights):
        _volCurrent = self._getVolCurrent(_volDF, _dictWeights)
        _volSMA = self._getVolSMA(_volDF, _dictWeights)

        _percentage = (_volCurrent / _volSMA) * 100

        return round(_percentage, 2)


    def _getDictCoVolPercentages(self, _volDF, _dictCurrentVolumes):
        _dictCoVolPercentage = {}
        
        for i in _volDF[f'{self.period}d-SMA Volume']:
            _ptg = (_dictCurrentVolumes[_volDF[f'{self.period}d-SMA Volume'][i].name] / _volDF[f'{self.period}d-SMA Volume'][i].iat[-1]) * 100
            _dictCoVolPercentage.update({_volDF[f'{self.period}d-SMA Volume'][i].name: round(_ptg, 2)})

        return _dictCoVolPercentage
    
    def getVolumeAnalysis(self):
        """
        hello world
        """
        dataObj = Data(self.index, self.period, False, None)

        _tickers = dataObj.getTickers()
        _volDF = dataObj.getVolumeData(_tickers)

        simple, _dictCurrentVolumes = self._getPercentageWRTSimpleVolAnalysis(_volDF)

        _dictWeights = dataObj.getWeights(_tickers)
        weighted = self._getPercentageWRTWeightedVolAnalysis(_volDF, _dictWeights)
    
        _dictCoVolPercentages = self._getDictCoVolPercentages(_volDF, _dictCurrentVolumes)

        return simple, weighted, _dictCoVolPercentages