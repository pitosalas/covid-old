#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


# In[2]:


df = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")


# In[3]:


df = df.loc[(df['state']=="Massachusetts") | (df['state']=="New York")| (df['state']=="California")]


# In[4]:


df = df.loc[df['date'] > "2020-03-15"]


# In[5]:


df = df.assign(casesc=df['cases'].diff(3))


# In[6]:


df = df.assign(deathsc=df['deaths'].diff(3))


# In[7]:


df['date'] = pd.to_datetime(df['date'])


# In[8]:


df.index = pd.to_datetime(df.date)


# In[9]:


state = ["Massachusetts", "New York", "California"]
states = [state for state in state for _ in range(2)]
var = ["cases", "deaths"]
plot_titles = [s + " " + v for s in state for v in var]
vals1 = [v for v in var*3]
vals2 = ["cases", "casesc", "deaths", "deathsc", 
        "cases", "casesc", "deaths", "deathsc"]


# In[10]:


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


# In[ ]:




