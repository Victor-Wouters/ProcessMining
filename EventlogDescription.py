import pm4py
import pandas as pd
import numpy as np

# Discover traces in the event log
def log_statistics(event_log):
    variants = pm4py.get_variants(event_log)
    dsit_traces=len(variants.keys())
    num_events=len(event_log)
    dist_events=len(set(event_log['Activity']))
    dist_traces=len(set(variants.keys()))
    num_cases = len(event_log.case_id.unique())
    start=pm4py.get_start_activities(event_log)
    end=pm4py.get_end_activities(event_log)
    max_length = max(len(key) for key in variants.keys())
    min_length=min(len(key) for key in variants.keys())
    avg_length = round(np.mean([len(key) for key in variants.keys()]))
    std_length=np.std(np.array([len(key) for key in variants.keys()])) 
    case_durations=pm4py.get_all_case_durations(event_log)
    max_duration=max(case_durations)/3600
    min_duration=min(case_durations)
    avg_duration=np.mean(case_durations)/3600
    std_duration = np.sqrt(np.var(case_durations)) / 3600

   
   
    

    
    data = {
        'Start Activities': list(start),
        'End Activities': list(end),
        'Max Length': [max_length],
        'Min Length': [min_length],
        'Avg Length': [avg_length],
        'Std Length': [std_length],
        'Number of distinct traces': [dist_traces],
        'Number of events': [num_events],
        'Number of distinct events': [dist_events],
        'Number of cases': [num_cases],
        'Max_duration (in hours)':[max_duration],
        'Min_duration (in seconds)':[min_duration],
        'Avg_duration (in hours)':[avg_duration],
        'Std_duration (in hours)':[std_duration]

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