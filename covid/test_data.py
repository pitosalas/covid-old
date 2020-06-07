import pandas as pd
import data as data
from datetime import datetime

class TestData:

    def setup(self):
        self.nyt = pd.DataFrame({"date": ["2020-01-01", "2020-01-01", "2020-01-02", "2020-01-02",
                                          "2020-01-03", "2020-01-03", "2020-01-04", "2020-01-04"],
                                 "state": ["A", "B", "A", "B", "A", "B", "A", "B"],
                                 "cases": [10,  30,   20,  50,  30,  70,  40, 100],
                                 "deaths": [1,   3,    2,   6,   5,   25, 10,  30]})
        self.cdc = pd.DataFrame({"Week Ending Date": ["2020-05-01", "2020-05-01", "2020-05-08", "2020-05-08", "2020-05-15", "2020-05-15", "2020-05-22", "2020-05-22"],
                                 "state": ["Florida", "Utah", "Florida", "Utah", "Florida", "Utah", "Florida", "Utah"],
                                 "Excess Lower Estimate": ["10,000",  "30,000",   "20,000",  "50,000",  "30,000",  "70,000",  "40,000", "100,000"],
                                 "Excess Higher Estimate": ["1",   "3",    "2",   "6",   "5",   "25", "10",  "30"],
                                 "Type": ["Predicted (weighted)", "Predicted (weighted)", "Predicted (weighted)", "Predicted (weighted)", "Predicted (weighted)", "Predicted (weighted)", "Predicted (weighted)", "Predicted (weighted)"],
                                 "Outcome": ["All causes", "All causes", "All causes", "All causes", "All causes", "All causes", "All causes", "All causes", ]})
        self.covid = pd.DataFrame({"date": ["20200401", "20200402", "20200403", "20200401", "20200402", "20200403"],
                                   "state": ["MA","MA","MA","FL","FL", "FL"],
                                   "positive": [100, 120, 130, 1000, 1100, 1200],
                                   "negative": [1000, 1200, 1300, 10000,10100,10200]})

    def test_prepare_covid_data(self):
        states = ["MA"]
        sd = "2020/03/30"
        df = data.prepare_covidtracking_data(self.covid, sd, states)
        assert(df.shape[0] == 3)

    def test_compute_covid_data(self):
        states = ["MA"]
        sd = "2020/03/30"
        vars = ["positive"]
        df_prep = data.prepare_covidtracking_data(self.covid, sd, states)
        df_processed = data.process_covidtracking_data(df_prep, vars)
        assert df_processed.shape[0] == 3

    def test_prepare_cdc_data(self):
        states = ["UT"]
        sd = "2020/03/30"
        df = data.prepare_cdc_data(self.cdc, sd, states)
        assert(df.shape[0] == 4)

    def test_compute_cdc_data(self):
        states = ["UT"]
        variables = ["excessh"]
        sd = datetime.strptime("2020/05/01", "%Y/%m/%d")
        df1 = data.prepare_cdc_data(self.cdc, sd, states)
        df2 = data.process_cdc_data(df1, variables)
        assert df2.shape[1] == 4 and df2.dtypes[0] == '<M8[ns]'

    def test_full_cdc(self):
        states = ["UT"]
        variabs = ["excessh"]
        sd = "2020/04/30"
        cdc_raw = data.read_cdc_data()
        cdc_prep = data.prepare_cdc_data(cdc_raw, sd, states)
        cdc_processed = data.process_cdc_data(cdc_prep, variabs)
        assert cdc_processed.shape[0] == 15 and cdc_processed.shape[1]==4

    def test_old_model(self):
        sd = "2020-03-01"
        states = ["Massachusetts"]
        vars = ["excessh"]
        dt1 = data.read_cdc_data_org(states, sd)
        dt2 = data.process_cdc_data(dt1, vars)
        assert dt2.shape[0] > 20 and dt2.shape[1] == 4

    def test_float_convert(self):
        df = pd.DataFrame({"x": ["1,000", "2.3"], "z": [
                          "a", "v"], "y": ["3,000", "30"]})
        data.float_convert(df, ["x", "y"])
        assert df.dtypes[0] == float

    def test_covid_data_calcs(self):
        states = ["MA"]
        sd = "2020/03/30"
        vars = ["positive", "positivec", "positiver"]
        df_prep = data.prepare_covidtracking_data(self.covid, sd, states)
        df_processed = data.process_covidtracking_data(df_prep, vars)
        assert df_processed.shape == (9, 4)

