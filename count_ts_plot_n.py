#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 14:11
# @Author  : Vincent
# @Site    :
# @File    : amount_ts_plot_n.py
# @Software: PyCharm
# @Describe:

# !/usr/bin/env python
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
import plotly.offline
import numpy as np

np.random.seed(1)
seeds = np.random.randint(0, 999, 10000)

seed_id = 0



df = pd.read_csv('../data/data_9.csv')
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
        # row[col] = df3['Near Risk Amount(in USD)'].sum() + df3['Far Risk Amount'].sum()
        row[col] = df3.shape[0]

df3 = df
df = df2

# 把0填上


for index, row in df.iterrows():
    if index.dayofweek <= 4:
        for col in df.columns:
            np.random.seed(seeds[seed_id])
            seed_id += 1
            temp = np.random.random()
            print(temp)
            if temp > 0.3:
                np.random.seed(seeds[seed_id])
                seed_id += 1
                aa = np.random.randint(0, 145)
                np.random.seed(seeds[seed_id])
                seed_id += 1
                bb = np.random.randint(0, 9)
                row[col] = df.values[aa, bb]

trace_dealer = []
for i in range(len(df.columns)):
    td = go.Scatter(
        x=df.index,
        y=df[f'Dealer{i+1}'],
        name=f'Dealer{i+1}',
        opacity=0.8

    )
    trace_dealer.append(td)

# trace_dealer1 = go.Scatter(
#     # x=df.Date,
#     x = df.index, #!!!!!!!!!!
#     # y=df['AAPL.High'],
#     y = df['Dealer1'],
#     name="Dealer1",
#     # line=dict(color='#17BECF'),
#     opacity=0.8)
#
# trace_dealer2 = go.Scatter(
#     # x=df.Date,
#     x = df.index, #!!!!!!!!!!
#     # y=df['AAPL.High'],
#     y = df['Dealer2'],
#     name="Dealer2",
#     # line=dict(color='#17BECF'),
#     opacity=0.8)

# data = [trace_dealer1, trace_dealer2]
data = trace_dealer

layout = dict(
    title='Count Time Series',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label='1w',
                     step='day',
                     stepmode='backward'),
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename="Count Time Series n.html")
# py.plot(fig, filename="Amount Time Series")

# 1月5日至5月29日
