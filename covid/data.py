import pandas as pd
import numpy as np


def float_convert1(df, cols):
    df.loc[:, cols] = df.loc[:, cols].apply(
        lambda x: x.str.replace(',', ""))
    df = df.convert_dtypes()
    return df


def float_convert(df, cols):
    df[cols] = df[cols].replace(',', '', regex=True)
    df[cols] = df[cols].astype(float)
    return df


def date_convert(df, cols):
    df[cols] = df[cols].apply(pd.to_datetime)
    return df


def read_covidtracking_data(start_date, states):
    df = pd.read_csv("https://covidtracking.com/api/v1/states/daily.csv")
    return df

def prepare_covidtracking_data(raw_df, start_date, states):
    df = (raw_df
        .fillna(0)
        .reset_index()
        .assign(date = lambda x: pd.to_datetime(x['date'], format="%Y%m%d"))
        .query("date > @start_date")
        .query("state in @states")
        .sort_values(by='date', ascending=True)
    )
    df =df.assign(positivec = df.groupby('state')['positive'].diff())
    df =df.assign(negativec = df.groupby('state')['negative'].diff())
    df =df.assign(hospitalizedCurrentlyc = df.groupby('state')['hospitalizedCurrently'].diff())
    df['positiver']=df.groupby('state')['positivec'].rolling(
        window=3).mean().reset_index(0, drop= True)
    df['negativer']=df.groupby('state')['negativec'].rolling(
        window=3).mean().reset_index(0, drop= True)
    df['hospitalizedCurrentlyr']=df.groupby('state')['hospitalizedCurrentlyc'].rolling(
        window=3).mean().reset_index(0, drop= True)

    df = (df.set_index('date', drop=True)
        .filter(["state", "positive", "negative","positiver", "negativer","positivec", "negativec", "hospitalizedCurrently", "hospitalizedCurrentlyr", "hospitalizedCurrentlyc", "probableCases"])
        )
    return df

def process_covidtracking_data(df, vars):
    print("Process covid: " + ",".join(vars))
    vars=list(set(vars) & set(["positive", "negative","positiver", "negativer","positivec", "hospitalizedCurrently", "hospitalizedCurrentlyr", "hospitalizedCurrentlyc","negativec", "probableCases"]))
    df=(df.reset_index()
            .melt(value_vars=vars, id_vars=["state", "date"])
            .query("variable in @vars")
          )
    print("Found records: ", len(df))
    return df



def read_cdc_data():
    df=pd.read_csv(
        "https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD&bom=true&format=true")
    return df


def prepare_cdc_data(raw_df, start_date, include_states):
    df=(raw_df.fillna(0)
          .rename(columns={'Excess Lower Estimate': 'excessl', 'Excess Higher Estimate': "excessh", 'Week Ending Date': 'date', 'State': 'state'}))
    df=float_convert(df, ["excessl", "excessh"])
    df=date_convert(df, ["date"])
    df['state']=map_states(df)
    df=(df.query("Outcome == 'All causes'")
          .query("Type == 'Predicted (weighted)'")
          .query("date > @start_date", engine='python')
          .query("state in @include_states")
          .set_index('date', drop=True)
          )
    return df


def process_cdc_data(df, include_variables):
    print("Process cdc: " + ",".join(include_variables))
    df=(df.pivot(columns='state', values=['excessl', 'excessh'])
            .resample('D')
            .interpolate(method='from_derivatives')
            .stack(level=1)
            .reset_index(level=1)
            .reset_index('date')
            .melt(id_vars=['date', 'state'])
            .query("variable in @include_variables")
          )
    print("Found records: ", len(df))
    return df


def read_nyt_data(start_date, include_states):
    states=pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv", parse_dates= True)
    states['state']=map_states(states)
    states=states.loc[(states['state'].isin(include_states))]
    usa=pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv", parse_dates= True)
    usa['state']="USA"
    if ("USA" in include_states):
        states =pd.concat([states, usa], sort = False)
    states=states.loc[states['date'] > start_date]
    return states


