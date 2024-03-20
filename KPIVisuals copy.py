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
    

   
   # Filter rows where Activity is 'validating'
    validating_cases = data[data['Activity'] == 'Validating']

    # Group by 'Starttime' and count unique cases validating
    validating_counts = validating_cases.groupby(validating_cases['Starttime'].dt.floor('H')).size()

    # Filter rows where Activity is 'Settling'
    settling_cases = data[data['Activity'] == 'Settling']

    # Group by 'Starttime' and count unique cases settling
    settling_counts = settling_cases.groupby(settling_cases['Starttime'].dt.floor('H')).size()

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plotting number of cases arriving
    plt.plot(validating_counts.index, validating_counts.values, marker='o', linestyle='-', label='Arriving Cases')

    # Plotting number of cases settling
    plt.plot(settling_counts.index, settling_counts.values, marker='o', linestyle='-', label='Settling Cases')


    plt.title('Number of Cases Arriving and Settling Over Time')
    plt.xlabel('Time')
    plt.ylabel('Number of Cases')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return

