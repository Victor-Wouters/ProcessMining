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


def settlements_graph(event_log_df):
    
    data=event_log_df
    # Convert 'Starttime' and 'Endtime' columns to datetime
    data['Starttime'] = pd.to_datetime(data['Starttime'])
    data['Endtime'] = pd.to_datetime(data['Endtime'])

    # Filter rows where Activity is 'Settling'
    settling_cases = data[data['Activity'] == 'Settling']

    # Group by 'Starttime' and count unique cases
    settling_counts = settling_cases.groupby(settling_cases['Starttime'].dt.floor('H')).size()

    # Plotting
    plt.figure(figsize=(10, 6))
    settling_counts.plot(marker='o', linestyle='-')
    plt.title('Number of Cases Settling Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Cases Settling')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return

def histogram_val_match_sett(event_log_df):
    df=event_log_df
    df['Starttime'] = pd.to_datetime(df['Starttime'])
    

    # Get unique dates
    unique_dates = event_log_df['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    for date in unique_dates:
        hist_data=0
        # Extract hour from Starttime
        df['Hour'] = df['Starttime'].dt.hour
        filtered_df=df[df["Starttime"].dt.date==date]
        print(filtered_df)

        # Filter data for Settling and Validating activities
        filtered_df = filtered_df[filtered_df['Activity'].isin([ 'Validating','Matching','Settling'])]

        # Group by hour and activity, count cases
        hist_data = filtered_df.groupby(['Hour', 'Activity']).size().unstack(fill_value=0)
        hist_data = hist_data[['Validating', 'Matching', 'Settling']]


        # Plotting histogram
        ax=hist_data.plot(kind='bar', stacked=False)
        plt.title(f'Cases validated, matched and settled per hour - Date: {date}')
        plt.xlabel('Hour')
        plt.ylabel('Number of Cases')
        plt.xticks(range(0, 24, 1), [f"{i}-{i+1}" for i in range(0, 24, 1)], rotation=45)
        plt.legend(title='Activity')
        for p in ax.patches:
            if p.get_height()!=0:
                ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='center', fontsize=6, color='black', xytext=(0, 5), 
                            textcoords='offset points')
        plt.show()
    return
def histogram_val_match_sett_30(event_log_df):
    df = event_log_df
    df['Starttime'] = pd.to_datetime(df['Starttime'])

    # Get unique dates
    unique_dates = event_log_df['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    for date in unique_dates:
        hist_data = 0
        # Extract hour and minute from Starttime
        df['Hour_Minute'] = df['Starttime'].dt.strftime('%H:%M')

        filtered_df = df[df["Starttime"].dt.date == date]

        # Filter data for Settling and Validating activities
        filtered_df = filtered_df[filtered_df['Activity'].isin(['Validating', 'Matching', 'Settling'])]

        # Group by 30-minute intervals and activity, count cases
        hist_data = filtered_df.groupby([pd.Grouper(key='Starttime', freq='30T'), 'Activity']).size().unstack(fill_value=0)
        hist_data = hist_data[['Validating', 'Matching', 'Settling']]


        # Plotting histogram
        ax = hist_data.plot(kind='bar', stacked=False)
        plt.figsize=(16, 10)
        plt.title(f'Cases validated, matched and settled per 30 minutes - Date: {date}')
        plt.xlabel('Time')
        plt.ylabel('Number of Cases')

        # Adjust x-axis ticks to align with the center of each 30-minute interval
        plt.xticks(range(len(hist_data.index)), hist_data.index.strftime('%H:%M'), rotation=45, ha='right')

        plt.legend(title='Activity')

        for p in ax.patches:
            if p.get_height() != 0:
                ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=6, color='black', xytext=(0, 5),
                            textcoords='offset points')
        plt.show()
    return

