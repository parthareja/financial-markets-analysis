from data import Data
from candle import Candle


class Scan:
    def __init__(self, objCandle):
        self.objCandle = objCandle
    
    
    def scan(self):
        scanDictBull = {}
        scanDictBear = {}
        
        b = self.pt3()
        a = self.pattern2()
        c = self.test()

        if self.pt3():
            scanDictBull['Pattern3'] = self.pt3()
        if c:
            scanDictBull['TEST'] = c
        if self.pattern2():
            scanDictBull['Pattern2'] = self.pattern2()

        return scanDictBull
    

    def hammer(self):
        existsArr = []
        for obj in self.objCandle:
            if (obj.high(0) - obj.low(0)) < (obj.open(-1) - obj.close(-1)):
                existsArr.append(obj.ticker)

        return existsArr
    

    def test(self):
        existsArr = []
        for obj in self.objCandle:
            if obj.open(0) == obj.high(0):
                existsArr.append(obj.ticker)
        return existsArr
        # pass

        # self.hammer()
        # self.pattern2()
        # self.pattern3()
        # dictionary = {'Hammer': self.hammer()}

        # return dictionary
        # a = self.hammer()
        # return a
        # pass
        # return self.hammer()


    def pt3(self):
            existsArr = []
            for obj in self.objCandle:
                if obj.open(0) < obj.close(0):
                    if obj.open(-1) > obj.close(-1):
                        if abs(obj.open(-1) - obj.close(-1)) > abs(obj.open(0) - obj.close(0)):
                            if obj.close(-1) < obj.open(0) and obj.open(-1) > obj.close(0):
                                existsArr.append(obj.ticker)
                            
                        # load open(-1), open(0), close(-1), close(0) etc. in a variable instead of calling fxns everydamntime (or check where variables most efficient)
            return existsArr


    def pattern2(self):
        existsArr = []
        
        for obj in self.objCandle:
            if obj.high(0) > obj.low(0):
                existsArr.append(obj.ticker)

        return existsArr

# ADD VOLUMES ALSO IN SCAN??? OR MAYBE ONLY FOR REQD. COMPANIES IDK
# perhaps add volumes as a separate thingy where volumes are greater than a specific no.? idk would be kinda using the vol analysis but righso what its good hmm idk 