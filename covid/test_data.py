import pandas as pd
import data
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
        self.states = ["UT"]
        self.vars = ["excessh"]
        self.sd = datetime.strptime("2020/04/30","%Y/%m/%d")
        #self.sd = "2020-05-02"

    def test_prepare_cdc_data(self):
        df = data.prepare_cdc_data(self.cdc, self.sd, self.states)
        assert(df.shape[0] == 2)

    def test_compute_cdc_data(self):
        df = data.prepare_cdc_data(self.cdc, self.sd, self.states)
        df1 = df.astype({'excessh':'float'})
        df2 = data.process_cdc_data(df1, self.vars)
        assert 1==1

    def test_full_cdc(self):
        cdc_raw = data.read_cdc_data()
        cdc_prep = data.prepare_cdc_data(cdc_raw, self.sd, self.states)
        cdc = data.process_cdc_data(cdc_prep, self.vars)

    def test_old_model(self):
        sd = "2020/05/01"
        df = data.read_cdc_data1(sd, self.states)
        df = data.process_cdc_data(df, self.vars)
        assert 1==1




