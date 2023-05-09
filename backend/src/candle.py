class Candle:
    def __init__(self, dataframe):
        self.df = dataframe

    
    def open(self, _index):
        return self.df.iat[_index - 1, self.df.columns.get_loc('Open')]
    
    
    def close(self, _index):
        return self.df.iat[_index - 1, self.df.columns.get_loc('Close')]
    

    def high(self, _index):
        return self.df.iat[_index - 1, self.df.columns.get_loc('High')]
    

    def low(self, _index):        
        return self.df.iat[_index - 1, self.df.columns.get_loc('Low')]
    

    def colour(self, _index):
        if self.close(_index) > self.open(_index):
            colour = 'GREEN'
        elif self.close(_index) < self.open(_index):
            colour = 'RED'
        else:
            colour = 'NA'
        return colour