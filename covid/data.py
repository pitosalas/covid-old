import pandas as pd
import numpy as np


def read_cdc_data(start_date, states):
    dt = (pd.read_csv("https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD&bom=true&format=true",
                      na_values=['(NA)', ''], thousands=',', parse_dates=['Week Ending Date']).fillna(0)
          .query("Outcome == 'All causes'")
          .query("Type == 'Predicted (weighted)'")
          .rename(columns={'Excess Lower Estimate': 'excessl', 'Excess Higher Estimate': "excessh", 'Week Ending Date': 'date', 'State': 'state'})
          .query("date > '" + start_date + "'")
          .query("state in @states")
          .set_index('date', drop=True)
          .pivot(columns='state', values=['excessl', 'excessh'])
          .resample('D')
          .interpolate(method='cubic')
          .stack(level=1)
          .reset_index(level=1)
          .reset_index('date')
          .melt(id_vars=['date', 'state'])
          )
    return dt


def process_cdc(df, start_date, include_variables, include_states):
    df = df[df.variable.isin(include_variables)]
    return df


def read_nyt_data(start_date, include_states):
    states = pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", parse_dates=True)
    states = states.loc[(states['state'].isin(include_states))]
    usa = pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv", parse_dates=True)
    usa['state'] = "USA"
    if ("USA" in include_states):
        states = pd.concat([states, usa], sort=False)
    states = states.loc[states['date'] > start_date]
    return states


def process_nyt(df, include_variables):
    df = df.assign(deathsd=df.groupby('state')['deaths'].apply(doubling))
    df = df.assign(casesd=df.groupby('state')['cases'].apply(doubling))
    df = df.assign(casesc=df.groupby('state')['cases'].diff())
    df = df.assign(deathsc=df.groupby('state')['deaths'].diff())
    df['casesr'] = df.groupby('state')['casesc'].rolling(
        7).mean().reset_index(0, drop=True)
    df['deathsr'] = df.groupby('state')['deathsc'].rolling(
        7).mean().reset_index(0, drop=True)
    df['date'] = pd.to_datetime(df['date'])
    df = df.melt(id_vars=['date', 'state'])
    df = df[df.variable.isin(include_variables)]
    return df


def read_data(start_date, states, variables):
    nyt = read_nyt_data(start_date, states)
    nyt = process_nyt(nyt, variables)
    cdc = read_cdc_data(start_date, states)
    cdc = process_cdc(cdc, start_date, variables, states)
    res = pd.concat([cdc, nyt], sort=False)
    return res


def doubling(indata):
    readings = indata.to_numpy()
    readingsLength = len(readings)
    double = np.zeros(readingsLength)
    double[:] = np.NaN
    for i in range(readingsLength - 1, -1, -1):
        target = readings[i]
        count = 0
        for j in range(i, -1, -1):
            diffsofar = target-readings[j]
            exact = target / 2
            if diffsofar > exact:
                f = (exact - readings[j]) / (readings[j]-readings[j+1]) + count
                double[i] = f
                break
            else:
                count = count+1
    outdata = pd.Series(data=double, name=indata.name, index=indata.index)
    return outdata
