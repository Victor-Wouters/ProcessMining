import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def transactions_over_time(event_log):
    print(event_log)
    data=pd.read_csv('data\eventlog0.csv', sep=';')
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

def histogram():
    df=pd.read_csv('data\eventlog0.csv', sep=';')
    df['Starttime'] = pd.to_datetime(df['Starttime'])

    # Extract hour from Starttime
    df['Hour'] = df['Starttime'].dt.hour

    # Filter data for Settling and Validating activities
    filtered_df = df[df['Activity'].isin([ 'Validating','Matching','Settling'])]

    # Group by hour and activity, count cases
    hist_data = filtered_df.groupby(['Hour', 'Activity']).size().unstack(fill_value=0)
    hist_data = hist_data[['Validating', 'Matching', 'Settling']]


    # Plotting histogram
    hist_data.plot(kind='bar', stacked=False)
    plt.title('Cases validated, matched and settled per hour')
    plt.xlabel('Hour')
    plt.ylabel('Number of Cases')
    plt.xticks(range(0, 24, 1), [f"{i}-{i+1}" for i in range(0, 24, 1)], rotation=45)
    plt.legend(title='Activity')
    plt.show()
    return

