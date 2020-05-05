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


# In[ ]:





# In[2]:


def compute(df, states, variables):
    df = df.loc[(df['state'].isin(states))]
    df = df.loc[df['date'] > "2020-04-01"]
    df = df.assign(casesc=df['cases'].diff(len(states)))
    df = df.assign(deathsc=df['deaths'].diff(len(states)))
    df = df.assign(deathsd=df.groupby('state')['deaths'].apply(doubling))
    df = df.assign(casesd=df.groupby('state')['cases'].apply(doubling))
    df['date'] = pd.to_datetime(df['date'])
    df = df.melt(id_vars=['date', 'state'])
    df = df[df.variable.isin(variables)]
    return df


# In[3]:


def read_data():
    states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
    usa = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    usa['state'] = "USA"
    df = pd.concat([states, usa], ignore_index=True, sort=False)
    return df


# In[4]:


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


# In[5]:


def graph_a(df, states, variables, filename, ratio):
    sns.set()
    plt.style.use('seaborn-darkgrid')
    g = sns.FacetGrid(df, row="variable", col="state", sharex=True, row_order=variables, sharey=False, height=ratio[0], aspect=ratio[1])
    g = g.map(plt.plot, "date", "value", marker='o', markersize=0.7)
    xformatter = mdates.DateFormatter("%m/%d")
    g.axes[0,0].xaxis.set_major_formatter(xformatter)
    g.set_titles("{col_name}", size=16)
    labelmap = {"deathsd": "Deaths Doubling", 
                "deaths": "Deaths",
                "cases": "Cases", 
                "casesd": "Cases Doubling"}
    for i in range(len(variables)):
        g.axes[i,0].set_ylabel(labelmap[variables[i]])
    plt.tight_layout()
    plt.savefig(filename)


# In[57]:


def graph_b(df, states, variables, filename, ratio):
    sns.set()
    plt.style.use('seaborn-darkgrid')
    g = sns.FacetGrid(df, col="variable", hue='state', sharex=True, row_order=variables, sharey=False, height=ratio[0], aspect=ratio[1])
    g = g.map(plt.plot, "date", "value")
    g.add_legend()
    labelmap = {"deathsd": "Deaths Doubling (higher is better)", 
                "deaths": "Deaths",
                "cases": "Cases", 
                "casesd": "Cases Doubling (higher is better)"}
    for i in range(len(variables)):
        g.axes[0,i].set_title(labelmap[variables[i]])
    xformatter = mdates.DateFormatter("%m/%d")
    xlocator = mdates.DayLocator(bymonthday=[1,5,10, 15, 20, 25])
    ylocator = ticker.AutoLocator()
    yformatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    g.axes[0,0].xaxis.set_major_formatter(xformatter)
    g.axes[0,0].xaxis.set_major_locator(xlocator)
    g.axes[0,0].yaxis.set_major_formatter(yformatter)
    g.axes[0,1].yaxis.set_major_formatter(yformatter)
    plt.savefig(filename)


# In[58]:


df = read_data()
states = ["Massachusetts", "USA", "New York", "South Carolina", "District of Columbia", "Illinois"]# , "New York"]# , "New York", "District of Columbia", "California"]
variables = ["casesd", "deathsd"]
df1 = compute(df, states, variables)
graph_b(df1, states, variables, "graph1", [2,2.5])

states = ["District of Columbia", "South Carolina"] # , "New York"]# , "New York", "District of Columbia", "California"]
variables = ["cases", "deaths"]
df1 = compute(df, states, variables)
graph_b(df1, states, variables, "graph2", [2,2.5])

states = ["Massachusetts", "California", "Illinois", "Florida"]
df1 = compute(df, states, variables)
graph_b(df1, states, variables, "graph3", [2,2.5])

states = ["USA", "New York"]
df1 = compute(df, states, variables)
graph_b(df1, states, variables, "graph4", [2,2.5])


# In[ ]:





# In[ ]:




