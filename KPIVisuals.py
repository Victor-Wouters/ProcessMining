import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import locale



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
                        ha='center', va='center', fontsize=6, color='black', xytext=(0, 5), 
                        textcoords='offset points')
    plt.show()
    return

def histogram_unsettled(event_log, event_log_df):
      # Filter traces where the pattern: "... -> Waiting in queue unsettled -> ... -> Settling" occurs
    settle_after_unsettled = pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled", "...", "Settling"]], positive=True)
    unsettled_no_credit=pm4py.filter_trace_segments(event_log, [["...", "Waiting in queue unsettled"]], positive=True)
    
    
    # Extract case ids where settling occurs after being unsettled
    id_settle_after_unsettled = settle_after_unsettled.case_id.unique()
    id_unsettled_no_credit=unsettled_no_credit.case_id.unique()
    print(id_settle_after_unsettled)

    # Convert 'Starttime' column to datetime format
    event_log_df['Starttime'] = pd.to_datetime(event_log_df['Starttime'])

    # Extract hour from 'Starttime'
    event_log_df['Hour'] = event_log_df['Starttime'].dt.hour

    # Filter DataFrame for case ids that settle after being unsettled
    # Convert case ids to string for consistency
    id_settle_after_unsettled = [int(tid) for tid in id_settle_after_unsettled]
    transactions_settle_after_unsettled = event_log_df[event_log_df['TID'].isin(id_settle_after_unsettled)]
    transactions_settle_after_unsettled = transactions_settle_after_unsettled[transactions_settle_after_unsettled['Activity'].isin(['Settling'])]
    
    id_unsettled_no_credit=[int(tid) for tid in id_unsettled_no_credit]
    transactions_unsettled = event_log_df[event_log_df['TID'].isin( id_unsettled_no_credit)]
    transactions_unsettled = transactions_unsettled[transactions_unsettled['Activity'].isin(["Waiting in queue unsettled"])]
    print(transactions_unsettled)

    # Group by hour and count cases
    hist_data_settle_after_unsettled = transactions_settle_after_unsettled.groupby('Hour').size()
    hist_data_unsettled = transactions_unsettled.groupby('Hour').size()
    
    # Bar for transactions unsettled
   # plt.bar(hist_data_settle_after_unsettled.index, hist_data_settle_after_unsettled.values, color='green', alpha=0.7, label='Settle After Unsettled')
    # Bar for transactions settled after being unsettled
   # plt.bar(hist_data_unsettled.index, hist_data_unsettled.values, color='blue', alpha=0.7, label='In Queue unsettled')
  


    # Plot histogram
    ax=hist_data_settle_after_unsettled.plot(kind='bar', color='skyblue')
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

def settlement_efficiency_participant(event_log,transactions):
    settled_transactions = pm4py.filter_trace_segments(event_log, [["...", "Settling"]], positive=True)
    settled_transactions_id=settled_transactions.case_id.unique()
    settled_transactions_id=[int(tid) for tid in settled_transactions_id]
    print(settled_transactions_id)
    print("number of transactions settled:", len(settled_transactions_id))
    settlement_participant=dict()

    number_participants=max(transactions["FromParticipantId"])
    participant_efficiency=dict()
    for participant in range(1,number_participants+1):
        #print("participant:", participant)
        sending_transactions_of_participant=transactions["Value"][(transactions['FromParticipantId'] == participant) & (transactions['FromAccountId'] != 0)]
        #print("sending transactions of participant", participant,":", sending_transactions_of_participant, len(sending_transactions_of_participant))

        #print("sending transactions of participant:",sending_transactions_of_participant)
        total_sending = sum(sending_transactions_of_participant)
        #print("sending value of participant", participant,":", total_sending)


        #print("value of settling transactions:",transactions["Value"][(transactions['FromParticipantId'] == participant) & (transactions['TID'].isin(settled_transactions_id))])
        sending_settled=transactions["Value"][(transactions['FromParticipantId'] == participant) & (transactions['FromAccountId'] != 0) & (transactions['TID'].isin(settled_transactions_id))]
        print("settled transactions of participant", participant, ":", sending_settled, len(sending_settled))
        total_sending_settled=sum(sending_settled)
        print("participant total settled value", total_sending_settled)
        settlement_participant[participant]=total_sending_settled
        
        
        settlement_efficiency=total_sending_settled/total_sending
        #print("settlement efficiencey:",participant,":", settlement_efficiency)
        participant_efficiency[participant]=settlement_efficiency
        print(settlement_participant)

    
    
    keys = list(participant_efficiency.keys())
    values = list(participant_efficiency.values())

    bar=plt.bar(keys, values)
    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Settlement efficiency for each participant')
    for bar, value in zip(bar, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(value,2), ha='center', va='bottom')
    mean_value = np.mean(values)
    print("mean settlement efficiency", mean_value)

    # Add a horizontal line for the mean value
    plt.axhline(y=mean_value, color='r', linestyle='-', label=f'Average Settlement efficiency: {mean_value:.2f}')
    plt.legend()
    plt.xticks(keys)
    plt.xlabel('Participant')
    plt.ylabel('Settlement efficiency')
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

def value_transactions_settled_unsettled(event_log, transactions):
    histogram_dict=dict()
    settled_transactions = pm4py.filter_trace_segments(event_log, [["...", "Settling"]], positive=True)
    settled_transactions_id=settled_transactions.case_id.unique()
    settled_transactions_id=[int(tid) for tid in settled_transactions_id]
    settled_transaction_value=sum(transactions["Value"][transactions['TID'].isin(settled_transactions_id)])
    histogram_dict["Settled value"]=settled_transaction_value


    

    unsettled_transactions = pm4py.filter_trace_segments(event_log, [["...", "Settling"]], positive=False)
    unsettled_transactions_id=unsettled_transactions.case_id.unique()
    unsettled_transactions_id=[int(tid) for tid in unsettled_transactions_id]
    unsettled_transaction_value=sum(transactions["Value"][transactions['TID'].isin(unsettled_transactions_id)])
    histogram_dict["Unsettled value"]=unsettled_transaction_value

    keys = list(histogram_dict.keys())
    values = list(histogram_dict.values())

    bar=plt.bar(keys, values)
    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Value of transactions settled and unsettled')
    locale.setlocale(locale.LC_ALL, '')
    formatter = lambda x, _: locale.format_string('%d', x, grouping=True)
    plt.gca().yaxis.set_major_formatter(formatter)
    bar=plt.bar(keys, values, color=['green', 'red'])  # Green for settled, red for unsettled
    for bar, value in zip(bar, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), locale.format_string('%d', value, grouping=True), ha='center', va='bottom')
    
    # Add a horizontal line for the mean value
    plt.legend()
    plt.xticks(keys)
    green_patch = mpatches.Patch(color='green', label='Settled')
    red_patch = mpatches.Patch(color='red', label='Unsettled')

    plt.legend(handles=[green_patch, red_patch])
    
   # plt.legend(bar, ['Settled', 'Unsettled'])
    plt.xlabel('Outcome')
    plt.ylabel('Value of transactions')
    plt.show()

    return




    

    

  




