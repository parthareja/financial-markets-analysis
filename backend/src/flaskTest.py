from flask import Flask
from scan import Scan
from candle import Candle
from data import Data
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return 'Home'

@app.route('/volHDFCBANK')
def volTest():
   pass


@app.route('/scanNifty50')
def scan():

    dataObj = Data('NIFTY50', '1mo')
    dataframe, _tickers = dataObj.getData()
    # data = data.fetchData()

    # data = Data.transformData(data)

    objCandle = []
    for ticker in _tickers:
        objCandle.append(Candle(dataframe, ticker))
    # objCandle.append(Candle(dataframe[ticker], ticker))
    print()
    print()
    print(0)

    arr = Scan(objCandle).scan()


    return arr

if __name__ == '__main__':
    app.run()
