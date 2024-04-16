import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import locale
import datetime as dt
import time
import Visuals
import math
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter
from datetime import time


def time_tests(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    for date in unique_dates:
        event_log_day=event_log[event_log['Starttime'].dt.date==date]
        arrival_rate_day=pm4py.stats.get_case_arrival_average(event_log_day)
        case_duration=pm4py.stats.get_all_case_durations(event_log_day)
        print(date)
        print("average case duration full log (in hours?):",np.mean(case_duration)/3600)
        
        print("Average time in minutes between 2 cases:",arrival_rate_day/60)
    case_duration=pm4py.stats.get_all_case_durations(event_log)
    print("complete log:")
    print("average case duration full log (in hours?):",np.mean(case_duration)/3600)


def days_after_deadline(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    #transactions['SettlementDeadline'] = transactions['SettlementDeadline'].dt.date
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])
    # Get unique dates
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    violations=dict()
    settled=dict()
    ratio=dict()
   
    for date in unique_dates:
        #print(date)
        settled_cases=event_log[event_log["Activity"]=="Settling"]
        deadline_violated=settled_cases[settled_cases["Starttime"].dt.date>settled_cases["SettlementDeadline"].dt.date]
        #print(deadline_violated)

        deadline_violated_day=deadline_violated[deadline_violated["Starttime"].dt.date==date]
        
        deadline_violated_day['number_of_days_over_deadline'] = (deadline_violated_day['Starttime'].dt.day - deadline_violated_day['SettlementDeadline'].dt.day)
        count_over_deadline = deadline_violated_day.groupby('number_of_days_over_deadline').size()
        max_days = 4
        days_counts = {f"{i}": count_over_deadline.get(i, 0) for i in range(1, max_days+1)}
        violations[date]=days_counts
     

        # Print the counts
        for days, count in days_counts.items():
            print(f"{date}, {count} times {days}")
    num_cols = 2
    num_rows = 2
    dates = list(violations.keys())[:4]


    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 8))
    fontsize1=15
    fontsize2=13
  

    # Plotting
    for idx, (date, ax) in enumerate(zip(dates, axes.flatten())):
        counts = violations[date]
        bars = ax.bar(counts.keys(), counts.values())
        ax.set_title(f"Number Of Days Settled After Deadline {date}",fontsize=fontsize1)
        ax.set_xlabel('Number Of Days Settled After Deadline', fontsize=fontsize1)
        ax.set_ylabel('Counts',fontsize=fontsize1)
        
        # Adding labels to bars with counts greater than 0
        for bar, count in zip(bars, counts.values()):
            if count > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom',fontsize=fontsize2)

    plt.tight_layout()
    plt.show()
    
    return

def days_after_deadline_hour(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    #transactions['SettlementDeadline'] = transactions['SettlementDeadline'].dt.date
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])
    desired_time = pd.to_datetime("19:30:00").time()
    event_log['SettlementDeadline'] = event_log['SettlementDeadline'].apply(lambda x: pd.Timestamp.combine(x.date(), desired_time))
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])
   
    #print(date)
    settled_cases=event_log[event_log["Activity"]=="Settling"]
    deadline_violated=settled_cases[settled_cases["Starttime"].dt.date>settled_cases["SettlementDeadline"].dt.date]
    deadline_violated['Starttime'] = deadline_violated['Starttime'].dt.tz_localize(None)
    deadline_violated['SettlementDeadline'] = deadline_violated['SettlementDeadline'].dt.tz_localize(None)
    #print(deadline_violated)
  
    deadline_violated['number_of_hours_over_deadline'] = (deadline_violated['Starttime'] - deadline_violated['SettlementDeadline']).dt.total_seconds() / 3600
    deadline_violated['number_of_hours_over_deadline'] = deadline_violated['number_of_hours_over_deadline'].apply(math.ceil)
    print(deadline_violated)
    deadline_violated.to_csv('deadline_violations.csv', index=False)

    print(deadline_violated['number_of_hours_over_deadline'])
    count_over_deadline = deadline_violated.groupby('number_of_hours_over_deadline').size()
    max_hours = 120
    hours_counts = {f"{i}": count_over_deadline.get(i, 0) for i in range(1, max_hours+1)}

    # Print the counts
    for days, count in hours_counts.items():
        print(f" {count} times {days}")
        
    fontsize1=15
    fontsize2=13
    plt.figure(figsize=(15, 8))
    bars=plt.bar(hours_counts.keys(), hours_counts.values(), color='skyblue')
    for bar, count in zip(bars, hours_counts.values()):
        if count != 0:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, '%d' % int(height), ha='center', va='bottom', fontsize=fontsize2)


    plt.xlabel('Hours Settled Over Deadline', fontsize=fontsize1)
    plt.ylabel('Frequency',fontsize=fontsize1)
    plt.title('Frequency Of Hours Settled After Deadline',fontsize=fontsize1)
    plt.xticks(rotation=45,fontsize=fontsize1)
    plt.xticks(range(0, max_hours, 5),fontsize=fontsize1) 
    plt.yticks(fontsize=fontsize1)
    plt.tight_layout()
    plt.show()

    return

