import pm4py

def process_tree(event_log):
    process_tree = pm4py.discover_process_tree_inductive(event_log)
    pm4py.view_process_tree(process_tree)
    return

def process_map_DFG_algorithm(event_log):
    dfg, start_activities, end_activities = pm4py.discover_dfg(event_log)
    pm4py.view_dfg(dfg, start_activities, end_activities)
    return

def process_map_Heuristics_Miner(event_log):
    map = pm4py.discover_heuristics_net(event_log)
    pm4py.view_heuristics_net(map)
    return