class Candle:
    def __init__(self, dataframe, ticker):
        self.data = dataframe
        self.ticker = ticker
        


    def open(self, index):
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Open'))]

    def close(self, index):
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Close'))]
        # return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Adj Close'))]
        # pass

    def high(self, index):
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'High'))]

    def low(self, index):        
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Low'))]

    def colour(self, index):
        if self.close() > self.open():
            colour = 'Green'
        elif self.close() < self.open():
            colour = 'Red'
        # else:
        #     colour = 
        return colour



# symbolsList = ['HDFCBANK.NS', 'TCS.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS']
# # symbolsList = ['HDFCBANK.NS', 'TCS.NS']


# ####### DRIVER
# from data import Data
# a = Data(symbolsList, '1mo')

# data = a.fetchData()
# print(data)

# b = Candle(data, 'ADANIPORTS.NS')
# print(b.high(-6))


# index as object (class) attribute or method attrobute?????