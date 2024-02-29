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
    avg_length = round(np.mean([len(key) for key in variants.keys()]))
    max_duration= max(pm4py.stats.get_case_duration(str(case)) for case in range(0, len(event_log)))


    
    data = {
        'Start Activities': list(start),
        'End Activities': list(end),
        'Max Length': [max_length],
        'Min Length': [min_length],
        'Avg Length': [avg_length],
        'max_duration':[max_duration]
    }

    print(data)
    
    max_length_trace = [variant for variant in variants.keys() if len(variant) == max_length]
    
    if max_length_trace:
        print("\nTrace(s) with the maximum length:")
        for trace in max_length_trace:
            print(trace)
    
    min_length_trace = [variant for variant in variants.keys() if len(variant) == min_length]
    
    if min_length_trace:
        print("\nTrace(s) with the maximum length:")
        for trace in min_length_trace:
            print(trace)

    return