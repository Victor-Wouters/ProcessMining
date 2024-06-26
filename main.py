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
import conformancecheck

if __name__ == "__main__":
    event_log_df= pd.read_csv('data/T+0_GW/eventlog.csv', sep=';')
    transactions = pd.read_csv('data/T+0_GW/TRANSACTION1.csv', sep=';')
    #participants = pd.read_csv('data/T+0_NO_GW/PARTICIPANTS1.csv', sep=';')
    event_log_joined=join_files.join_eventlog_transactions(event_log_df, transactions)
    event_log=ImportData.read_in_data('JoinedLog.csv')
    #event_log_part_tran=join_files.join_merged_event_log_participants(event_log, participants)
    event_log=remove_warmup.remove_warmup_cooldown(event_log, warmup_days=1, cooldown_days=0)
    print(event_log)

    
    #Visuals.process_map_Heuristics_Miner(event_log)
    # VisualizeSenderReceiver.visualize_sender_receiver(event_log)
    #VisualizeSenderReceiver.visualize_sender_receiver_value(event_log)
    #KPIVisuals.view(event_log)
    
    
    
    # ActivitiesStats.activities(event_log)
    # BPMN.process_tree_to_BPMN(event_log)
    # BPMN.inductive_miner_algorithm(event_log)
    # Visuals.process_tree(event_log)
    
    # Visuals.process_map_Heuristics_Miner(event_log)
    # VisualizeSenderReceiver.visualize_sender_receiver(event_log)
    # EventlogDescription.log_statistics(event_log)
    #KPIVisuals.histogram_val_match_sett(event_log)
    #KPIVisuals.histogram_val_match_sett_30(event_log)
    # KPIVisuals.settlements_graph(event_log)
    # KPIVisuals.histogram_val_match_sett_uneven(event_log)
    # KPIVisuals.per_day(event_log)
    # KPIVisuals.histogram_failed_to_settle_value(event_log)
    # KPIVisuals.histogram_failed_to_settle(event_log)
    # KPIVisuals.histogram_failed_to_settle(event_log)
    # KPIVisuals.over_deadline_activites(event_log)
    # KPIVisuals.over_deadline_settlements(event_log)
    time_dimension.days_after_deadline_hour(event_log)
    #time_dimension.duration_and_case_count(event_log)
    #time_dimension.days_after_deadline(event_log)
    #time_dimension.calculate_avg_duration_between_validating_settling(event_log)
    #time_dimension.calculate_avg_duration_between_start_and_end_backlog(event_log)
    #time_dimension.calculate_trace_counts(event_log)
    #time_dimension.days_after_deadline(event_log)
    #conformancecheck.conformance_check(event_log)
    
   

  




    
    

    
    


 







   