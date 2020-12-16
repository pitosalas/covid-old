import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import seaborn as sns
from scipy.interpolate import UnivariateSpline


def graph_b(df, states, variables, filename, ratio):
    sns.set()
    plt.style.use('seaborn-darkgrid')
    g = sns.FacetGrid(df, col="variable", hue='state', sharex=True,
                      col_order=variables, sharey=False, height=ratio[0], aspect=ratio[1])
    g = g.map(plt.plot, "date", "value", linewidth=3)
    # g.add_legend()
    labelmap = {"deathsd": "Deaths Doubling",
                "deaths": "Total Deaths",
                "positive": "Positive Tests",
                "negative": "Negative Tests",
                "positiver": "Positive Tests (rolling average)",
                "negativer": "Negative Tests (rolling average)",
                "positivec": "New Positive Tests",
                "negativec": "New Negative Tests",
                "cases": "Cases",
                "casesd": "Cases Doubling",
                "casesc": "New Cases",
                "deathsc": "New Deaths",
                "excessl": "Excess Deaths",
                "excessh": "Excess Deaths (h)",
                "deathsr": "New Deaths (rolling average)",
                "casesr": "New Cases (rolling average)",
                "hospitalizedCurrently": "Newly Hospitalized",
                "hospitalizedCurrentlyr": "Newly Hospitalized (rolling average)",
                "hospitalizedCurrentlyc": "Newly Hospitalized (change from yesterday)",
                "probableCases": "Probable Cases"}
    for i in range(len(variables)):
        g.axes[0, i].set_title(labelmap[variables[i]], fontsize=20)
        g.axes[0, i].legend(title_fontsize=25)
    xformatter = mdates.DateFormatter("%m/%d")
    xlocator = mdates.DayLocator(bymonthday=[1, 5, 10, 15, 20, 25])
    yformatter = ticker.FuncFormatter(lambda x, p: format(int(x), ','))
    [axis[0].xaxis.set_major_formatter(xformatter) for axis in g.axes]
    [axis[0].xaxis.set_major_locator(xlocator) for axis in g.axes]
    [axis[0].yaxis.set_major_formatter(yformatter) for axis in g.axes]
    plt.savefig(filename)

def curve_fit(x,y):
    s = UnivariateSpline(x, y, s=5)
    xs = np.linspace(0, len(x), len(x)*5)
    ys = s(xs)
    return (xs,ys)
