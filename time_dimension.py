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
        print("average case duration (in hours?):",np.mean(case_duration)/3600)
        print("arrival rate of the day (cases per minute?):",arrival_rate_day/60)




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
        print(violations.keys())
        print(violations.values())

        # Print the counts
        for days, count in days_counts.items():
            print(f"{date}, {count} times {days}")
    num_cols = 2
    num_rows = 2
    dates = list(violations.keys())[:4]


    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 8))

    # Plotting
    for idx, (date, ax) in enumerate(zip(dates, axes.flatten())):
        counts = violations[date]
        bars = ax.bar(counts.keys(), counts.values())
        ax.set_title(f"number of days settled after deadline {date}")
        ax.set_xlabel('Keys')
        ax.set_ylabel('Counts')

        # Adding labels to bars with counts greater than 0
        for bar, count in zip(bars, counts.values()):
            if count > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom')

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
    print(event_log['SettlementDeadline'])
   
    #print(date)
    settled_cases=event_log[event_log["Activity"]=="Settling"]
    deadline_violated=settled_cases[settled_cases["Starttime"].dt.date>settled_cases["SettlementDeadline"].dt.date]
    deadline_violated['Starttime'] = deadline_violated['Starttime'].dt.tz_localize(None)
    deadline_violated['SettlementDeadline'] = deadline_violated['SettlementDeadline'].dt.tz_localize(None)
    #print(deadline_violated)
  
    deadline_violated['number_of_hours_over_deadline'] = (deadline_violated['Starttime'] - deadline_violated['SettlementDeadline']).dt.total_seconds() / 3600
    deadline_violated['number_of_hours_over_deadline'] = deadline_violated['number_of_hours_over_deadline'].apply(math.ceil)

    print(deadline_violated['number_of_hours_over_deadline'])
    count_over_deadline = deadline_violated.groupby('number_of_hours_over_deadline').size()
    max_hours = 120
    hours_counts = {f"{i}": count_over_deadline.get(i, 0) for i in range(1, max_hours+1)}

    # Print the counts
    for days, count in hours_counts.items():
        print(f" {count} times {days}")
    
    plt.figure(figsize=(12, 6))
    bars=plt.bar(hours_counts.keys(), hours_counts.values(), color='skyblue')
    for bar, count in zip(bars, hours_counts.values()):
        if count != 0:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, '%d' % int(height), ha='center', va='bottom', fontsize=8)


    plt.xlabel('Hours Settled Over Deadline')
    plt.ylabel('Frequency')
    plt.title('Frequency of Hours Settled after deadline')
    plt.xticks(rotation=45)
    plt.xticks(range(0, max_hours, 5)) 
    plt.tight_layout()
    plt.show()

    return