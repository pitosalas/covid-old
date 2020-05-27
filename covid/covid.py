import data
import graph
import argparse
import sys
import pandas as pd


def run_from_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def command_parser():
    parser = argparse.ArgumentParser(description='Generate COVID graphs')
    parser.add_argument("--states", nargs="+", type=str)
    parser.add_argument("-v", "--vars", nargs="+", type=str)
    parser.add_argument("-g", "--graph", nargs="+", type=str)
    parser.add_argument("-d", "--data", nargs="+", type=str)
    if len(sys.argv) == 1 or run_from_ipython():
        args = parser.parse_args(
            ' --data x --graph y --states ak al ma --vars  excessl deathsr'.split())
    else:
        args = parser.parse_args()
    return args


def print_spec(states, variables, date, filename, dimensions):
    states_s = ', '.join(str(x) for x in states)
    variables_s = ', '.join(str(x) for x in variables)
    print("Graph start date: ", date, "- for ",
          states_s, "- showing ", variables_s)


def doit():
    statesmap = {"nc": "North Carolina",
                 "wv": "West Virginia",
                 "sc": "South Carolina",
                 "dc": "District of Columbia",
                 "ma": "Massachusetts",
                 "nh": "New Hampshire",
                 "ny": "New York",
                 "wa": "Washington",
                 "nj": "New Jersey",
                 "ca": "California",
                 "tx": "Texas",
                 "fl": "Florida",
                 "usa": "USA",
                 "ct": "Connecticut",
                 "al": "Alabama",
                 "ak": "Arkansas",
                 "vt": "Vermont"
                 }
    args = command_parser()
    states = list(map(lambda state: statesmap[state], args.states))
    variables = args.vars
    datfilename = args.data[0] + ".csv"
    startdate = "2020-03-01"
    dim = [4, 2.5]
    if args.data and not args.graph:
        print("covid: saving data in " + datfilename)
        df = data.read_data(startdate, states, variables)
        df.to_csv(datfilename)
    if args.graph:
        graphfilename = args.graph[0]
        print("covid: generating graph from " +
              datfilename + " into " + graphfilename)
        df = (pd.read_csv(datfilename, parse_dates=['date'])
              .query("state in @states"))
        graph.graph_b(df, states, variables, graphfilename, dim)


doit()
