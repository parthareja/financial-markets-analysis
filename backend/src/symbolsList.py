symbolsList = ['HDFCBANK.NS', 'TCS.NS']

from data import Data
a = Data(symbolsList, '1mo').fetchData()
print(a)
#self, tickersArr, period, interval = None):
