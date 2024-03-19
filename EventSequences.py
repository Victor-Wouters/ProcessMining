import pm4py
import pandas as pd
import numpy as np

def filter_activity(event_log):
    settle_after_unsettled= pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled", "...","Settling"]], positive=True)

    queue_unsettled=pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled", "..."]], positive=True)
    number_settle_after_unsettled=len(settle_after_unsettled.case_id.unique())
    number_queue_unsettled=len(queue_unsettled.case_id.unique())
    ratio=number_settle_after_unsettled/number_queue_unsettled
    
    print("number of cases queue unsettled: ",number_queue_unsettled)
    print("number of cases settle after unsettled: ",number_settle_after_unsettled)
    print("ratio: ",ratio)
    #print(settle_after_unsettled.case_id.unique())


    return 




