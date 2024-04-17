import pm4py
import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import locale
import datetime
import time
import Visuals
from datetime import time
from datetime import timedelta
from datetime import datetime, time

def process_tree(event_log):
    process_tree = pm4py.discover_process_tree_inductive(event_log)
    pm4py.view_process_tree(process_tree)
    return

def process_map_DFG_algorithm(event_log):
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
    pm4py.view_dfg(dfg, start_activities, end_activities)
    return



def process_map_Heuristics_Miner(event_log):
    event_log2=filter_log(event_log)
    map = pm4py.discover_heuristics_net(event_log2)
    pm4py.view_heuristics_net(map)
    return

def filter_log(event_log):
    opening_time = time(22, 00)
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    event_log['Endtime'] = pd.to_datetime(event_log['Endtime'])

    # Determine the start datetime for the analysis
    start_date = event_log['Starttime'].min().floor('D')  # Start from the first day
    print(start_date)
    start_datetime = datetime.combine(start_date, opening_time)
    start_datetime_utc = pd.Timestamp(start_datetime).tz_localize('UTC')
    print(start_datetime)

    # Filter the DataFrame to include entries from the first day starting from 10 PM onwards
    event_log = event_log[event_log["Starttime"] >= start_datetime_utc]
    print("log",event_log)
    return event_log