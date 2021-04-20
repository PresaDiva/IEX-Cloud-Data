class Stock_IEX:

    def __init__(self,key):
        self.key = key

    import requests
    import json
    from pandas.io.json import json_normalize
    import pandas as pd
    import numpy as np

    def get_quote(self,ticker,range = 'YTD'):
      """
      Returns the historic daily stock prices for one ticker
      API Documentation
      https://iexcloud.io/docs/api/#historical-prices

      Arguements
      -- ticker -> One ticker (STR)
      -- range (Optional, default = YTD, STR)
            Options: max, 5y, 2y, 1y, ytd, 6m, 3m, 1m, 1mm, 5d, 5dm
      """
      temp = self.pd.DataFrame()
      base_url = 'https://sandbox.iexapis.com/'+'stable/stock/'
      url = base_url + ticker + '/chart/' + range
      company = self.requests.get(url, params = {"token": self.key})
      if company.status_code != 200: print(company) #Error Checking
      company = company.json()
      company = self.pd.DataFrame(company)
      temp = self.pd.concat([temp,company]).drop_duplicates()
      return temp

    def get_daily_stocks(self,tickers,range = 'ytd',return_value = 'close'):
        """
        Returns daily stock data for entered tickers.
        -- Tickers -> List[] of stock tickers
        -- Range -> time frame (Optional, default = YTD, STR)
            Options: max, 5y, 2y, 1y, ytd, 6m, 3m, 1m, 1mm, 5d, 5dm
        -- Return_value -> (Optional,default = close, STR)
            Options: open, close, high, low, volume, change, changePercent
        """
        temp = self.pd.DataFrame()
        for i,t in enumerate(tickers):
          stock_temp = self.get_quote(t,range)
          if i == 0:
            temp['date'] = stock_temp['date']
            temp[t] = stock_temp[return_value]
          temp[t] = stock_temp[return_value]
        temp.set_index('date', inplace = True)
        temp.index = self.pd.to_datetime(temp.index, format='%Y-%m-%d').to_period('D')
        temp = temp.sort_index()
        return temp
