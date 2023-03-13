# import requests
import yfinance as yf
import pandas as pd




# URL = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
# df = pd.read_csv(URL, index_col = 'Company Name')
# print(df)

# url = 'https://www.nseindia.com/market-data/live-equity-market?symbol=NIFTY%2050'
url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
url = 'https://www1.nseindia.com/content/indices/ind_niftybanklist.csv'


# response = requests.get(url)
# print(response)
# df = pd.read_csv(url, index_col = 'Company Name')
df = pd.read_csv(url)
print(df)

currentTickersArr = []
for i in df['Symbol']:
    currentTickersArr.append(f'{i}.NS')

print(currentTickersArr)


# url = 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
# df = pd.read_csv(url)
# arrTickers = []
# for i in df['Company Name']:
#     arrTickers.append(i)
# print(arrTickers)


# print(df)

# df2 = df.iloc[:, 0]
# print(df2)

# print(df)
# df2 = df.iloc[:, 0]
# print(df2)

#     for j in i:
#         print(j)
    
    # print(df[0])



# data = yf.download('^NSEI', period = '1mo', threads = True, group_by = 'ticker', progress = False)
# print(data)
# # stock_url = 