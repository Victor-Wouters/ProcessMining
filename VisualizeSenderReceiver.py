import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def visualize_sender_receiver(event_log):
    fontsize1=15
    fontsize2=13
    event_log=event_log[event_log["FromAccountId"]!=0]
    pair_counts = event_log.groupby(['FromParticipantId', 'ToParticipantId']).size().reset_index(name='count')
    plt.figure(figsize=(15, 8))
    plt.scatter(pair_counts['FromParticipantId'], pair_counts['ToParticipantId'], s=pair_counts['count']*5, alpha=0.5)
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


