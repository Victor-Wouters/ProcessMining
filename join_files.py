import pandas as pd
import numpy as np

def join_eventlog_transactions(event_log, transactions):
    merged_event_log_tran = pd.merge(event_log, transactions, left_on=['TID'], right_on=['TID'], how='inner')
    merged_event_log_tran.to_csv('JoinedLog.csv', index=False,sep=';')
    return merged_event_log_tran

def join_merged_event_log_participants(event_log, participants):
    merged_event_log_part = pd.merge(event_log, participants, left_on=['FromParticipantId', 'FromAccountId'], right_on=['Part ID', 'Account ID'], how='inner')
    merged_event_log_part = merged_event_log_part.rename(columns={'Part ID': 'Sending Part', 'Account ID': 'Sending Account ID', 'Balance': 'Initial Account Balance'})
    merged_event_log_part.to_csv('JoinedLogTranPart.csv', index=False,sep=';')
    return merged_event_log_part