def histogram_val_match_sett_uneven(event_log_df):
    df = event_log_df.copy()
    df['Starttime'] = pd.to_datetime(df['Starttime'])

    # Get unique dates
    unique_dates = df['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    for date in unique_dates:
        # Extract hour and minute from Starttime
        df['Hour_Minute'] = df['Starttime'].dt.strftime('%H:%M')

        filtered_df = df[df["Starttime"].dt.date == date]

        # Filter data for Settling and Validating activities
        filtered_df = filtered_df[filtered_df['Activity'].isin(['Validating', 'Matching', 'Settling'])]
        during_day=filtered_df[filtered_df['Starttime'].dt.hour.between(2, 22)].groupby([pd.Grouper(key='Starttime', freq='60T'), 'Activity']).size().unstack(fill_value=0)
        before_opening=filtered_df[filtered_df['Starttime'].dt.hour.between(0, 1)].groupby([pd.Grouper(key='Starttime', freq='30T'), 'Activity']).size().unstack(fill_value=0)
        after_opening=filtered_df[filtered_df['Starttime'].dt.hour.between(23, 24)].groupby([pd.Grouper(key='Starttime', freq='30T'), 'Activity']).size().unstack(fill_value=0)
        before_opening.index = before_opening.index.strftime('%H:%M')
        during_day.index=during_day.index.strftime('%H:%M')
        after_opening.index = after_opening.index.strftime('%H:%M')
       
    
        # Combine data
      
        hist_data = pd.concat([before_opening, during_day,after_opening], axis=0, sort=False)
        hist_data = hist_data[['Validating', 'Matching', 'Settling']]
     

        # Plotting histogram
        ax = hist_data.plot(kind='bar', stacked=False)
        plt.title(f'Cases validated, matched and settled per hour - Date: {date}')
        plt.xlabel('Time')
        plt.ylabel('Number of Cases')

        # Customize x-axis ticks
        plt.xticks(range(len(hist_data.index)), hist_data.index, rotation=45, ha='right')
        plt.legend(title='Activity')

        for p in ax.patches:
            if p.get_height() != 0:
                ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=6, color='black', xytext=(0, 5),
                            textcoords='offset points')
        plt.show()

       
    return


def histogram_failed_to_settle(event_log):
   
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    
    date_dict_unsettled=dict()
    # Get unique dates
    unique_dates = event_log['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    tried_to_settle=dict()

    for date in unique_dates:

        # Filter traces where the pattern: "... -> Waiting in queue unsettled -> ... -> Settling" occurs
        unsettled_no_credit=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling"]], positive=True)
        id_unsettled_no_credit=unsettled_no_credit.case_id.unique()
        date_dict_unsettled[date]=len(id_unsettled_no_credit)

        processed_transactions = pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...","Positioning", "..."]], positive=True)
        processed_transactions_id=processed_transactions.case_id.unique()
        number_processed=len(processed_transactions_id)
        tried_to_settle[date]=number_processed

    # Extract dates and corresponding violations counts from the dictionary
    dates = tried_to_settle.keys()
    tried_to_settle_values= tried_to_settle.values()
    failed_to_settle =date_dict_unsettled.values()


    # Convert dates to numbers for plotting
    x = range(len(dates))

    # Plot bars for recycling values
    plt.bar(x, tried_to_settle_values, width=0.4, align='center', label='Total Tried to settle')

    # Plot bars for settled values
    plt.bar([i + 0.4 for i in x], failed_to_settle, width=0.4, align='center', label='Total Failed to settle')

    # Add labels to bars
    for i, (recycle, settled) in enumerate(zip(tried_to_settle_values, failed_to_settle)):
        plt.text(i, recycle, str(recycle), ha='center', va='bottom')
        plt.text(i + 0.4, settled, str(settled), ha='center', va='bottom')

    # Add x-axis labels (dates)
    plt.xticks(x, dates)
    plt.xlabel('Date')

    # Add y-axis label
    plt.ylabel('Total')

    # Add legend
    plt.legend()
    plt.title('Successful versus failed settlements per day')

    # Show plot
    plt.tight_layout()
    plt.show()
    return

def over_deadline(event_log):
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
        settled_case_day=settled_cases[settled_cases["Starttime"].dt.date==date]
        #print("number of deadline violations on", date,":", len(deadline_violated_day))
        #print("Cases that violate the deadline:", deadline_violated_day["TID"].tolist())
        violations[date]=len(deadline_violated_day)
        settled[date]=len(settled_case_day)
        ratio[date]=len(deadline_violated_day)/len(settled_cases)
        print(date, settled_case_day, deadline_violated_day)

    
    ratio = {date: (violations[date] / settled[date]) * 100 for date in violations}

    # Extract dates and corresponding violations counts from the dictionary
    dates = list(violations.keys())
    violations_count = list(violations.values())

    # Create the bar chart
    plt.figure(figsize=(10, 6))
    
    bars = plt.bar(dates, violations_count,color='skyblue')

    # Add values on top of the bars
    for bar, value, date in zip(bars, violations_count, dates):
        plt.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 0.05, 
                f'{value}\nPercentage of settled: {ratio[date]:.2f}%', 
                ha='center', 
                va='bottom')

    plt.title('Number of cases settling after deadline')
    plt.xlabel('Date')
    plt.ylabel('Number of Violations')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
    return

