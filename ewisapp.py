import numpy as np 
import pandas as pd
import requests
import streamlit as st
import math

st.write("""
# Equal Weight Investment Strategy

Please enter the amount you are willing to invest, i.e, the value of your portfolio, in order to obtain an equal-weight investment distribution for Top 100 cryptocurrencies.

### Top 100 Cryptocurrencies

""")


api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
data = requests.get(api_url).json()


my_columns = ['Name', 'Ticker', 'Current Price', 'Market Capitalization', 'Number of Tokens to Buy']
final_dataframe = pd.DataFrame(columns = my_columns)

for i in data:
    name = i['name']
    ticker = i['symbol']
    price = i['current_price']
    market_cap = i['market_cap']
    final_dataframe = final_dataframe.append(
    pd.Series(
        [
            name,
            ticker.upper(),
            price,
            market_cap,
            'N/A'
        ],
            index = my_columns,
    ),
        ignore_index = True
)
st.dataframe(final_dataframe, 1200, 900)

portfolio_size = st.number_input('Enter the value of your portfolio')

position_size = portfolio_size / len(final_dataframe.index)

print(position_size)

for i in range(0, len(final_dataframe.index)):
   final_dataframe.loc[i, 'Number of Tokens to Buy'] = math.floor(position_size / final_dataframe['Current Price'][i])
st.dataframe(final_dataframe, 1200, 900)

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(final_dataframe)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='fianl_dataframe.csv',
    mime='text/csv',
)