import data
import graph
import argparse
import sys

def command_parser():
    parser = argparse.ArgumentParser(description='Generate COVID graphs')
    parser.add_argument("filename", action="store")
    parser.add_argument("--states", nargs="+", type=str)
    parser.add_argument("--vars", nargs="+", type=str)
    print(sys.argv)
    if len(sys.argv) == 1:
        args = parser.parse_args('testout --states ak al --vars  excessl deathsr'.split())
    else:
        args = parser.parse_args()
    return args

def print_spec(states, variables, date, filename, dimensions):
    states_s = ', '.join(str(x) for x in states)
    variables_s = ', '.join(str(x) for x in variables)
    print("Graph start date: ", date, "- for ", states_s, "- showing ", variables_s)

def report_row(df, states, variables, date, filename, dimensions):
    print_spec(states, variables, date, filename, dimensions)
    graph.graph_b(df, states, variables, filename, dimensions)

def doit():
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
                "usa" : "USA",
                "al" : "Alabama",
                "ak" : "Arkansas"
                }
    args = command_parser()
    states = list(map(lambda state: statesmap[state], args.states))
    variables = args.vars
    startdate = "2020-03-01"
    dim = [4, 2.5]
    df = data.read_data(startdate, states, variables)
    print_spec(states, variables, startdate, args.filename, dim)
    graph.graph_b(df, states, variables, args.filename, dim)

doit()