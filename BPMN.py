import pm4py

def process_tree_to_BPMN(event_log):
    #converts process tree into bpmn model
    process_tree = pm4py.discover_process_tree_inductive(event_log)
    bpmn_model1 = pm4py.convert_to_bpmn(process_tree)
    pm4py.view_bpmn(bpmn_model1)
    return

def inductive_miner_algorithm(event_log):
    bpmn_model2=pm4py.discovery.discover_bpmn_inductive(event_log)
    pm4py.view_bpmn(bpmn_model2)
    return