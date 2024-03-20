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
    event_log = ImportData.read_in_data('data\eventlog0.csv')
    transactions = pd.read_csv('data\TRANSACTION1.csv', sep=';')
    #print(event_log)
    #ActivitiesStats.activities(event_log)
    #BPMN.process_tree_to_BPMN(event_log)
    #BPMN.inductive_miner_algorithm(event_log)
    #Visuals.process_tree(event_log)
    #Visuals.process_map_DFG_algorithm(event_log)
    #Visuals.process_map_Heuristics_Miner(event_log)
    #EventlogDescription.log_statistics(event_log)
    #event_log1 = ImportData.read_in_data('data\eventlogtest3.csv')
    #EventSequences.filter_activity(event_log, transactions)
    KPIVisuals.transactions_over_time(event_log)
    KPIVisuals.histogram()







   