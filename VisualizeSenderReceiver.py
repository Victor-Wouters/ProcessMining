import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def visualize_sender_receiver(event_log):
    event_log=event_log[event_log["FromAccountId"]!=0]
    pair_counts = event_log.groupby(['FromParticipantId', 'ToParticipantId']).size().reset_index(name='count')
    plt.figure(figsize=(8, 6))
    plt.scatter(pair_counts['FromParticipantId'], pair_counts['ToParticipantId'], s=pair_counts['count']*5, alpha=0.5)
    for i, row in pair_counts.iterrows():
        plt.text(row['FromParticipantId'], row['ToParticipantId'], row['count'], color='black', ha='center', va='center')

    plt.title('Sender-Receiver Relationships')
    plt.xlabel('Sender')
    plt.ylabel('Receiver')
    plt.xticks(range(int(pair_counts['FromParticipantId'].max()) + 2))
    plt.yticks(range(int(pair_counts['ToParticipantId'].max()) + 2))
    plt.grid(True)
    plt.show()
    return


