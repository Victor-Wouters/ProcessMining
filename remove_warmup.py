import pandas as pd
import datetime
import time


def remove_warmup_cooldown(event_log, warmup_days, cooldown_days):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    event_log['Endtime'] = pd.to_datetime(event_log['Endtime'])
    unique_dates = event_log['Starttime'].dt.date.unique()
    unique_dates = sorted(unique_dates)
    print(unique_dates)
    if warmup_days!=0:
        for day in range(0,warmup_days):
            date=unique_dates[day]
            print("date to remove:", date)
            transactions_on_date = event_log[event_log['Starttime'].dt.date == date]
            transactions_on_date = transactions_on_date.sort_values(by='Starttime')
            event_log = event_log.drop(transactions_on_date.index)

    if cooldown_days!=0:
        for day in range(-1, -cooldown_days-1, -1):
            date=unique_dates[day]
            print("date to remove:", date)
            transactions_on_date = event_log[event_log['Starttime'].dt.date == date]
            
            transactions_on_date = transactions_on_date.sort_values(by='Starttime')
            event_log = event_log.drop(transactions_on_date.index)
    return event_log