def histogram_recycled(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    cases_in_backlog_eod=[]
    date_dict_settled=dict()
    date_dict_recycling=dict()
    # Get unique dates
    unique_dates = event_log['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)

    for date in unique_dates:
        cases_backlog_eod=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling"]], positive=True)
        cases_in_backlog_eod.extend(cases_backlog_eod.case_id.unique())
   
    
    for date in unique_dates:
        # Filter traces where the pattern: "... -> Waiting in queue unsettled -> ... -> Settling" occurs
        settle_after_unsettled_same_day = pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling", "...", "Settling"]], positive=True)
        # Extract case ids where settling occurs after being unsettled
        id_settle_after_unsettled = settle_after_unsettled_same_day.case_id.unique()

        settle_on_day=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...","Settling"]], positive=True)
        settle_on_day_from_backlog=settle_on_day[settle_on_day.case_id.isin(cases_in_backlog_eod)]
        id_settle_on_day_from_backlog=settle_on_day_from_backlog.case_id.unique()

        total_settled_by_recyling_day=len(id_settle_after_unsettled)+len( id_settle_on_day_from_backlog)
        date_dict_settled[date]=total_settled_by_recyling_day

        tried_to_recycle_this_day=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling", "Positioning", "..."]], positive=True)
        id_tried_to_recycle_this_day = tried_to_recycle_this_day.case_id.unique()

        processing_on_day=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...","Positioning","..."]], positive=True)
        tried_to_recycle_from_backlog=processing_on_day[processing_on_day.case_id.isin(cases_in_backlog_eod)]
        id_tried_to_recycle_from_backlog=tried_to_recycle_from_backlog.case_id.unique()
        
        total_tried_to_recyle=len(id_tried_to_recycle_this_day) + len(id_tried_to_recycle_from_backlog)
        date_dict_recycling[date]=total_tried_to_recyle
        date_dict_settled[date]=total_settled_by_recyling_day

        print(date)
        print("total tried to recycle:", total_tried_to_recyle)
        print("total settled after recycling", total_tried_to_recyle)
        
    dates = date_dict_recycling.keys()
    recycling_values = date_dict_recycling.values()
    settled_values = date_dict_settled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))

    # Plot bars for recycling values
    plt.bar(x, recycling_values, width=0.4, align='center', label='Total Cases Tried to Recycle')

    # Plot bars for settled values
    plt.bar([i + 0.4 for i in x], settled_values, width=0.4, align='center', label='Total Cases Settled by Recycling')

    # Add labels to bars
    for i, (recycle, settled) in enumerate(zip(recycling_values, settled_values)):
        plt.text(i, recycle, str(recycle), ha='center', va='bottom')
        plt.text(i + 0.4, settled, str(settled), ha='center', va='bottom')

    # Add x-axis labels (dates)
    plt.xticks(x, dates)
    plt.xlabel('Date')

    # Add y-axis label
    plt.ylabel('Total Cases')

    # Add legend
    plt.legend()
    plt.title('Performance of recycling')


    # Show plot
    plt.tight_layout()
    plt.show()
    return date_dict_settled, date_dict_recycling

