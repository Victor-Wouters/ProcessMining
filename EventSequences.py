import pm4py
import pandas as pd
import numpy as np

def filter_activity(event_log, transactions):
    settle_after_unsettled= pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled", "...","Settling"]], positive=True)

    queue_unsettled=pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled", "..."]], positive=True)
    number_settle_after_unsettled=len(settle_after_unsettled.case_id.unique())
    number_queue_unsettled=len(queue_unsettled.case_id.unique())
    ratio=number_settle_after_unsettled/number_queue_unsettled
    id_settle_after_unsettled=settle_after_unsettled.case_id.unique()


    
    print("number of cases queue unsettled: ",number_queue_unsettled)
    print("number of cases settle after unsettled: ",number_settle_after_unsettled)
    print("ratio: ",ratio)
    
    transaction_ids = [int(tid) for tid in id_settle_after_unsettled]
    filtered_transactions = transactions[transactions['TID'].isin(transaction_ids)]


    print("transactions that settled after being unsettled:",filtered_transactions)
    mean_value = filtered_transactions['Value'].mean()
    print("mean value of all the transactions that settle after being unsettled:" ,mean_value)
    total_value = transactions['Value'].sum()
    print("value ratio:", filtered_transactions['Value'].sum()/total_value)
    return 




