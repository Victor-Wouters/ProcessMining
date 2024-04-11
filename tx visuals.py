import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import locale
import datetime
import time
import Visuals

def read_data(filename):
    eventlog=pd.read_csv(filename, sep=";")
    eventlog['case_id'] = eventlog['TID'].astype(str)
    eventlog['Starttime'] = pd.to_datetime(eventlog['Starttime'], format='%Y-%m-%d %H:%M:%S')
    eventlog['Endtime'] = pd.to_datetime(eventlog['Endtime'], format='%Y-%m-%d %H:%M:%S')
    eventlog['Activity'] = eventlog['Activity'].astype(str)
    eventlog = eventlog.drop(columns=['TID'])

    #convert event log into pm4py object
    event_log = pm4py.format_dataframe(eventlog, case_id='case_id',activity_key='Activity', timestamp_key='Starttime')
    print(event_log)
    return event_log

def per_day(event_log_df, event_log, transactions):
    event_log_df['Starttime'] = pd.to_datetime(event_log_df['Starttime'])

    # Extract date component from 'starttime' column
    event_log_df['Start_date'] = event_log_df['Starttime'].dt.date

    # Get unique dates
    unique_dates = event_log_df['Start_date'].unique()
    previous_dates=[]
    processed=dict()
    

    for date in unique_dates:
        print(date)
        histogram_date=dict()
        event_log_day=event_log[event_log['Starttime'].dt.date==date]
        Visuals.process_map_Heuristics_Miner(event_log_day)
        settled_transactions = pm4py.filter_trace_segments(event_log_day, [["...", "Settling"]], positive=True)
        settled_transactions_id=settled_transactions.case_id.unique()
        settled_transactions_id=[int(tid) for tid in settled_transactions_id]
        number_settled=len(settled_transactions_id)
        print("settled:", number_settled)

        processed_transactions = pm4py.filter_trace_segments(event_log_day, [["...", "Matching", "Checking balance and credit", "..."], ["Checking balance and credit","..."]], positive=True)
        processed_transactions_id=processed_transactions.case_id.unique()
        processed_transactions_id=[int(tid) for tid in processed_transactions_id]
        number_processed=len(processed_transactions_id)
        print("processed:",number_processed)
        
        recycled_transactions_day=pm4py.filter_trace_segments(event_log_day, [["...", "Waiting in queue unsettled", "Checking balance and credit","..."]], positive=True)
        recycled_transactions_day_id=recycled_transactions_day.case_id.unique()
        #recycled_transactions_day_id=[int(tid) for tid in recycled_transactions_day_id]
        print("total transactions tried to recycle:",len(recycled_transactions_day_id))

        #print(len(recycled_transactions_day_id))
        #print(recycled_transactions_day_id)
        validation_transactions = pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date !=date], [["Checking balance and credit","..."]], positive=True)
      
        recycled_transactions_day_previous_days = validation_transactions[(validation_transactions["Starttime"].dt.date !=date) & validation_transactions.case_id.isin(recycled_transactions_day_id)]
        recycled_transactions_day_previous_days_id=recycled_transactions_day_previous_days.case_id.unique()
        recycled_transactions_day_previous_days_id=[int(tid) for tid in recycled_transactions_day_previous_days_id]
        #print("number of transactions tried to recycle from previous days:", len(recycled_transactions_day_previous_days_id))
        #print("recycled:",recycled_transactions_day_previous_days_id)
        #print("processed:",processed_transactions_id)

        settled_value_day=sum(transactions["Value"][transactions['TID'].isin(settled_transactions_id)])
        #print(settled_value_day)
        processed[date]=number_processed
        
        '''for element in recycled_transactions_day_previous_days_id:
            processed_transactions_id.append(element)'''
        print("total processed:" ,len(processed_transactions_id))

        processed_value_day=sum(transactions["Value"][transactions['TID'].isin(processed_transactions_id)])
        

        print("settlement efficiency:", settled_value_day/processed_value_day)
    dates = list(processed.keys())
    violations_count = list(processed.values())

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(dates, violations_count, color='skyblue')

    # Add values on top of the bars
    for bar, value in zip(bars, violations_count):
        plt.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 0.05, 
                f'{value}', 
                ha='center', 
                va='bottom')

    plt.title('Number of transactions processed')
    plt.xlabel('Date')
    plt.ylabel('Number of transactions')
    plt.xticks(rotation=45)

    # Set x-axis ticks to only include dates with violations
    plt.xticks(dates)

    plt.tight_layout()
    plt.show()
    

    return

