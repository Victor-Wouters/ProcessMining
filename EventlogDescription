import pm4py
import pandas as pd
import numpy as np

# Discover traces in the event log
def log_statistics(eventlog):
    variants = pm4py.get_variants(eventlog)
    start=pm4py.get_start_activities(event_log)
    end=pm4py.get_end_activities(event_log)
    max_length = max(len(key) for key in variants.keys())
    min_length=min(len(key) for key in variants.keys())
    print(f"number of variants:{len(variants)}, the start activities are: {start}, the end activities are: {end},max number of events per trace: {max_length}")