def calculate_avg_duration_between_validating_settling(event_log):
    # Convert to datetime if necessary
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Filter the log to include only the activities of interest
    filtered_log = event_log[event_log['Activity'].isin(['Validating', 'Settling'])]

    # Group by case_id and filter out cases that don't have both activities
    grouped = filtered_log.groupby('case_id')
    
    durations = []  # This will store the duration in hours between 'Validating' and 'Settling' for each case
    
    for case_id, group in grouped:
        if 'Validating' in group['Activity'].values and 'Settling' in group['Activity'].values:
            # Get the minimum start time for 'Validating' and 'Settling'
            validating_time = group[group['Activity'] == 'Validating']['Starttime'].min()
            settling_time = group[group['Activity'] == 'Settling']['Starttime'].min()

            if pd.notnull(validating_time) and pd.notnull(settling_time) and settling_time > validating_time:
                duration = (settling_time - validating_time).total_seconds() / 3600  # Duration in hours
                durations.append(duration)

    # Calculate the average duration if any durations were calculated
    if durations:
        avg_duration = sum(durations) / len(durations)
        print(f"Average duration between 'Validating' and 'Settling' in hours: {avg_duration}")
    else:
        print("No valid cases with both 'Validating' and 'Settling' were found.")

def calculate_avg_duration_between_start_and_end(event_log):
    # Ensure datetime format is correct and sorted
    event_log = dataframe_utils.convert_timestamp_columns_in_df(event_log)
    event_log = event_log.sort_values('Starttime')

    # Convert the DataFrame to an event log
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case_id'}
    log = log_converter.apply(event_log, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

    # Filter traces and calculate durations
    durations = []
    for trace in log:
        if trace and trace[0]['concept:name'] == 'Validating':  # Start activity must be 'Validating'
            if trace[-1]['concept:name'] in ['Settling', 'Waiting in backlog for recycling']:  # Check the last event specifically
                start_time = trace[0]['time:timestamp']
                end_time = trace[-1]['time:timestamp']
                if end_time > start_time:  # Ensure the end event is after the start event
                    duration = (end_time - start_time).total_seconds()
                    durations.append(duration)

    # Compute the average duration in minutes
    if durations:
        avg_duration = np.mean(durations) / 3600  # Convert seconds to minutes
        print(f"Average duration between 'Validating' and last event in hours: {avg_duration:.2f}")
    else:
        print("No valid cases were found that start with 'Validating' and end with 'Settling' or 'Waiting in backlog for recycling'.")

def calculate_trace_counts(event_log):
    # Ensure datetime format is correct and sorted
    event_log = dataframe_utils.convert_timestamp_columns_in_df(event_log)
    event_log = event_log.sort_values('Starttime')

    # Convert the DataFrame to an event log
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case_id'}
    log = log_converter.apply(event_log, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

    count_validating_to_settling = 0
    count_validating_to_waiting = 0

    # Iterate through each trace in the log
    for trace in log:
        if trace and trace[0]['concept:name'] == 'Validating':  # Start activity must be 'Validating'
            if trace[-1]['concept:name'] == 'Settling':
                count_validating_to_settling += 1
            elif trace[-1]['concept:name'] == 'Waiting in backlog for recycling':
                count_validating_to_waiting += 1

    # Print out the results
    print(f"Count of traces starting with 'Validating' and ending with 'Settling': {count_validating_to_settling}")
    print(f"Count of traces starting with 'Validating' and ending with 'Waiting in backlog for recycling': {count_validating_to_waiting}")

def calculate_avg_duration_between_start_and_end_backlog(event_log):
    # Ensure datetime format is correct and sorted
    event_log = dataframe_utils.convert_timestamp_columns_in_df(event_log)
    event_log = event_log.sort_values('Starttime')

    # Convert the DataFrame to an event log
    parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'case_id'}
    log = log_converter.apply(event_log, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)

    # Filter traces and calculate durations
    durations = []
    for trace in log:
        if trace and trace[0]['concept:name'] == 'Validating':  # Start activity must be 'Validating'
            if trace[-1]['concept:name'] in ['Waiting in backlog for recycling']:  # Check the last event specifically
                start_time = trace[0]['time:timestamp']
                end_time = trace[-1]['time:timestamp']
                if end_time > start_time:  # Ensure the end event is after the start event
                    duration = (end_time - start_time).total_seconds()
                    durations.append(duration)

    # Compute the average duration in minutes
    if durations:
        avg_duration = np.mean(durations) / 3600  # Convert seconds to minutes
        print(f"Average duration between 'Validating' and 'Waiting in backlog unsettled' in hours: {avg_duration:.2f}")
    else:
        print("No valid cases were found that start with 'Validating' and end with 'Settling' or 'Waiting in backlog for recycling'.")
    return

def duration_and_case_count(event_log):
    settling_end = pm4py.filter_trace_segments(event_log, [["Validating", "...", "Settling"]], positive=True)
    unsettling_end = pm4py.filter_trace_segments(event_log, [["Validating", "...", "Waiting in backlog for recycling"]], positive=True)
    duration_settling=pm4py.stats.get_all_case_durations(settling_end)
    duration_unsettling=pm4py.stats.get_all_case_durations(unsettling_end)

    print("average case duration for validating... settling (in hours):",round(np.mean(duration_settling)/3600,2))
    print("number of cases:", len(settling_end.case_id.unique()))
    print("average case duration for validating... backlog unsettled (in hours):",round(np.mean(duration_unsettling)/3600,2))
    print("number of cases:", len(unsettling_end.case_id.unique()))
    return

def rtp_vs_batch(event_log):
    opening_time = time(1, 30)
    closing_time=time(19, 30)
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    avg_rtp_ratio=0
    avg_batch_ratio=0
    for date in unique_dates:
        event_log_day=event_log[event_log['Starttime'].dt.date==date]
        event_log_day_settling=event_log_day[event_log_day['Activity']=="Settling"]
        #print(event_log_day_settling)
        
        settlements=event_log_day_settling["Value"]
        rtp_settlements=event_log_day_settling["Value"][(event_log_day_settling["Starttime"].dt.time>opening_time) & (event_log_day_settling["Starttime"].dt.time<closing_time)]
        batch_settlements=event_log_day_settling["Value"][event_log_day_settling["Starttime"].dt.time>closing_time]

        rtp_value = rtp_settlements.sum()
        batch_value=batch_settlements.sum()
        settlement_value=settlements.sum()
        avg_rtp_ratio+=rtp_value/settlement_value
        avg_batch_ratio+=batch_value/settlement_value

        print(date)
        print("rtp value on this day:", rtp_value)
        print("batch value on this day (from previous day):", batch_value)
        print("ratio (rtp/batch):", round(rtp_value/batch_value,2))
        print("ratio rtp/total settled", round(rtp_value/settlement_value,2))
        print("ratio batch/total settled", round(batch_value/settlement_value,2))
        print()
    print("average RTP ratio over all the days:", round(avg_rtp_ratio/len(unique_dates),4)*100)
    print("average batch ratio over all the days:", round(avg_batch_ratio/len(unique_dates),4)*100)

    return