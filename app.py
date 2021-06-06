import requests
import simplejson as json
from datetime import datetime
import datetime
import streamlit as st
import altair as alt
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("key")



ticker=st.text_input("Ticker symbol: ", 'AAPL')
start_date=st.sidebar.date_input('start date', datetime.date(2011,1,1))
end_date=st.sidebar.date_input('end date', datetime.date(2021,1,1))
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}&outputsize=full'.format(ticker, key)
response = requests.get(url)
if 'Error Message' in response.json():
    st.text(response.json()['Error Message'])
else:
    if start_date < end_date:
            data=response.json()['Time Series (Daily)']
            data= {key: data[key]['5. adjusted close'] for key in sorted(data.keys())}
            x, y = zip(*sorted(data.items()))
            y = [float(i) for i in y]
            temp = pd.DataFrame({'Date':x, 'Price':y})
            temp['Date']=pd.to_datetime(temp['Date'])
            temp=temp[(temp['Date']>pd.to_datetime(start_date))&(temp['Date']<pd.to_datetime(end_date))]
            title = 'Historical Adjusted Closing Price for '+ticker
            c= alt.Chart(temp).mark_line().encode(
                x='Date',
                y='Price').properties(title=title)
            st.write(c)
    else:
            st.text('Start date is not before the end date!')




