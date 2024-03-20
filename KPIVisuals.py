import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    # Extract hour from Starttime
    df['Hour'] = df['Starttime'].dt.hour

    # Filter data for Settling and Validating activities
    filtered_df = df[df['Activity'].isin([ 'Validating','Matching','Settling'])]

    # Group by hour and activity, count cases
    hist_data = filtered_df.groupby(['Hour', 'Activity']).size().unstack(fill_value=0)
    hist_data = hist_data[['Validating', 'Matching', 'Settling']]


    # Plotting histogram
    ax=hist_data.plot(kind='bar', stacked=False)
    plt.title('Cases validated, matched and settled per hour')
    plt.xlabel('Hour')
    plt.ylabel('Number of Cases')
    plt.xticks(range(0, 24, 1), [f"{i}-{i+1}" for i in range(0, 24, 1)], rotation=45)
    plt.legend(title='Activity')
    for p in ax.patches:
        if p.get_height()!=0:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', fontsize=4, color='black', xytext=(0, 5), 
                        textcoords='offset points')
    plt.show()
    return

def histogram_unsettled(event_log, event_log_df):
      # Filter traces where the pattern: "... -> Waiting in queue unsettled -> ... -> Settling" occurs
    settle_after_unsettled = pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled", "...", "Settling"]], positive=True)
    
    # Extract case ids where settling occurs after being unsettled
    id_settle_after_unsettled = settle_after_unsettled.case_id.unique()
    
    
    
    # Convert 'Starttime' column to datetime format
    event_log_df['Starttime'] = pd.to_datetime(event_log_df['Starttime'])

    # Extract hour from 'Starttime'
    event_log_df['Hour'] = event_log_df['Starttime'].dt.hour

    # Filter DataFrame for case ids that settle after being unsettled
    # Convert case ids to string for consistency
    id_settle_after_unsettled = [int(tid) for tid in id_settle_after_unsettled]
    filtered_transactions = event_log_df[event_log_df['TID'].isin(id_settle_after_unsettled)]
    filtered_transactions = filtered_transactions[filtered_transactions['Activity'].isin(['Settling'])]
    print(filtered_transactions)

    # Group by hour and count cases
    hist_data = filtered_transactions.groupby('Hour').size()


    # Plot histogram
    ax=hist_data.plot(kind='bar', color='skyblue')
    plt.title('Cases settled after being unsettled per hour')
    plt.xlabel('Hour')
    plt.ylabel('Number of Cases')
    plt.xticks(rotation=45)
    for p in ax.patches:
        if p.get_height()!=0:
            ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', fontsize=8, color='black', xytext=(0, 5), 
                        textcoords='offset points')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


   
    return
    

    

  




