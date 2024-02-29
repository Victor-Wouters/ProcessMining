import pm4py
import pandas as pd
import numpy as np

# Discover traces in the event log
def log_statistics(event_log):
    variants = pm4py.get_variants(event_log)
    start=pm4py.get_start_activities(event_log)
    end=pm4py.get_end_activities(event_log)
    max_length = max(len(key) for key in variants.keys())
    min_length=min(len(key) for key in variants.keys())
    
    data = {
        'Start Activities': list(start),
        'End Activities': list(end),
        'Max Length': [max_length],
        'Min Length': [min_length]
    }

    print(data)
