import requests
import simplejson as json
from datetime import datetime
import streamlit as st
import altair as alt
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv("key")



ticker=st.text_input("Ticker symbol: ", 'AAPL')
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
response = requests.get(url)
if 'Error Message' in response.json():
    st.text(response.json()['Error Message'])
else:
    data=response.json()['Time Series (Daily)']
    data= {key: data[key]['5. adjusted close'] for key in sorted(data.keys())}
    x, y = zip(*sorted(data.items()))
    y = [float(i) for i in y]
    temp = pd.DataFrame({'Date':x, 'Price':y})
    temp['Date']=pd.to_datetime(temp['Date'])
    title = 'Historical Adjusted Closing Price for '+ticker
    c= alt.Chart(temp).mark_line().encode(
        x='Date',
        y='Price').properties(title=title)
    st.write(c)
