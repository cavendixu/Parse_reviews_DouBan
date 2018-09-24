#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 17:03
# @Author  : Vincent
# @Site    : 
# @File    : Sentiment Index.py
# @Software: PyCharm
# @Describe:



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/3 15:16
# @Author  : Vincent
# @Site    :
# @File    : amount_ts_plot.py
# @Software: PyCharm
# @Describe: x轴是时间，y轴是amount

import pandas as pd
from datetime import datetime
import plotly.plotly as py
import plotly.graph_objs as go

df = pd.read_csv('../data/data.csv')
# sns.set_style('dark')
# 按日期排正序
df.sort_values('Deal Date', inplace=True)
max_date = max(df['Deal Date'])
min_date = min(df['Deal Date'])



def days_between(d1, d2):
    d1 = datetime.strptime(d1, '%Y/%m/%d')
    d2 = datetime.strptime(d2, '%Y/%m/%d')
    return abs((d2 - d1).days)


days = days_between(max_date, min_date)

dates = pd.date_range("1 5 2015", periods=days + 1, freq="D")

dealer_name_list = list(df['Dealer Name'].value_counts().index)
dealer_name_list.sort()

df2 = pd.DataFrame(index=dates, columns=dealer_name_list, dtype=float)

for index, row in df2.iterrows():
    for col in df2.columns:
        t = str(index).split(' ')[0].replace('-', '/')
        df3 = df[(df['Deal Date'] == t) & (df['Dealer Name'] == col)]
        row[col] = df3['Near Risk Amount(in USD)'].sum() + df3['Far Risk Amount'].sum()





df = df2


trace_dealer1 = go.Scatter(
    # x=df.Date,
    x = df.index, #!!!!!!!!!!
    # y=df['AAPL.High'],
    y = df['Dealer1'],
    name="Dealer1",
    # line=dict(color='#17BECF'),
    opacity=0.8)

trace_dealer2 = go.Scatter(
    # x=df.Date,
    x = df.index, #!!!!!!!!!!
    # y=df['AAPL.High'],
    y = df['Dealer2'] / max(df['Dealer2']),
    name="Dealer2",
    # line=dict(color='#17BECF'),
    opacity=0.8)

# data = [trace_dealer1, trace_dealer2]
data = [trace_dealer2]

layout = dict(
    title='Sentiment Index',
    xaxis=dict(

        rangeselector=dict(
            # buttons=list([
            #     dict(count=7,
            #          label='1w',
            #          step='day',
            #          stepmode='backward'),
            #     dict(count=1,
            #          label='1m',
            #          step='month',
            #          stepmode='backward'),
            #     dict(step='all')
            # ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
py.plot(fig, filename="Sentiment Index")
