import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import Visuals

def visualize_sender_receiver(event_log):
    fontsize1=15
    fontsize2=13
    event_log=Visuals.filter_log(event_log)
    event_log=event_log[event_log["Activity"]=="Validating"]
    event_log=event_log[event_log["FromAccountId"]!=0]
    pair_counts = event_log.groupby(['FromParticipantId', 'ToParticipantId']).size().reset_index(name='count')
    plt.figure(figsize=(15, 8))
    plt.scatter(pair_counts['FromParticipantId'], pair_counts['ToParticipantId'], s=pair_counts['count']*30, alpha=0.5)
    for i, row in pair_counts.iterrows():
        plt.text(row['FromParticipantId'], row['ToParticipantId'], row['count'], color='black', ha='center', va='center',fontsize=fontsize2)
    
    
    plt.title('Sender-Receiver Relationships', fontsize=fontsize1)
    plt.xlabel('Sender',fontsize=fontsize1)
    plt.ylabel('Receiver',fontsize=fontsize1)
    plt.xticks(range(int(pair_counts['FromParticipantId'].max()) + 2),fontsize=fontsize1)
    plt.yticks(range(int(pair_counts['ToParticipantId'].max()) + 2),fontsize=fontsize1)
    plt.grid(True)
    plt.show()
    return

def visualize_sender_receiver_value(event_log):
    fontsize1=15
    fontsize2=13
    
    # Filter out irrelevant data and ensure sender is not 0
    event_log = Visuals.filter_log(event_log)
    event_log=event_log[event_log["Activity"]=="Validating"]
    event_log = event_log[event_log["FromAccountId"] != 0]
    
    # Group by sender and receiver, summing the values sent
    pair_values = event_log.groupby(['FromParticipantId', 'ToParticipantId'])['Value'].sum().reset_index(name='total_value')
    
    # Plotting
    plt.figure(figsize=(15, 8))
    plt.scatter(pair_values['FromParticipantId'], pair_values['ToParticipantId'], s=pair_values['total_value']*0.000001, alpha=0.5)
    
    # Annotate with the total value
    for i, row in pair_values.iterrows():
        plt.text(row['FromParticipantId'], row['ToParticipantId'], "${:,.2f}".format(row['total_value']), color='black', ha='center', va='center', fontsize=fontsize2)
    
    # Labels and grid
    plt.title('Value Sent from Sender to Receiver', fontsize=fontsize1)
    plt.xlabel('Sender', fontsize=fontsize1)
    plt.ylabel('Receiver', fontsize=fontsize1)
    plt.xticks(range(int(pair_values['FromParticipantId'].max()) + 2), fontsize=fontsize1)
    plt.yticks(range(int(pair_values['ToParticipantId'].max()) + 2), fontsize=fontsize1)
    plt.grid(True)
    plt.show()

    return

