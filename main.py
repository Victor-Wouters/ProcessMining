import pandas as pd
import pm4py
import ImportData
import ActivitiesStats
import BPMN
import Visuals
import EventlogDescription
import EventSequences
import KPIVisuals

if __name__ == "__main__":
    event_log_df= pd.read_csv('data\eventlogweek.csv', sep=';')
    event_log = ImportData.read_in_data('data\eventlogweek.csv')
    transactions = pd.read_csv('data\TRANSACTION1.csv', sep=';')
    #print(event_log)
    ActivitiesStats.activities(event_log)
    BPMN.process_tree_to_BPMN(event_log)
    BPMN.inductive_miner_algorithm(event_log)
    Visuals.process_tree(event_log)
    Visuals.process_map_DFG_algorithm(event_log)
    Visuals.process_map_Heuristics_Miner(event_log)
    EventlogDescription.log_statistics(event_log)
    #EventSequences.filter_activity(event_log, transactions)
    KPIVisuals.settlements_graph(event_log_df)
    KPIVisuals.histogram_val_match_sett(event_log_df)
    #KPIVisuals.histogram_unsettled(event_log, event_log_df)
    #KPIVisuals.settlement_efficiency_participant(event_log,transactions)
    KPIVisuals.number_transactions_settled_unsettled(event_log)
    KPIVisuals.value_transactions_settled_unsettled(event_log, transactions)
    #KPIVisuals.settlement_efficiency_over_time(event_log, transactions)







   