def number_transactions_settled_unsettled(event_log):
    histogram_dict=dict()
    settled_transactions = pm4py.filter_trace_segments(event_log, [["...", "Settling"]], positive=True)
    settled_transactions_id=settled_transactions.case_id.unique()
    settled_transactions_id=[int(tid) for tid in settled_transactions_id]
    number_settled=len(settled_transactions_id)
    histogram_dict["settled"]=number_settled

    unsettled_transactions = pm4py.filter_trace_segments(event_log, [["...", "Settling"]], positive=False)
    unsettled_transactions_id=unsettled_transactions.case_id.unique()
    unsettled_transactions_id=[int(tid) for tid in unsettled_transactions_id]
    number_unsettled=len(unsettled_transactions_id)
    histogram_dict["unsettled"]=number_unsettled

    keys = list(histogram_dict.keys())
    values = list(histogram_dict.values())

    bar=plt.bar(keys, values)
    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Number of transactions settled and unsettled')
    bar=plt.bar(keys, values, color=['green', 'red'])  # Green for settled, red for unsettled
    for bar, value in zip(bar, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(value,2), ha='center', va='bottom')
    
    # Add a horizontal line for the mean value
    plt.legend()
    plt.xticks(keys)
    green_patch = mpatches.Patch(color='green', label='Settled')
    red_patch = mpatches.Patch(color='red', label='Unsettled')

    plt.legend(handles=[green_patch, red_patch])
    
   # plt.legend(bar, ['Settled', 'Unsettled'])
    plt.xlabel('Outcome')
    plt.ylabel('Number of transactions')
    plt.show()

    return


def over_deadline(event_log_df, event_log, transactions):
    event_log_df['Starttime'] = pd.to_datetime(event_log_df['Starttime'])

    # Extract date component from 'starttime' column
    event_log_df['Start_date'] = event_log_df['Starttime'].dt.date
    #transactions['SettlementDeadline'] = transactions['SettlementDeadline'].dt.date
    transactions['SettlementDeadline'] = pd.to_datetime(transactions['SettlementDeadline'])


    # Get unique dates
    unique_dates = event_log_df['Start_date'].unique()
    violations=dict()
    merged_df=join_eventlog_transactions(event_log_df, transactions)

    for date in unique_dates:
        #print(date)
        settled_cases=merged_df[merged_df["Activity"]=="Settling"]
        deadline_violated=settled_cases[settled_cases["Starttime"].dt.date>settled_cases["SettlementDeadline"].dt.date]
        #print(deadline_violated)

        deadline_violated_day=deadline_violated[deadline_violated["Starttime"].dt.date==date]
        #print("number of deadline violations on", date,":", len(deadline_violated_day))
        #print("Cases that violate the deadline:", deadline_violated_day["TID"].tolist())
        violations[date]=len(deadline_violated_day)

    
   # Extract dates and corresponding violations counts from the dictionary
    dates = list(violations.keys())
    violations_count = list(violations.values())

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(dates, violations_count, color='skyblue')

    # Add values on top of the bars
    for bar, value in zip(bars, violations_count):
        plt.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 0.05, 
                f'{value}', 
                ha='center', 
                va='bottom')

    plt.title('Number of Deadline Violations for Each Day')
    plt.xlabel('Date')
    plt.ylabel('Number of Violations')
    plt.xticks(rotation=45)

    # Set x-axis ticks to only include dates with violations
    plt.xticks(dates)

    plt.tight_layout()
    plt.show()


    return

def join_eventlog_transactions(event_log, transactions):
    merged_df = pd.merge(event_log, transactions, left_on=['TID'], right_on=['TID'], how='inner')
    return merged_df

event_log=read_data('data/eventlog.csv')
transactions = pd.read_csv('data/TRANSACTION1.csv', sep=';')
event_log_df= pd.read_csv('data/eventlog.csv', sep=';')
per_day(event_log_df, event_log, transactions)
over_deadline(event_log_df, event_log, transactions)
#join_eventlog_transactions(event_log_df, transactions)