def process_nyt(df, include_variables):
    print("Process nyt: " + ",".join(include_variables))
    df =df.assign(deathsd = df.groupby('state')['deaths'].apply(doubling))
    df =df.assign(casesd = df.groupby('state')['cases'].apply(doubling))
    df =df.assign(casesc = df.groupby('state')['cases'].diff())
    df =df.assign(deathsc = df.groupby('state')['deaths'].diff())
    df['casesr']=df.groupby('state')['casesc'].rolling(
        7).mean().reset_index(0, drop= True)
    df['deathsr']=df.groupby('state')['deathsc'].rolling(
        7).mean().reset_index(0, drop= True)
    df['date']=pd.to_datetime(df['date'])
    df =df.melt(id_vars = ['date', 'state'])
    df=df[df.variable.isin(include_variables)]
    print("Found records: ", len(df))
    return df


def map_states(df):
    statesmap={"North Carolina": "NC",
                 "West Virginia": "WV",
                 "South Carolina": "SC",
                 "District of Columbia": "DC",
                 "Massachusetts": "MA",
                 "New Hampshire": "NH",
                 "Maine": "ME",
                 "Rhode Island": "RE",
                 "New York": "NY",
                 "Washington": "WA",
                 "New Jersey": "NJ",
                 "California": "CA",
                 "Texas": "TX",
                 "Florida": "FL",
                 "USA": "USA",
                 "Connecticut": "CT",
                 "Alabama": "AL",
                 "Arkansas": "AR",
                 "Vermont": "VT",
                 "Maine": "ME",
                 "Utah": "UT",
                 "Virginia": "VI",
                 "Illinois": "IL",
                 "Wisconsin": "WI",
                 "Wyoming": "WY",
                 "Kansas" : "KS",
                 "Oklahoma" : "OK",
                 "Arizona" : "AZ",
                 }
    return (df['state'].replace(statesmap))


def read_data(start_date, states, variables):
    nyt=read_nyt_data(start_date, states)
    nyt=process_nyt(nyt, variables)
    cdc_raw=read_cdc_data()
    cdc_prep=prepare_cdc_data(cdc_raw, start_date, states)
    cdc=process_cdc_data(cdc_prep, variables)
    cv_raw =read_covidtracking_data(start_date, states)
    cv_prep = prepare_covidtracking_data(cv_raw, start_date, states)
    cv = process_covidtracking_data(cv_prep, variables)
    res =pd.concat([cdc, nyt, cv], sort = False)
    return res


def doubling(indata):
    readings=indata.to_numpy()
    readingsLength=len(readings)
    double=np.zeros(readingsLength)
    double[:]=np.NaN
    for i in range(readingsLength - 1, -1, -1):
        target=readings[i]
        count=0
        for j in range(i, -1, -1):
            diffsofar=target-readings[j]
            exact=target / 2
            if diffsofar > exact:
                f=(exact - readings[j]) / (readings[j]-readings[j+1]) + count
                double[i]=f
                break
            else:
                count=count+1
    outdata=pd.Series(data= double, name = indata.name, index = indata.index)
    return outdata


# OLD STUFF
def read_cdc_data_used_to_be_1(start_date, include_states):
    df=(pd.read_csv("https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD&bom=true&format=true",
                    na_values = ['(NA)', ''], thousands = ',', parse_dates = ['Week Ending Date'])
        .fillna(0)
        .rename(columns = {'Excess Lower Estimate': 'excessl', 'Excess Higher Estimate': "excessh", 'Week Ending Date': 'date', 'State': 'state'}))

    df['state']=map_states(df)
    df=(df.query("Outcome == 'All causes'")
        .query("Type == 'Predicted (weighted)'")
        .query("date > '" + start_date + "'")
        .assign(state = lambda x: map_states(x))
        .query("state in @include_states")
        .set_index('date', drop=True)
        )
    return

def read_cdc_data_org(include_states, start_date):
    dt=(pd.read_csv("https://data.cdc.gov/api/views/xkkf-xrst/rows.csv?accessType=DOWNLOAD&bom=true&format=true",
                    na_values = ['(NA)', ''], thousands = ',', parse_dates = ['Week Ending Date']).fillna(0)
        .query("Outcome == 'All causes'")
        .query("Type == 'Predicted (weighted)'")
        .rename(columns = {'Excess Lower Estimate': 'excessl', 'Excess Higher Estimate': "excessh", 'Week Ending Date': 'date', 'State': 'state'})
        .query("date > @start_date")
        .query("state in @include_states")
        .set_index('date', drop = True)
            )
    return dt
