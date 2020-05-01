#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from datetime import datetime


# In[2]:


def doubling(indata):
    readings = indata.to_numpy()
    readingsLength = len(readings)
    double = np.zeros(readingsLength)
    double[:] = np.NaN
    for i in range( readingsLength - 1, -1, -1):
        target = readings[i]
        count = 0
        for j in range(i, -1, -1):
            diffsofar = target-readings[j]
            exact = target / 2
            if diffsofar  > exact:
                f = (exact - readings[j]) / (readings[j]-readings[j+1]) + count
                double[i] = f
                break
            else:
                count = count+1
    outdata = pd.Series(data=double, name=indata.name, index=indata.index)
    return outdata


# In[9]:


def compute(df, states, variables):
    df = df.loc[(df['state'].isin(states))]
    df = df.loc[df['date'] > "2020-03-15"]
    df = df.assign(casesc=df['cases'].diff(len(states)))
    df = df.assign(deathsc=df['deaths'].diff(len(states)))
    df = df.assign(deathsd=df.groupby('state')['deaths'].apply(doubling))
    df = df.assign(casesd=df.groupby('state')['cases'].apply(doubling))
    df['date'] = pd.to_datetime(df['date'])
    df = df.melt(id_vars=['date', 'state'])
    df = df[df.variable.isin(variables)]
    return df


# In[48]:


def generate_graph(df, filename, ratio):
    plt.style.use('seaborn-darkgrid')
    g = sns.FacetGrid(df, row="variable", col="state", sharey=False, height=ratio[0], aspect=ratio[1])
    g = g.map(plt.plot, "date", "value", marker='o', markersize=0.7)
    xformatter = mdates.DateFormatter("%m/%d")
    g.axes[0,0].xaxis.set_major_formatter(xformatter)
    plt.tight_layout()
    plt.savefig(filename)


# In[49]:


def read_data():
    states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
    usa = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    usa['state'] = "USA"
    return pd.concat([states, usa], ignore_index=True, sort=False)


# In[54]:


states = ["Massachusetts", "USA"]# , "New York"]# , "New York", "District of Columbia", "California"]
variables = ["deathsd"]
df = read_data()
df1 = compute(df, states, variables)
generate_graph(df1, "graph1", [3,2])

states = ["District of Columbia", "California", "Florida", "Illinois", "New York"]
variables = ["deathsd", "casesd", "deaths", "cases"]
df1 = compute(df, states, variables)
generate_graph(df1, "graph2", [2,2])

             





# In[ ]:




