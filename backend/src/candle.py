class Candle:
    def __init__(self, dataframe, ticker):
        self.data = dataframe
        self.ticker = ticker
        
    def open(self, index):
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Open'))]

    def close(self, index):
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Close'))]

    def high(self, index):
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'High'))]

    def low(self, index):        
        return self.data.iat[index - 1, self.data.columns.get_loc((self.ticker, 'Low'))]

    def colour(self, index):
        if self.close(index) > self.open(index):
            colour = 'GREEN'
        elif self.close(index) < self.open(index):
            colour = 'RED'
        else:
            colour = 'NA'
        return colour