def per_day(event_log):
    processed=dict()
    settled=dict()
    recycled=dict()
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date

    # Get unique dates
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    settled_by_recycling,selected_for_recycling =histogram_recycled(event_log)
    processed=dict()
    recycled_selected=dict()
    recycled_settled=dict()
    settled=dict()
    date_dict_unsettled=dict()
    

    for date in unique_dates:
        print(date)
        histogram_date=dict()
        event_log_day=event_log[event_log['Starttime'].dt.date==date]
        #Visuals.process_map_Heuristics_Miner(event_log)
        settled_transactions = pm4py.filter_trace_segments(event_log_day, [["...", "Settling"]], positive=True)
        settled_transactions_id=settled_transactions.case_id.unique()
        number_settled=len(settled_transactions_id)
        print("Number of cases settled:", number_settled)

        unsettled_no_credit=pm4py.filter_trace_segments(event_log_day, [["...", "Waiting in backlog for recycling"]], positive=True)
        id_unsettled_no_credit=unsettled_no_credit.case_id.unique()
        date_dict_unsettled[date]=len(id_unsettled_no_credit)
        

        processed_transactions = pm4py.filter_trace_segments(event_log_day, [["...","Positioning", "..."]], positive=True)
        processed_transactions_id=processed_transactions.case_id.unique()
        number_processed=len(processed_transactions_id)
        print("Number of cases selected for processing:",number_processed)
        
        selected_for_recycling_day=selected_for_recycling.get(date)

        recycled_transactions_day= settled_by_recycling.get(date)
        print("Number of cases settled by recycling:",recycled_transactions_day)
        processed[date]=number_processed
        settled[date]=number_settled
        recycled_selected[date]=selected_for_recycling_day
        recycled_settled[date]=recycled_transactions_day


    dates = processed.keys()
    processed_values = processed.values()
    settled_values = settled.values()
    recycled_selected_values = recycled_selected.values()
    recycled_settled_values = recycled_settled.values()
    unsettled_values=date_dict_unsettled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))

    # Plot bars for processed values
    plt.bar(x, processed_values, width=0.2, align='center', label='Processed')

    # Plot bars for settled values
    plt.bar([i + 0.2 for i in x], settled_values, width=0.2, align='center', label='Settled')

    plt.bar([i + 0.4 for i in x], unsettled_values, width=0.2, align='center', label='Failed to settle')

    # Plot bars for recycled_selected values
    plt.bar([i + 0.6 for i in x], recycled_selected_values, width=0.2, align='center', label='Selected for recycling')

    # Plot bars for recycled_settled values
    plt.bar([i + 0.8 for i in x], recycled_settled_values, width=0.2, align='center', label='Settled by recycling')

    # Add labels to bars
    for i, (processed_val, settled_val, unsettled_val,selected_val, settled_recycled) in enumerate(zip(processed_values, settled_values,unsettled_values, recycled_selected_values, recycled_settled_values)):
        plt.text(i, processed_val, str(processed_val), ha='center', va='bottom')
        plt.text(i + 0.2, settled_val, str(settled_val), ha='center', va='bottom')
        plt.text(i + 0.4, unsettled_val, str(unsettled_val), ha='center', va='bottom')
        plt.text(i + 0.6, selected_val, str(selected_val), ha='center', va='bottom')
        plt.text(i + 0.8, settled_recycled, str(settled_recycled), ha='center', va='bottom')

    # Add x-axis labels (dates)
    plt.xticks(x, dates)
    plt.xlabel('Date')

    # Add y-axis label
    plt.ylabel('Total')

    # Add legend
    plt.legend()
    plt.title('Processing, settlement and recycling of cases')

    # Show plot
    plt.tight_layout()
    plt.show()

    return

    

  




