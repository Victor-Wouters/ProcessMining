import pm4py
import pandas as pd
import pm4py
from pm4py.objects.conversion.log import converter as log_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.conformance.tokenreplay import algorithm as token_replay
from pm4py.visualization.petri_net import visualizer as pn_visualizer


def conformance_check(event_log):
# Ensure that the 'Starttime' or your timestamp column is in datetime format
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    
    # Configuring the parameters for conversion
    parameters = {
        "case_id_glue": "case_id",   # Adjust 'case_id' to the column name in your DataFrame that serves as case ID.
        "timestamp_key": "Starttime",  # Adjust 'Starttime' to the column name in your DataFrame that serves as the timestamp.
        "activity_key": "Activity"  # Adjust 'Activity' to the column name for the activity.
    }
    # Convert DataFrame to Event Log
    event_log = log_converter.apply(event_log, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)


    # Discovering a process model using the Alpha Miner
    net, initial_marking, final_marking = alpha_miner.apply(event_log)

    # Perform token-based replay conformance checking
    replayed_traces = token_replay.apply(event_log, net, initial_marking, final_marking)

    # Print results or perform further analysis
    print("Model discovered and conformance checked.")
    gviz = pn_visualizer.apply(net, initial_marking, final_marking)
    pn_visualizer.view(gviz)

    #Let's assume replayed_traces contains your results from token replay
    for trace_index, trace_result in enumerate(replayed_traces):
        print(f"Trace {trace_index + 1}:")
        print(f"  Trace is fit: {trace_result['trace_is_fit']}")
        print(f"  Consumed tokens: {trace_result['consumed_tokens']}")
        print(f"  Produced tokens: {trace_result['produced_tokens']}")
        print(f"  Missing tokens: {trace_result['missing_tokens']}")
        print(f"  Remaining tokens: {trace_result['remaining_tokens']}")
        print(f"  Trace fitness: {trace_result['trace_fitness']}")

    #Calculate overall fitness from replayed traces
    total_fitness = sum(trace['trace_fitness'] for trace in replayed_traces) / len(replayed_traces)
    print(f"Overall fitness of the process model: {total_fitness:.2f}")