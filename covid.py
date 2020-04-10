#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np


# In[2]:


def doubling(readings):
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
    return double


# In[3]:


def readfile():
    df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
    df = df.loc[(df['state']=="Massachusetts") | (df['state']=="New York")| (df['state']=="California")]
    df = df.loc[df['date'] > "2020-03-15"]
    df = df.assign(casesc=df['cases'].diff(3))
    df = df.assign(deathsc=df['deaths'].diff(3))
    df['date'] = pd.to_datetime(df['date'])
    df.index = pd.to_datetime(df.date)
    return df


# In[4]:


def graph(df):
    state = ["Massachusetts", "New York", "California"]
    states = [state for state in state for _ in range(2)]
    var = ["cases", "deaths"]
    plot_titles = [s + " " + v for s in state for v in var]
    vals1 = [v for v in var*3]
    vals2 = ["cases", "casesc", "deaths", "deathsc", 
            "cases", "casesc", "deaths", "deathsc"]
    plt.style.use('seaborn-darkgrid')
    plt.rcParams["figure.figsize"] = (24, 9) # (w, h)
    xformatter = mdates.DateFormatter("%m-%d")
    yformatter = ticker.StrMethodFormatter('{x:,.0f}')


    for i in range(6):
        plt.subplot(3, 2, i+1)
        plt.plot('date', vals1[i], data = df[df.state == states[i]])
        plt.plot('date', vals2[i], data = df[df.state == states[i]])
        plt.title(plot_titles[i])
        plt.gca().xaxis.set_major_formatter(xformatter)
        plt.gca().yaxis.set_major_formatter(yformatter)
        plt.legend()

    plt.savefig("graph")


# In[5]:


def calcmerge(state, data):
    date = data[data['state']==state].date
    cases = data[data['state']==state].cases.to_numpy()
    deaths = data[data['state']==state].deaths.to_numpy()
    casesd = doubling(cases)
    deathsd = doubling(deaths)
    zipped = zip(date, cases, deaths, casesd, deathsd)
    return zipped


# In[6]:


def graphrow(df, state):
    plt.subplot(1, 2, 1)
    plt.title(state + " count (lower is better)")
    xformatter = mdates.DateFormatter("%m-%d")
    yformatter = ticker.StrMethodFormatter('{x:,.0f}')
    
    plt.plot(df.date, df['cases'])
    plt.plot(df.date, df['deaths'])
    plt.gca().xaxis.set_major_formatter(xformatter)
    plt.gca().yaxis.set_major_formatter(yformatter)
    plt.legend(['cases', 'deaths'])

    plt.subplot(1, 2, 2)
    plt.title("days to double (higher is better)")
    plt.plot(df.date, df['dbl cas'])
    plt.plot(df.date, df['dbl deat'])
    plt.gca().xaxis.set_major_formatter(xformatter)
    plt.gca().yaxis.set_major_formatter(yformatter)
    plt.legend(['cases', 'deaths'])
    plt.savefig("graph" + state.replace(" ", "").lower())
    plt.clf()


# In[7]:


def graphdbl(dta, state):
    r = calcmerge(state, dta)
    df = pd.DataFrame(r, columns=['date', 'cases', 'deaths', 'dbl cas', 'dbl deat'])
    graphrow(df, state)


# In[8]:


def graphprep():
    plt.rcParams["figure.figsize"] = (10, 3) # (w, h)
    plt.style.use('seaborn-darkgrid')


# In[9]:


d = readfile()
graphprep()
graphdbl(d,'New York')
graphdbl(d,'Massachusetts')
graphdbl(d,'California')


# In[ ]:




