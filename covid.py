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
import argparse


# In[2]:


def process_nyt(df, include_variables):
    df = df.assign(deathsd=df.groupby('state')['deaths'].apply(doubling))
    df = df.assign(casesd=df.groupby('state')['cases'].apply(doubling))
    df = df.assign(casesc=df.groupby('state')['cases'].diff())
    df = df.assign(deathsc=df.groupby('state')['deaths'].diff())
    df['casesr'] = df.groupby('state')['casesc'].rolling(7).mean().reset_index(0,drop=True)
    df['deathsr'] = df.groupby('state')['deathsc'].rolling(7).mean().reset_index(0,drop=True)
    df['date'] = pd.to_datetime(df['date'])
    df = df.melt(id_vars=['date', 'state'])
    df = df[df.variable.isin(include_variables)]
    return df    


# In[3]:


def read_nyt_data(start_date, include_states):
    states = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", parse_dates=True)
    states = states.loc[(states['state'].isin(include_states))]
    usa = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv", parse_dates=True)
    usa['state'] = "USA"
    if ("USA" in include_states):
        states = pd.concat([states, usa], sort=False)
    states = states.loc[states['date'] > start_date]
    return states


# In[4]:


def read_cdc_data(start_date, states):
    dt = (pd.read_csv("https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD&bom=true&format=true",
                     na_values=['(NA)', ''], thousands=',', parse_dates=['Week Ending Date']).fillna(0)
      .query("Outcome == 'All causes'")
      .query("Type == 'Predicted (weighted)'")
      .rename(columns={'Excess Lower Estimate': 'excessl', 'Excess Higher Estimate': "excessh", 'Week Ending Date': 'date', 'State':'state'})
      .query("date > '" + start_date + "'")
      .query("state in @states")
      .set_index('date', drop=True)
      .pivot(columns='state', values=['excessl', 'excessh'])
      .resample('D')
      .interpolate()
      .stack(level=1)
      .reset_index(level=1)
      .reset_index('date')
      .melt(id_vars=['date','state'])
     )
    return dt


# In[5]:


#read_cdc_data("2020-05-01", ["Florida", "South Carolina"])


# In[6]:


def process_cdc(df, start_date, include_variables, include_states):
    df = df[df.variable.isin(include_variables)]
    return df 


# In[7]:


def read_data(start_date, states, variables):
    nyt = read_nyt_data(start_date, states)
    nyt = process_nyt(nyt, variables)
    cdc = read_cdc_data(start_date, states)
    cdc = process_cdc(cdc, start_date, variables, states)
    res = pd.concat([cdc, nyt], sort=False)
    return res


# In[18]:


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


# In[23]:


def graph_b(df, states, variables, filename, ratio):
    sns.set()
    plt.style.use('seaborn-darkgrid')
    g = sns.FacetGrid(df, col="variable", hue='state', sharex=True, col_order=variables, sharey=False, height=ratio[0], aspect=ratio[1])
    g = g.map(plt.plot, "date", "value")
    g.add_legend()
    labelmap = {"deathsd": "Deaths Doubling", 
                "deaths": "Deaths",
                "cases": "Cases", 
                "casesd": "Cases Doubling",
                "casesc": "New Cases", 
                "deathsc": "New Deaths",
                "excessl": "Excess Deaths",
                "excessh" : "Excess Deaths (h)",
               "deathsr": "New Deaths (rolling average)",
               "casesr": "New Cases (rolling average)"}
    for i in range(len(variables)):
        g.axes[0,i].set_title(labelmap[variables[i]])
    xformatter = mdates.DateFormatter("%m/%d")
    xlocator = mdates.DayLocator(bymonthday=[1,5,10, 15, 20, 25])
    ylocator = ticker.AutoLocator()
    yformatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    g.axes[0,0].xaxis.set_major_formatter(xformatter)
    g.axes[0,0].xaxis.set_major_locator(xlocator)
    g.axes[0]
    [axis[0].yaxis.set_major_formatter(yformatter) for axis in g.axes]
    plt.savefig(filename)


# In[35]:


parser = argparse.ArgumentParser(description='Generate COVID graphs')
parser.add_argument("filename", action="store")
parser.add_argument("--states", nargs="+", type=str)
parser.add_argument("--vars", nargs="+", type=str)
#args = parser.parse_args('xxx --states ma fl --vars  excessl excessh'.split())
args = parser.parse_args()


# In[39]:


def print_spec(states, variables, date, filename, dimensions):
    states_s = ', '.join(str(x) for x in states)
    variables_s = ', '.join(str(x) for x in variables)
    print("Graph start date: ", date, "- for ", states_s, "- showing ", variables_s)


# In[40]:


def report_row(df, states, variables, date, filename, dimensions):
    print_spec(states, variables, date, filename, dimensions)
    graph_b(df, states, variables, filename, dimensions)


# In[41]:


statesmap = {"nc" : "North Carolina",
             "wv" : "West Virginia",
             "sc" : "South Carolina",
             "dc" : "District of Columbia",
             "ma" : "Massachusetts",
             "nh" : "New Hampshire", 
             "ny" : "New York",
            "wa" : "Washington",
            "nj": "New Jersey",
            "ca" : "California",
             "tx" : "Texas",
             "fl" : "Florida",
             "usa" : "USA"
            }
states = list(map(lambda state: statesmap[state], args.states))
variables = args.vars
startdate = "2020-04-01"
dim = [4, 2.5]
df = read_data(startdate, states, variables)
report_row(df, states, variables, startdate, args.filename, dim)


# In[ ]:


def test_data():
    return (pd.DataFrame({"date": ["2020-01-01","2020-01-01","2020-01-02","2020-01-02",
                                   "2020-01-03","2020-01-03","2020-01-04","2020-01-04"],
                         "state": ["A", "B", "A", "B", "A", "B", "A", "B"],
                         "cases": [10,  30,   20,  50,  30,  70,  40, 100],
                         "deaths": [1,   3,    2,   6,   5,   25, 10,  30]}))


# In[ ]:




