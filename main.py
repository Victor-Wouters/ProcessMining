import pandas as pd
import pm4py
import ImportData
import ActivitiesStats
import BPMN
import Visuals

if __name__ == "__main__":
    event_log = ImportData.read_in_data('data\eventlogtest.csv')
    print(event_log)
    ActivitiesStats.activities(event_log)
    BPMN.process_tree_to_BPMN(event_log)
    BPMN.inductive_miner_algorithm(event_log)
    Visuals.process_tree(event_log)
    Visuals.process_map_DFG_algorithm(event_log)
    Visuals.process_map_Heuristics_Miner(event_log)

