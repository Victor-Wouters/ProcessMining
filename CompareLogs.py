import pandas as pd

# Assuming df1 and df2 are your DataFrames representing the two event logs

specific_activity = 'Matching'

# Step 1: Filter for the specific activity in both DataFrames
filtered_df1 = event_log[event_log['concept:name'] == specific_activity]
filtered_df2 = event_log1[event_log1['concept:name'] == specific_activity]

# Step 2: Extract unique case IDs for the specific activity from both DataFrames
case_ids_log1 = set(filtered_df1['case_id'].unique())
case_ids_log2 = set(filtered_df2['case_id'].unique())

# Step 3: Compare the sets of case IDs
only_in_log1 = case_ids_log1 - case_ids_log2
only_in_log2 = case_ids_log2 - case_ids_log1
common_to_both_logs = case_ids_log1 & case_ids_log2

# Print the results
print(f"Case IDs only in log 1 for activity '{specific_activity}':", only_in_log1)
print(f"Case IDs only in log 2 for activity '{specific_activity}':", only_in_log2)
#print(f"Case IDs in both logs for activity '{specific_activity}':", common_to_both_logs)
# Assuming 'df' is your DataFrame representing the event log

for i in [4263,447]:
    case_id_to_print = i  # Change this to the case ID you want to print the trace for

    # Filter the DataFrame for the specified case ID
    filtered_trace = event_log1[event_log1['case:concept:name'] == str(case_id_to_print)]

    # Optionally, sort by 'time:timestamp' if you want to ensure chronological order
    filtered_trace_sorted = filtered_trace.sort_values(by='time:timestamp')

    # Print the trace
    print(filtered_trace_sorted)