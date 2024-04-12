##thise code is unused

def settlement_efficiency_participant(event_log,transactions):
    settled_transactions = pm4py.filter_trace_segments(event_log, [["...", "Settling"]], positive=True)
    settled_transactions_id=settled_transactions.case_id.unique()
    settled_transactions_id=[int(tid) for tid in settled_transactions_id]
    #print(settled_transactions_id)
    print("number of transactions settled:", len(settled_transactions_id))
    settlement_participant=dict()
    processed_transactions=pm4py.filter_trace_segments(event_log, [["...","Validating","..."]], positive=True)
    #print(processed_transactions)
    processed_transactions_id=processed_transactions.case_id.unique()
    processed_transactions_id=[int(tid) for tid in processed_transactions_id]

    number_participants=max(transactions["FromParticipantId"])
    participant_efficiency=dict()
    for participant in range(1,number_participants+1):
        #print("participant:", participant)
        sending_transactions_of_participant=transactions["Value"][(transactions['FromParticipantId'] == participant) & (transactions['FromAccountId'] != 0) & (transactions['TID'].isin(processed_transactions_id))]
        print("sending transactions of participant", participant,":", sending_transactions_of_participant, len(sending_transactions_of_participant))

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
    print(participant_efficiency)

    bar=plt.bar(keys, values)
    plt.xlabel('Keys')
    plt.ylabel('Values')
    plt.title('Settlement efficiency for each participant')
    for bar, value in zip(bar, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(value,2), ha='center', va='bottom')
    mean_value = np.mean(values)
   # print("mean settlement efficiency", mean_value)

    # Add a horizontal line for the mean value
   # plt.axhline(y=mean_value, color='r', linestyle='-', label=f'Average Settlement efficiency: {mean_value:.2f}')
    plt.legend()
    plt.xticks(keys)
    plt.xlabel('Participant')
    plt.ylabel('Settlement efficiency')
    plt.show()
    return

def number_transactions_settled_unsettled(event_log):
    df=event_log
    event_log['Starttime'] = pd.to_datetime(df['Starttime'])
    

    # Get unique dates
    unique_dates = event_log['Starttime'].dt.date.unique()
    for date in unique_dates:
        histogram_dict=dict()
        settled_transactions = pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Settling"]], positive=True)
        settled_transactions_id=settled_transactions.case_id.unique()
        settled_transactions_id=[int(tid) for tid in settled_transactions_id]
        number_settled=len(settled_transactions_id)
        histogram_dict["settled"]=number_settled

        unsettled_transactions = pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Settling"]], positive=False)
        print(unsettled_transactions)
        unsettled_transactions_id=unsettled_transactions.case_id.unique()
        unsettled_transactions_id=[int(tid) for tid in unsettled_transactions_id]
        number_unsettled=len(unsettled_transactions_id)
        histogram_dict["unsettled"]=number_unsettled

        keys = list(histogram_dict.keys())
        values = list(histogram_dict.values())

        bar=plt.bar(keys, values)
        plt.xlabel('Keys')
        plt.ylabel('Values')
        plt.title(f'Number of transactions settled and unsettled - Date: {date}')
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
    settlement_efficiency=histogram_dict["Settled value"]/(histogram_dict["Settled value"]+histogram_dict["Unsettled value"])

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
    efficiency_patch = mpatches.Patch(color='blue', label=f'Settlement Efficiency: {settlement_efficiency:.2f}')


    plt.legend(handles=[green_patch, red_patch,efficiency_patch])
    
   # plt.legend(bar, ['Settled', 'Unsettled'])
    plt.xlabel('Outcome')
    plt.ylabel('Value of transactions')
    plt.show()

    return

def settlement_efficiency_over_time(event_log, transactions):
    for i in range(0, 86400, 900):  
        time_hour = time.gmtime(i) 
        time_hour_str = time.strftime('%H:%M:%S', time_hour) 
        
        filtered_event_log = event_log[event_log["Starttime"].hour < time_hour_str]
       
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