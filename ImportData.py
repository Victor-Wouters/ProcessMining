import pandas as pd
import csv
import pm4py

def read_in_data(filename):

    eventlog=pd.read_csv(filename, sep=";")
    eventlog['case_id'] = eventlog['TID'].astype(str)
    eventlog['Starttime'] = pd.to_datetime(eventlog['Starttime'], format='%Y-%m-%d %H:%M:%S')
    eventlog['Endtime'] = pd.to_datetime(eventlog['Endtime'], format='%Y-%m-%d %H:%M:%S')
    eventlog['Activity'] = eventlog['Activity'].astype(str)
    eventlog = eventlog.drop(columns=['TID'])

    #convert event log into pm4py object
    event_log = pm4py.format_dataframe(eventlog, case_id='case_id',activity_key='Activity', timestamp_key='Starttime')

    return event_log