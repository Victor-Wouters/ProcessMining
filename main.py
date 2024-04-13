import pandas as pd
import pm4py
import ImportData
import ActivitiesStats
import BPMN
import Visuals
import EventlogDescription
import EventSequences
import KPIVisuals
import remove_warmup
import join_files
import VisualizeSenderReceiver
import time_dimension

if __name__ == "__main__":
    event_log_df= pd.read_csv('data/eventlog.csv', sep=';')
    transactions = pd.read_csv('data/TRANSACTION1.csv', sep=';')
    event_log_joined=join_files.join_eventlog_transactions(event_log_df, transactions)
    event_log=ImportData.read_in_data('JoinedLog.csv')
    event_log=remove_warmup.remove_warmup_cooldown(event_log, warmup_days=2, cooldown_days=0)
    print(event_log)
    time_dimension.days_after_deadline(event_log)

    
    ActivitiesStats.activities(event_log)
    BPMN.process_tree_to_BPMN(event_log)
    BPMN.inductive_miner_algorithm(event_log)
    Visuals.process_tree(event_log)
    Visuals.process_map_DFG_algorithm(event_log)
    Visuals.process_map_Heuristics_Miner(event_log)
    VisualizeSenderReceiver.visualize_sender_receiver(event_log)
    EventlogDescription.log_statistics(event_log)
    KPIVisuals.settlements_graph(event_log)
    #KPIVisuals.histogram_val_match_sett(event_log)
    #KPIVisuals.histogram_val_match_sett_30(event_log)
    KPIVisuals.histogram_val_match_sett_uneven(event_log)
    KPIVisuals.per_day(event_log)
    KPIVisuals.histogram_failed_to_settle(event_log)
    KPIVisuals.over_deadline(event_log)
    KPIVisuals.deadline_violated_cases_day(event_log)
    
    time_dimension.days_after_deadline_hour(event_log)

    
    


 







   