#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
from datetime import datetime


# In[117]:


def compute(df, states, variables, start_date):
    df = df.loc[(df['state'].isin(states))]
    df = df.loc[df['date'] > start_date]
    df = df.assign(deathsd=df.groupby('state')['deaths'].apply(doubling))
    df = df.assign(casesd=df.groupby('state')['cases'].apply(doubling))
    df = df.assign(casesc=df.groupby('state')['cases'].diff())
    df = df.assign(deathsc=df.groupby('state')['deaths'].diff())
    df['casesr'] = df.groupby('state')['casesc'].rolling(7).mean().reset_index(0,drop=True)
    df['deathsr'] = df.groupby('state')['deathsc'].rolling(7).mean().reset_index(0,drop=True)
    df['date'] = pd.to_datetime(df['date'])
    df = df.melt(id_vars=['date', 'state'])
    df = df[df.variable.isin(variables)]
    return df


# In[118]:


def read_data():
    states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
    usa = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv")
    usa['state'] = "USA"
    df = pd.concat([states, usa], sort=False)
    return df


# In[119]:


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


# In[120]:


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
                "casesd": "Cases Doubling",
                "casesc": "New Cases", 
                "deathsc": "New Deaths"}
    for i in range(len(variables)):
        g.axes[i,0].set_ylabel(labelmap[variables[i]])
    plt.tight_layout()
    plt.savefig(filename)


# In[121]:


def test_data():
    return (pd.DataFrame({"date": ["2020-01-01","2020-01-01","2020-01-02","2020-01-02",
                                   "2020-01-03","2020-01-03","2020-01-04","2020-01-04"],
                         "state": ["A", "B", "A", "B", "A", "B", "A", "B"],
                         "cases": [10,  30,   20,  50,  30,  70,  40, 100],
                         "deaths": [1,   3,    2,   6,   5,   25, 10,  30]}))


# In[122]:


def report_test():
    x = test_data()
    states = ["A", "B"]
    variables = ["cases", "casesc", "casesr"]
    y = compute(x, states, variables, "2019-01-01")
    graph_b(y, states, variables, "graph1", [4,2.5])


# In[123]:


def report_row(df, states, variables, date, filename, dimensions):
    df1 = compute(df, states, variables, date)
    graph_b(df1, states, variables, filename, dimensions)


# In[124]:


def do_report1():
    df = read_data()
    s1 = ["USA", "New York"]
    s2 = ["Massachusetts", "Florida", "California", "Washington"]
    v1 = ["casesc", "deathsc"]
    v2 = ["casesr", "deathsr"]
    dt = "2020-04-01"
    dim = [4, 2.5]
    report_row(df, s1, v1, dt, "graph1", dim)
    report_row(df, s1, v2, dt, "graph2", dim)
    report_row(df, s2, v1, dt, "graph3", dim)
    report_row(df, s2, v2, dt, "graph4", dim)               


# In[125]:


def do_report2():
    df = read_data()
    s1 = ["USA", "New York"]
    v1 = ["deaths", "deathsc", "deathsr"]
    dt = "2020-04-01"
    dim = [4, 2.5]
    report_row(df, s1, v1, dt, "graph1", dim)
    v1 = ["cases", "casesc", "casesr"]
    report_row(df, s1, v1, dt, "graph2", dim)





# In[126]:


do_report1()


# In[ ]:





# In[ ]:




