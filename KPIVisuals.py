import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import locale
import datetime
import time
import Visuals
from datetime import time
from datetime import timedelta
from datetime import datetime, time


def view(event_log):
    view=pm4py.filter_trace_segments(event_log, [["...","Waiting in backlog for recycling" ,"Positioning","..."]], positive=True)
    print(view)
    print(view.case_id.unique())

    return

def settlements_graph(event_log):
    opening_time = time(22, 00)
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    event_log['Endtime'] = pd.to_datetime(event_log['Endtime'])

    # Determine the start datetime for the analysis
    start_date = event_log['Starttime'].min().floor('D')  # Start from the first day
    start_datetime = datetime.combine(start_date, opening_time)
    start_datetime_utc = pd.Timestamp(start_datetime).tz_localize('UTC')

    # Filter the DataFrame to include entries from the first day starting from 10 PM onwards
    filtered_data = event_log[event_log["Starttime"] >= start_datetime_utc]

    # Filter rows where Activity is 'Settling'
    settling_cases = filtered_data[filtered_data['Activity'] == 'Settling']

    # Create a DataFrame with all hours within the desired range
    end_date = settling_cases['Starttime'].max().floor('H')
    all_hours = pd.date_range(start=start_datetime_utc, end=end_date, freq='H')

    # Group by 'Starttime' and count unique cases
    settling_counts = settling_cases.groupby(settling_cases['Starttime'].dt.floor('H')).size()

    # Merge the two DataFrames to include all hours
    merged_counts = pd.merge(all_hours.to_frame(), settling_counts.reset_index(name='count'), left_on=0, right_on='Starttime', how='left').fillna(0)

    # Drop redundant columns and rename if necessary
    merged_counts = merged_counts.drop(columns=['Starttime']).rename(columns={0: 'Hour'})


    # Plotting
    fontsize1=15
    fontsize2=13
    plt.figure(figsize=(15, 8))
    plt.plot(merged_counts['Hour'], merged_counts['count'], linestyle='-')
    plt.title('Settling Cases Per Hour Over Time', fontsize=fontsize1)
    plt.xlabel('Hour',fontsize=fontsize1)
    plt.ylabel('Count',fontsize=fontsize1)
    plt.xticks(rotation=45,fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return

def histogram_val_match_sett(event_log_df):
    df=event_log_df
    df['Starttime'] = pd.to_datetime(df['Starttime'])
    
    # Get unique dates
    unique_dates = event_log_df['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    for date in unique_dates:
        hist_data=0
        # Extract hour from Starttime
        df['Hour'] = df['Starttime'].dt.hour
        filtered_df=df[df["Starttime"].dt.date==date]

        # Filter data for Settling and Validating activities
        filtered_df = filtered_df[filtered_df['Activity'].isin([ 'Validating','Matching','Settling'])]

        # Group by hour and activity, count cases
        hist_data = filtered_df.groupby(['Hour', 'Activity']).size().unstack(fill_value=0)
        hist_data = hist_data[['Validating', 'Matching', 'Settling']]


        # Plotting histogram
        ax=hist_data.plot(kind='bar', stacked=False)
        fontsize1=15
        fontsize2=13
        plt.figure(figsize=(15, 8))
        plt.title(f'Cases Validated, Matched And Settled Per Hour - Date: {date}',fontsize=fontsize1)
        plt.xlabel('Hour',fontsize=fontsize1)
        plt.ylabel('Number of Cases',fontsize=fontsize1)
        plt.xticks(range(0, 24, 1), [f"{i}-{i+1}" for i in range(0, 24, 1)], rotation=45,fontsize=fontsize1)
        plt.legend(title='Activity',fontsize=fontsize2)
        for p in ax.patches:
            if p.get_height()!=0:
                ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='center', color='black', xytext=(0, 5), 
                            textcoords='offset points',fontsize=fontsize2)
        plt.show()
    return

# def histogram_val_match_sett_30(event_log_df):
#     df = event_log_df
#     df['Starttime'] = pd.to_datetime(df['Starttime'])

#     # Get unique dates
#     unique_dates = event_log_df['Starttime'].dt.date.unique()
#     unique_dates=sorted(unique_dates)
#     for date in unique_dates:
#         hist_data = 0
#         # Extract hour and minute from Starttime
#         df['Hour_Minute'] = df['Starttime'].dt.strftime('%H:%M')

#         filtered_df = df[df["Starttime"].dt.date == date]

#         # Filter data for Settling and Validating activities
#         filtered_df = filtered_df[filtered_df['Activity'].isin(['Validating', 'Matching', 'Settling'])]

#         # Group by 30-minute intervals and activity, count cases
#         hist_data = filtered_df.groupby([pd.Grouper(key='Starttime', freq='30T'), 'Activity']).size().unstack(fill_value=0)
#         hist_data = hist_data[['Validating', 'Matching', 'Settling']]


#         # Plotting histogram
#         ax = hist_data.plot(kind='bar', stacked=False)
#         plt.figsize=(16, 10)
#         plt.title(f'Cases validated, matched and settled per 30 minutes - Date: {date}')
#         plt.xlabel('Time')
#         plt.ylabel('Number of Cases')

#         # Adjust x-axis ticks to align with the center of each 30-minute interval
#         plt.xticks(range(len(hist_data.index)), hist_data.index.strftime('%H:%M'), rotation=45, ha='right')

#         plt.legend(title='Activity')

#         for p in ax.patches:
#             if p.get_height() != 0:
#                 ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
#                             ha='center', va='center', fontsize=6, color='black', xytext=(0, 5),
#                             textcoords='offset points')
#         plt.show()
#     return

# def histogram_val_match_sett_uneven(event_log_df):
#     df = event_log_df.copy()
#     df['Starttime'] = pd.to_datetime(df['Starttime'])

#     # Get unique dates
#     unique_dates = df['Starttime'].dt.date.unique()
#     unique_dates=sorted(unique_dates)
#     for date in unique_dates:
#         # Extract hour and minute from Starttime
#         df['Hour_Minute'] = df['Starttime'].dt.strftime('%H:%M')

#         filtered_df = df[df["Starttime"].dt.date == date]

#         # Filter data for Settling and Validating activities
#         filtered_df = filtered_df[filtered_df['Activity'].isin(['Validating', 'Matching', 'Settling'])]
#         during_day=filtered_df[filtered_df['Starttime'].dt.hour.between(2, 22)].groupby([pd.Grouper(key='Starttime', freq='60T'), 'Activity']).size().unstack(fill_value=0)
#         before_opening=filtered_df[filtered_df['Starttime'].dt.hour.between(0, 1)].groupby([pd.Grouper(key='Starttime', freq='30T'), 'Activity']).size().unstack(fill_value=0)
#         after_opening=filtered_df[filtered_df['Starttime'].dt.hour.between(23, 24)].groupby([pd.Grouper(key='Starttime', freq='30T'), 'Activity']).size().unstack(fill_value=0)
#         before_opening.index = before_opening.index.strftime('%H:%M')
#         during_day.index=during_day.index.strftime('%H:%M')
#         after_opening.index = after_opening.index.strftime('%H:%M')
       
#         # Combine data
      
#         hist_data = pd.concat([before_opening, during_day,after_opening], axis=0, sort=False)
#         hist_data = hist_data[['Validating', 'Matching', 'Settling']]
     
#         # Plotting histogram
#         ax = hist_data.plot(kind='bar', stacked=False)
#         plt.title(f'Cases validated, matched and settled per hour - Date: {date}')
#         plt.xlabel('Time')
#         plt.ylabel('Number of Cases')

#         # Customize x-axis ticks
#         plt.xticks(range(len(hist_data.index)), hist_data.index, rotation=45, ha='right')
#         plt.legend(title='Activity')

#         for p in ax.patches:
#             if p.get_height() != 0:
#                 ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
#                             ha='center', va='center', fontsize=6, color='black', xytext=(0, 5),
#                             textcoords='offset points')
#         plt.show()

       
#     return


def histogram_val_match_sett_uneven(event_log_df):
    df = event_log_df.copy()
    df['Starttime'] = pd.to_datetime(df['Starttime'])

    # Check if Starttime is timezone-aware and adjust bins accordingly
    tz_info = df['Starttime'].dt.tz  # Get timezone information from Starttime

    # Get unique dates
    unique_dates = df['Starttime'].dt.date.unique()
    unique_dates = sorted(unique_dates)
    for date in sorted(event_log_df['Starttime'].dt.date.unique()):
        if date== sorted(event_log_df['Starttime'].dt.date.unique())[0]:
            pass
        else: 
            day_df = df[df['Starttime'].dt.date == date]

            # Filter data for Settling, Matching, and Validating activities
            day_df = day_df[day_df['Activity'].isin(['Validating', 'Matching', 'Settling'])]

            # Define time bins with timezone awareness matching Starttime
            start_time = pd.Timestamp(date, tz=tz_info)
            mid_time = start_time + pd.Timedelta(minutes=30)
            second_last_time = pd.Timestamp(date, tz=tz_info) + pd.Timedelta(hours=23, minutes=30)
            end_time = pd.Timestamp(date, tz=tz_info) + pd.Timedelta(days=1, minutes=-1)  # Adjust last bin to end at 23:59

            # Create custom time bins without duplication
            bins = [start_time, mid_time] + pd.date_range(start=mid_time + pd.Timedelta(hours=1), end=second_last_time, freq='1H').tolist() + [end_time]

            # Create labels for each bin by considering the range each bin covers
            labels = []
            for i in range(len(bins)-1):
                start_label = bins[i].strftime('%H:%M')
                end_label = bins[i+1].strftime('%H:%M')
                labels.append(f'{start_label}-{end_label}')

            # Bin data according to defined bins
            day_df['Time_Bin'] = pd.cut(day_df['Starttime'], bins=bins, labels=labels, right=False)
            binned_data = day_df.groupby(['Time_Bin', 'Activity']).size().unstack(fill_value=0)
            binned_data = binned_data[['Validating', 'Matching', 'Settling']]

            
            ax = binned_data.plot(kind='bar',figsize=(15, 8), stacked=False, width=0.8) #color=[colors.get(x) for x in binned_data.columns]
            fontsize1=15
            fontsize2=13
        
            plt.title(f'Cases Validated, Matched, and Settled Per Hour - Date: {date}', fontsize=fontsize1)
            plt.xlabel('Time', fontsize=fontsize1)
            plt.ylabel('Number of Cases', fontsize=fontsize1)
            plt.xticks(rotation=45, ha='right', fontsize=fontsize1)
            plt.yticks(fontsize=fontsize1)

            # Annotate bar heights
            for p in ax.patches:
                if p.get_height() != 0:
                    ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', color='black', xytext=(0, 5),
                                textcoords='offset points', fontsize=fontsize2)
            

            plt.legend(title='Activity', fontsize=fontsize2)
            plt.tight_layout()
            plt.show()

def histogram_failed_to_settle(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    closing_time=time(19,30)
    opening_time=time(22,00)

    settled=dict()
    unsettled=dict()
    processed=dict()

    for day in sorted(event_log['Starttime'].dt.date.unique()):
        if day== sorted(event_log['Starttime'].dt.date.unique())[0]:
            pass
        else: 
            closing_day=day
            opening_day=day-timedelta(days=1)
            batch_previous_day=event_log[event_log["Starttime"].dt.date==opening_day]
            batch_previous_day=batch_previous_day[batch_previous_day["Starttime"].dt.time>=opening_time]

            rtp_this_day=event_log[event_log["Starttime"].dt.date==closing_day]
            rtp_this_day=rtp_this_day[rtp_this_day["Starttime"].dt.time<=closing_time]

            #compute settled transactions
            #for rtp
            settled_transactions_rtp = pm4py.filter_trace_segments(rtp_this_day, [["...", "Settling"]], positive=True)
            settled_rtp_id=settled_transactions_rtp.case_id.unique()
            number_settled_rtp=len(settled_rtp_id)
           # print(day)
            #print("Number of cases by rtp settled:", number_settled_rtp)
            #add rtp value here

            #for batch
            settled_transactions_batch = pm4py.filter_trace_segments(batch_previous_day, [["...", "Settling"]], positive=True)
            settled_batch_id=settled_transactions_batch.case_id.unique()
            number_settled_batch=len(settled_batch_id)
            #print("Number of cases by batch settled:", number_settled_batch)
            #add batch value here

            total_settled_day=number_settled_batch+number_settled_rtp
            #print("total settled", total_settled_day)
            settled[day]=total_settled_day


            #compute unsettled transactions
            #for rtp
            unsettled_rtp=pm4py.filter_trace_segments(rtp_this_day, [["...", "Waiting in backlog for recycling"]], positive=True)
            unsettled_rtp_id=unsettled_rtp.case_id.unique()
            number_unsettled_rtp=len(unsettled_rtp_id)
           # print("failed to settle rtp:",number_unsettled_rtp)

            #for batch
            unsettled_batch=pm4py.filter_trace_segments(batch_previous_day, [["...", "Waiting in backlog for recycling"]], positive=True)
            unsettled_batch_id=unsettled_batch.case_id.unique()
            number_unsettled_batch=len(unsettled_batch_id)
           # print("failed to settle batch:",number_unsettled_batch)

            total_unsettled_day=number_unsettled_batch+number_unsettled_rtp
            #print("total failed to settle", total_unsettled_day)
            unsettled[day]=total_unsettled_day

             #cases selected for processing
            #for rtp
            processed_transactions_rtp = pm4py.filter_trace_segments(rtp_this_day, [["...","Positioning", "..."]], positive=True)
            processed_transactions_rtp_id=processed_transactions_rtp.case_id.unique()
            number_processed_rtp=len(processed_transactions_rtp_id)
           # print("Number of cases selected for processing rtp:",number_processed_rtp)

            processed_transactions_batch = pm4py.filter_trace_segments(batch_previous_day, [["...","Positioning", "..."]], positive=True)
            processed_transactions_batch_id=processed_transactions_batch.case_id.unique()
            number_processed_batch=len(processed_transactions_batch_id)

            total_processed=number_processed_batch+number_processed_rtp
            #print("total processed cases:", total_processed)
            processed[day]=total_processed

    # Extract dates and corresponding violations counts from the dictionary
    dates = processed.keys()
    tried_to_settle_values= processed.values()
    failed_to_settle =unsettled.values()
    settled=settled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))

    # Plot bars for recycling values
    fontsize1=15
    fontsize2=13
    bar_width = 0.2

    # Create a list of x-coordinates for each group of bars
    x = range(len(tried_to_settle_values))

    # Plot bars for 'Total Selected For Processing'
    plt.bar(x, tried_to_settle_values, width=bar_width, align='center', label='Total Selected For Processing')

    # Plot bars for 'Total Settled'
    plt.bar([i + bar_width for i in x], settled, width=bar_width, align='center', label='Total Settled')

    # Plot bars for 'Total Failed to settle'
    plt.bar([i + 2 * bar_width for i in x], failed_to_settle, width=bar_width, align='center', label='Total Failed to settle')

    # Add labels to bars
    for i, (recycle, settled, failed) in enumerate(zip(tried_to_settle_values, settled, failed_to_settle)):
        plt.text(i, recycle, str(recycle), ha='center', va='bottom', fontsize=fontsize2)
        plt.text(i + bar_width, settled, str(settled), ha='center', va='bottom', fontsize=fontsize2)
        plt.text(i + 2 * bar_width, failed, str(failed), ha='center', va='bottom', fontsize=fontsize2)


    # Add x-axis labels (dates)
    plt.xticks(x, dates,fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)

    # Add y-axis label
    plt.ylabel('Count',fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    # Add legend
    plt.legend( fontsize=fontsize2)
    plt.title('Processed, Settled And Failed Cases Per Day',fontsize=fontsize1)

    # Show plot
    plt.tight_layout()
    plt.show()
    return

def histogram_failed_to_settle_value(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    closing_time=time(19,30)
    opening_time=time(22,00)

    settled=dict()
    unsettled=dict()
    processed=dict()
    rtp=dict()
    batch=dict()
    rtp_ratio=0
    batch_ratio=0

    for day in sorted(event_log['Starttime'].dt.date.unique()):
        if day== sorted(event_log['Starttime'].dt.date.unique())[0]:
            pass
        else: 
            closing_day=day
            opening_day=day-timedelta(days=1)
            batch_previous_day=event_log[event_log["Starttime"].dt.date==opening_day]
            batch_previous_day=batch_previous_day[batch_previous_day["Starttime"].dt.time>=opening_time]

            rtp_this_day=event_log[event_log["Starttime"].dt.date==closing_day]
            rtp_this_day=rtp_this_day[rtp_this_day["Starttime"].dt.time<=closing_time]

            #compute settled transactions
            #for rtp
            settled_transactions_rtp = pm4py.filter_trace_segments(rtp_this_day, [["...", "Settling"]], positive=True)
            rtp_settled_value=settled_transactions_rtp["Value"][settled_transactions_rtp["Activity"]=="Settling"].sum()
            rtp[day]=rtp_settled_value
            #for batch
            settled_transactions_batch = pm4py.filter_trace_segments(batch_previous_day, [["...", "Settling"]], positive=True)
            batch_settled_value=settled_transactions_batch["Value"][settled_transactions_batch["Activity"]=="Settling"].sum()
            batch[day]=batch_settled_value

            total_settled_day=batch_settled_value+rtp_settled_value
            #print("total settled", total_settled_day)
            settled[day]=total_settled_day

            #compute unsettled transactions
            #for rtp
            unsettled_rtp=pm4py.filter_trace_segments(rtp_this_day, [["...", "Waiting in backlog for recycling"]], positive=True)
            rtp_unsettled_value=unsettled_rtp["Value"][unsettled_rtp["Activity"]=="Waiting in backlog for recycling"].sum()

            #for batch
            unsettled_batch=pm4py.filter_trace_segments(batch_previous_day, [["...", "Waiting in backlog for recycling"]], positive=True)
            batch_unsettled_value=unsettled_batch["Value"][unsettled_batch["Activity"]=="Waiting in backlog for recycling"].sum()

            total_unsettled_day=batch_unsettled_value+rtp_unsettled_value
            #print("total failed to settle", total_unsettled_day)
            unsettled[day]=total_unsettled_day

             #cases selected for processing
            #for rtp
            processed_transactions_rtp = pm4py.filter_trace_segments(rtp_this_day, [["...","Positioning", "..."]], positive=True)
            rtp_processed_value=processed_transactions_rtp["Value"][processed_transactions_rtp["Activity"]=="Positioning"].sum()

            processed_transactions_batch = pm4py.filter_trace_segments(batch_previous_day, [["...","Positioning", "..."]], positive=True)
            batch_processed_value=processed_transactions_batch["Value"][processed_transactions_batch["Activity"]=="Positioning"].sum()


            total_processed=batch_processed_value+rtp_processed_value
            #print("total processed cases:", total_processed)
            processed[day]=total_processed

    # Initialize sums
    total_rtp = 0
    total_batch = 0
    total_settled = 0
    for day in settled:
        total_rtp += rtp[day]
        total_batch += batch[day]
        total_settled += settled[day]

    # Calculate averages
    average_rtp = total_rtp / total_settled
    average_batch = total_batch / total_settled

    # Print results
    print("Average RTP per total settled:", round(average_rtp,6)*100)
    print("Average batch per total settled:", round(average_batch,6)*100)
    # Extract dates and corresponding violations counts from the dictionary
    dates = processed.keys()
    tried_to_settle_values= processed.values()
    failed_to_settle =unsettled.values()
    settled=settled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))

    # Plot bars for recycling values
    fontsize1=15
    fontsize2=13
    bar_width = 0.2

    # Create a list of x-coordinates for each group of bars
    x = range(len(tried_to_settle_values))

    # Plot bars for 'Total Selected For Processing'
    plt.bar(x, tried_to_settle_values, width=bar_width, align='center', label='Total Selected For Processing')

    # Plot bars for 'Total Settled'
    plt.bar([i + bar_width for i in x], settled, width=bar_width, align='center', label='Total Settled')

    # Plot bars for 'Total Failed to settle'
    plt.bar([i + 2 * bar_width for i in x], failed_to_settle, width=bar_width, align='center', label='Total Failed to settle')

    # Add labels to bars
    for i, (recycle, settled, failed) in enumerate(zip(tried_to_settle_values, settled, failed_to_settle)):
        plt.text(i, recycle, str(recycle), ha='center', va='bottom', fontsize=fontsize2)
        plt.text(i + bar_width, settled, str(settled), ha='center', va='bottom', fontsize=fontsize2)
        plt.text(i + 2 * bar_width, failed, str(failed), ha='center', va='bottom', fontsize=fontsize2)


    # Add x-axis labels (dates)
    plt.xticks(x, dates,fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)

    # Add y-axis label
    plt.ylabel('Value',fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    # Add legend
    plt.legend( fontsize=fontsize2)
    plt.title('Processed, Settled And Failed Value Per Day',fontsize=fontsize1)

    # Show plot
    plt.tight_layout()
    plt.show()
    return

def over_deadline_settlements(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    closing_time=time(19,30)
    opening_time=time(22,00)
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])

    violations=dict()
    settled=dict()
    ratio=dict()

    for day in sorted(event_log['Starttime'].dt.date.unique()):
        if day== sorted(event_log['Starttime'].dt.date.unique())[0]:
            pass
        else: 
            closing_day=day
            opening_day=day-timedelta(days=1)
            batch_previous_day=event_log[event_log["Starttime"].dt.date==opening_day]
            batch_previous_day=batch_previous_day[batch_previous_day["Starttime"].dt.time>=opening_time]

            rtp_this_day=event_log[event_log["Starttime"].dt.date==closing_day]
            rtp_this_day=rtp_this_day[rtp_this_day["Starttime"].dt.time<=closing_time]
            

            settled_cases_rtp=rtp_this_day[rtp_this_day["Activity"]=="Settling"]
            deadline_violated_rtp=settled_cases_rtp[settled_cases_rtp["Starttime"].dt.date>settled_cases_rtp["SettlementDeadline"].dt.date]

            settled_cases_batch=batch_previous_day[batch_previous_day["Activity"]=="Settling"]
            deadline_violated_batch=settled_cases_batch[(settled_cases_batch["Starttime"].dt.date)+timedelta(days=1)>settled_cases_batch["SettlementDeadline"].dt.date]
            #print("deadline violations rpt", len(deadline_violated_rtp))
            #print("deadline violations batch", len(deadline_violated_batch))

            total_deadline_violations=len(deadline_violated_rtp)+len(deadline_violated_batch)
            total_settled=len(settled_cases_rtp)+len(settled_cases_batch)
            ratio[day]=(total_deadline_violations/ total_settled)*100


    dates = list(ratio.keys())
    ratios = list(ratio.values())

    # Create the bar chart
    fontsize1=15
    fontsize2=13
    plt.figure(figsize=(15, 8))
    
    bars = plt.bar(dates, ratios,color='skyblue')

    # Add values on top of the bars
    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 f"{ratios[i]:.1f}%", ha='center', va='bottom', fontsize=fontsize2)

    plt.title('% of Settled Cases Settling After Deadline',fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)
    plt.ylabel('% of Violations',fontsize=fontsize1)
    plt.xticks(dates, rotation=45,fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    plt.tight_layout()
    plt.show()
    return

"""
def over_deadline(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    #transactions['SettlementDeadline'] = transactions['SettlementDeadline'].dt.date
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])


    # Get unique dates
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    violations=dict()
    settled=dict()
    ratio=dict()
  
    for date in unique_dates:
        #print(date)
        settled_cases=event_log[event_log["Activity"]=="Settling"]
        deadline_violated=settled_cases[settled_cases["Starttime"].dt.date>settled_cases["SettlementDeadline"].dt.date]
        #print(deadline_violated)

        deadline_violated_day=deadline_violated[deadline_violated["Starttime"].dt.date==date]
        settled_case_day=settled_cases[settled_cases["Starttime"].dt.date==date]
        #print("number of deadline violations on", date,":", len(deadline_violated_day))
        #print("Cases that violate the deadline:", deadline_violated_day["TID"].tolist())
        violations[date]=len(deadline_violated_day)
        settled[date]=len(settled_case_day)
        ratio[date]=len(deadline_violated_day)/len(settled_cases)
        #print(date, settled_case_day, deadline_violated_day)

    
    ratio = {date: (violations[date] / settled[date]) * 100 for date in violations}

    # Extract dates and corresponding violations counts from the dictionary
    dates = list(violations.keys())
    violations_count = list(violations.values())

    # Create the bar chart
    fontsize1=15
    fontsize2=13
    plt.figure(figsize=(15, 8))
    
    bars = plt.bar(dates, violations_count,color='skyblue')

    # Add values on top of the bars
    for bar, value, date in zip(bars, violations_count, dates):
        plt.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 0.05, 
                f'{value}\n% Of Settled Day: {ratio[date]:.2f}%', 
                ha='center', 
                va='bottom', fontsize=fontsize2)

    plt.title('Number of Cases Settling After Deadline',fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)
    plt.ylabel('Number of Violations',fontsize=fontsize1)
    plt.xticks(dates, rotation=45,fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    plt.tight_layout()
    plt.show()
    return
    """
"""
def histogram_recycled(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    cases_in_backlog_eod=[]
    date_dict_settled=dict()
    date_dict_recycling=dict()
    # Get unique dates
    unique_dates = event_log['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    cases_backlog_eod2=pm4py.filter_trace_segments(event_log, [["...", "Waiting in backlog for recycling"]], positive=True)


    for date in unique_dates:
        cases_backlog_eod=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling"]], positive=True)
        cases_in_backlog_eod.extend(cases_backlog_eod.case_id.unique())
    recycling_time = time(19, 30)
    
    for date in unique_dates:
        cases_backlog_until_today=cases_backlog_eod2[(cases_backlog_eod2["Activity"]=="Waiting in backlog for recycling") & (cases_backlog_eod2["Starttime"].dt.date<date)]

        # Filter traces where the pattern: "... -> Waiting in queue unsettled -> ... -> Settling" occurs
        settle_after_unsettled_same_day = pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling", "...", "Settling"]], positive=True)
        # Extract case ids where settling occurs after being unsettled
        id_settle_after_unsettled = settle_after_unsettled_same_day.case_id.unique()

        settle_on_day=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...","Settling"]], positive=True)
        settle_on_day_from_backlog=cases_backlog_eod2[(cases_backlog_eod2['Starttime'].dt.time == date) & (cases_backlog_eod2['Activity'] == 'Settling')]

        id_settle_on_day_from_backlog=settle_on_day_from_backlog.case_id.unique()

        total_settled_by_recyling_day=len(id_settle_after_unsettled)+len(id_settle_on_day_from_backlog)
        date_dict_settled[date]=total_settled_by_recyling_day

        tried_to_recycle_this_day=pm4py.filter_trace_segments(event_log[event_log["Starttime"].dt.date==date], [["...", "Waiting in backlog for recycling", "Positioning", "..."]], positive=True)
        id_tried_to_recycle_this_day = tried_to_recycle_this_day.case_id.unique()

        processing_on_day=pm4py.filter_trace_segments(event_log[(event_log['Starttime'].dt.date == date)], [["...","Positioning","..."]], positive=True)
        print(processing_on_day)
        #tried_to_recycle_from_backlog=processing_on_day[processing_on_day.case_id.isin(cases_in_backlog_eod)]
        tried_to_recycle_from_backlog=cases_backlog_until_today[(cases_backlog_until_today['Starttime'].dt.time == recycling_time) & (cases_backlog_until_today['Activity'] == 'Positioning')]
        print(tried_to_recycle_from_backlog)
        id_tried_to_recycle_from_backlog=tried_to_recycle_from_backlog.case_id.unique()

        print("this day",len(id_tried_to_recycle_this_day))
        print("backlog",len(id_tried_to_recycle_from_backlog) )
        
        total_tried_to_recyle=len(id_tried_to_recycle_this_day) + len(id_tried_to_recycle_from_backlog)
        date_dict_recycling[date]=total_tried_to_recyle
        date_dict_settled[date]=total_settled_by_recyling_day

        print(date)
        print("total tried to recycle:", total_tried_to_recyle)
        print("total settled after recycling", total_settled_by_recyling_day)
        
    dates = date_dict_recycling.keys()
    recycling_values = date_dict_recycling.values()
    settled_values = date_dict_settled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))

    # Plot bars for recycling values
    plt.bar(x, recycling_values, width=0.4, align='center', label='Total Cases Tried to Recycle')

    # Plot bars for settled values
    plt.bar([i + 0.4 for i in x], settled_values, width=0.4, align='center', label='Total Cases Settled by Recycling')

    # Add labels to bars
    for i, (recycle, settled) in enumerate(zip(recycling_values, settled_values)):
        plt.text(i, recycle, str(recycle), ha='center', va='bottom')
        plt.text(i + 0.4, settled, str(settled), ha='center', va='bottom')

    # Add x-axis labels (dates)
    plt.xticks(x, dates)
    plt.xlabel('Date')

    # Add y-axis label
    plt.ylabel('Total Cases')

    # Add legend
    plt.legend()
    plt.title('Performance of recycling')

    # Show plot
    plt.tight_layout()
    plt.show()
    return date_dict_settled, date_dict_recycling

    """

def histogram_recycled(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    cases_in_backlog_eod=[]
    date_dict_settled=dict()
    date_dict_recycling=dict()
    # Get unique dates
    unique_dates = event_log['Starttime'].dt.date.unique()
    unique_dates=sorted(unique_dates)
    recycling_time = time(19, 20)
    print(recycling_time)
    
    for date in sorted(event_log['Starttime'].dt.date.unique()):
        if date== sorted(event_log['Starttime'].dt.date.unique())[0]:
            pass
        else: 
            event_log_day=event_log[event_log["Starttime"].dt.date==date]
            #print(event_log_day["Starttime"].dt.time)
            recycling_today=event_log_day[(event_log_day["Starttime"].dt.time==recycling_time) & (event_log_day["Activity"]=="Positioning")]
            #print(recycling_today)
            id_tried_to_recycle_this_day = recycling_today.case_id.unique()

            settle_by_recycling= event_log_day[(event_log_day["Activity"]=="Settling") & event_log_day.case_id.isin(id_tried_to_recycle_this_day)]
            #print(settle_by_recycling)

            total_tried_to_recyle=len(id_tried_to_recycle_this_day)
            total_settled_by_recyling_day=len(settle_by_recycling)

            date_dict_recycling[date]=total_tried_to_recyle
            date_dict_settled[date]=total_settled_by_recyling_day

            print(date)
            print("total tried to recycle:", total_tried_to_recyle)
            print("total settled after recycling", total_settled_by_recyling_day)

    
    dates = date_dict_recycling.keys()
    recycling_values = date_dict_recycling.values()
    settled_values = date_dict_settled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))
    fontsize1=15
    fontsize2=13
    plt.figure(figsize=(15, 8))
    

    # Plot bars for recycling values
    plt.bar(x, recycling_values, width=0.4, align='center', label='Total Cases Tried to Recycle')

    # Plot bars for settled values
    plt.bar([i + 0.4 for i in x], settled_values, width=0.4, align='center', label='Total Cases Settled by Recycling')

    # Add labels to bars
    
    for i, (recycle, settled) in enumerate(zip(recycling_values, settled_values)):
        plt.text(i, recycle, str(recycle), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.4, settled, str(settled), ha='center', va='bottom',fontsize=fontsize2)

    # Add x-axis labels (dates)
    plt.xticks(x, dates,fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)

    # Add y-axis label
    plt.ylabel('Total Cases',fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    # Add legend
    plt.legend(fontsize=fontsize2)
    plt.title('Performance Of Recycling',fontsize=fontsize1)

    # Show plot
    plt.tight_layout()
    plt.show()
    return date_dict_settled, date_dict_recycling


def per_day(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    closing_time=time(19,30)
    opening_time=time(22,00)

    settled=dict()
    unsettled=dict()
    processed=dict()
    settled_by_recycling,selected_for_recycling =histogram_recycled(event_log)
    recycled_selected=dict()
    recycled_settled=dict()

    for day in sorted(event_log['Starttime'].dt.date.unique()):
        if day== sorted(event_log['Starttime'].dt.date.unique())[0]:
            pass
        else: 
            closing_day=day
            opening_day=day-timedelta(days=1)
            batch_previous_day=event_log[event_log["Starttime"].dt.date==opening_day]
            batch_previous_day=batch_previous_day[batch_previous_day["Starttime"].dt.time>=opening_time]

            rtp_this_day=event_log[event_log["Starttime"].dt.date==closing_day]
            rtp_this_day=rtp_this_day[rtp_this_day["Starttime"].dt.time<=closing_time]

            #compute settled transactions
            #for rtp
            settled_transactions_rtp = pm4py.filter_trace_segments(rtp_this_day, [["...", "Settling"]], positive=True)
            settled_rtp_id=settled_transactions_rtp.case_id.unique()
            number_settled_rtp=len(settled_rtp_id)
            #print(day)
            #print("Number of cases by rtp settled:", number_settled_rtp)
            #add rtp value here

            #for batch
            settled_transactions_batch = pm4py.filter_trace_segments(batch_previous_day, [["...", "Settling"]], positive=True)
            settled_batch_id=settled_transactions_batch.case_id.unique()
            number_settled_batch=len(settled_batch_id)
            #print("Number of cases by batch settled:", number_settled_batch)
            #add batch value here

            total_settled_day=number_settled_batch+number_settled_rtp
           # print("total settled", total_settled_day)
            settled[day]=total_settled_day


            #compute unsettled transactions
            #for rtp
            unsettled_rtp=pm4py.filter_trace_segments(rtp_this_day, [["...", "Waiting in backlog for recycling"]], positive=True)
            unsettled_rtp_id=unsettled_rtp.case_id.unique()
            number_unsettled_rtp=len(unsettled_rtp_id)
           # print("failed to settle rtp:",number_unsettled_rtp)

            #for batch
            unsettled_batch=pm4py.filter_trace_segments(batch_previous_day, [["...", "Waiting in backlog for recycling"]], positive=True)
            unsettled_batch_id=unsettled_batch.case_id.unique()
            number_unsettled_batch=len(unsettled_batch_id)
           # print("failed to settle batch:",number_unsettled_batch)

            total_unsettled_day=number_unsettled_batch+number_unsettled_rtp
           # print("total failed to settle", total_unsettled_day)
            unsettled[day]=total_unsettled_day

            #cases selected for processing
            #for rtp
            processed_transactions_rtp = pm4py.filter_trace_segments(rtp_this_day, [["...","Positioning", "..."]], positive=True)
            processed_transactions_rtp_id=processed_transactions_rtp.case_id.unique()
            number_processed_rtp=len(processed_transactions_rtp_id)
           # print("Number of cases selected for processing rtp:",number_processed_rtp)

            processed_transactions_batch = pm4py.filter_trace_segments(batch_previous_day, [["...","Positioning", "..."]], positive=True)
            processed_transactions_batch_id=processed_transactions_batch.case_id.unique()
            number_processed_batch=len(processed_transactions_batch_id)
           # print("Number of cases selected for processing rtp:",number_processed_batch)

            total_processed=number_processed_batch+number_processed_rtp
           # print("total processed cases:", total_processed)
            processed[day]=total_processed

            selected_for_recycling_day=selected_for_recycling.get(day)
            recycled_transactions_day= settled_by_recycling.get(day)
            recycled_selected[day]=selected_for_recycling_day
            recycled_settled[day]=recycled_transactions_day

    dates = processed.keys()
    processed_values = processed.values()
    settled_values = settled.values()
    recycled_selected_values = recycled_selected.values()
    recycled_settled_values = recycled_settled.values()
    unsettled_values=unsettled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))
    plt.figure(figsize=(15, 8))
    fontsize1=15
    fontsize2=13
   

    # Plot bars for processed values
    plt.bar(x, processed_values, width=0.2, align='center', label='Processed')

    # Plot bars for settled values
    plt.bar([i + 0.2 for i in x], settled_values, width=0.2, align='center', label='Settled')

    plt.bar([i + 0.4 for i in x], unsettled_values, width=0.2, align='center', label='Failed to settle')

    # Plot bars for recycled_selected values
    plt.bar([i + 0.6 for i in x], recycled_selected_values, width=0.2, align='center', label='Selected for recycling')

    # Plot bars for recycled_settled values
    plt.bar([i + 0.8 for i in x], recycled_settled_values, width=0.2, align='center', label='Settled by recycling')

    # Add labels to bars
    
    for i, (processed_val, settled_val, unsettled_val,selected_val, settled_recycled) in enumerate(zip(processed_values, settled_values,unsettled_values, recycled_selected_values, recycled_settled_values)):
        plt.text(i, processed_val, str(processed_val), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.2, settled_val, str(settled_val), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.4, unsettled_val, str(unsettled_val), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.6, selected_val, str(selected_val), ha='center', va='bottom', fontsize=fontsize2)
        plt.text(i + 0.8, settled_recycled, str(settled_recycled), ha='center', va='bottom',fontsize=fontsize2)

    # Add x-axis labels (dates)
    plt.xticks(x, dates,fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)

    # Add y-axis label
    plt.ylabel('Total',fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    # Add legend
    plt.legend(fontsize=fontsize2)
    plt.title('Processing, Settlement And Recycling Of Cases',fontsize=fontsize1)

    # Show plot
    plt.tight_layout()
    plt.show()
            
            

    return
'''
def per_day(event_log):
    processed=dict()
    settled=dict()
    recycled=dict()
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    
    # Get unique dates
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    settled_by_recycling,selected_for_recycling =histogram_recycled(event_log)
    processed=dict()
    recycled_selected=dict()
    recycled_settled=dict()
    settled=dict()
    date_dict_unsettled=dict()
    

    for date in unique_dates:
        
        histogram_date=dict()
        previous_date = date - timedelta(days=1)
        opening_date=previous_date
        closing_date=date
        print("date",date)
        print("opening",opening_date)
        print("closing",closing_date)
        closing_time=time(19,30)
        opening_time=time(22,00)
        opening_datetime=datetime.combine(previous_date, opening_time).replace(tzinfo=None)
        closing_datetime=datetime.combine(date, closing_time).replace(tzinfo=None)
        print(event_log['Starttime'])
        print(opening_datetime)
        print(closing_datetime)
        opening_datetime_utc = opening_datetime.replace(tzinfo=pd.Timestamp.tz_utc)
        closing_datetime_utc = closing_datetime.replace(tzinfo=pd.Timestamp.tz_utc)
       
        event_log_day=event_log[(event_log['Starttime']<=closing_datetime_utc) & (event_log['Starttime']>=opening_datetime_utc)]
        print(event_log_day)
       
     
        #Visuals.process_map_Heuristics_Miner(event_log)
        settled_transactions = pm4py.filter_trace_segments(event_log_day, [["...", "Settling"]], positive=True)
        settled_transactions_id=settled_transactions.case_id.unique()
        number_settled=len(settled_transactions_id)
        print("Number of cases settled:", number_settled)

        unsettled_no_credit=pm4py.filter_trace_segments(event_log_day, [["...", "Waiting in backlog for recycling"]], positive=True)
        id_unsettled_no_credit=unsettled_no_credit.case_id.unique()
        date_dict_unsettled[date]=len(id_unsettled_no_credit)
        

        processed_transactions = pm4py.filter_trace_segments(event_log_day, [["...","Positioning", "..."]], positive=True)
        processed_transactions_id=processed_transactions.case_id.unique()
        number_processed=len(processed_transactions_id)
        print("Number of cases selected for processing:",number_processed)
        
        selected_for_recycling_day=selected_for_recycling.get(date)

        recycled_transactions_day= settled_by_recycling.get(date)
        print("Number of cases settled by recycling:",recycled_transactions_day)
        processed[date]=number_processed
        settled[date]=number_settled



    dates = processed.keys()
    processed_values = processed.values()
    settled_values = settled.values()
    recycled_selected_values = recycled_selected.values()
    recycled_settled_values = recycled_settled.values()
    unsettled_values=date_dict_unsettled.values()

    # Convert dates to numbers for plotting
    x = range(len(dates))
    plt.figure(figsize=(15, 8))
    fontsize1=15
    fontsize2=13
   

    # Plot bars for processed values
    plt.bar(x, processed_values, width=0.2, align='center', label='Processed')

    # Plot bars for settled values
    plt.bar([i + 0.2 for i in x], settled_values, width=0.2, align='center', label='Settled')

    plt.bar([i + 0.4 for i in x], unsettled_values, width=0.2, align='center', label='Failed to settle')

    # Plot bars for recycled_selected values
    plt.bar([i + 0.6 for i in x], recycled_selected_values, width=0.2, align='center', label='Selected for recycling')

    # Plot bars for recycled_settled values
    plt.bar([i + 0.8 for i in x], recycled_settled_values, width=0.2, align='center', label='Settled by recycling')

    # Add labels to bars
    
    for i, (processed_val, settled_val, unsettled_val,selected_val, settled_recycled) in enumerate(zip(processed_values, settled_values,unsettled_values, recycled_selected_values, recycled_settled_values)):
        plt.text(i, processed_val, str(processed_val), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.2, settled_val, str(settled_val), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.4, unsettled_val, str(unsettled_val), ha='center', va='bottom',fontsize=fontsize2)
        plt.text(i + 0.6, selected_val, str(selected_val), ha='center', va='bottom', fontsize=fontsize2)
        plt.text(i + 0.8, settled_recycled, str(settled_recycled), ha='center', va='bottom',fontsize=fontsize2)

    # Add x-axis labels (dates)
    plt.xticks(x, dates,fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)

    # Add y-axis label
    plt.ylabel('Total',fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    # Add legend
    plt.legend(fontsize=fontsize2)
    plt.title('Processing, Settlement And Recycling Of Cases',fontsize=fontsize1)

    # Show plot
    plt.tight_layout()
    plt.show()

    return
'''
"""
def deadline_violated_cases_day(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])

    # Extract date component from 'starttime' column
    event_log['Start_date'] = event_log['Starttime'].dt.date
    #transactions['SettlementDeadline'] = transactions['SettlementDeadline'].dt.date
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])

    # Get unique dates
    unique_dates = event_log['Start_date'].unique()
    unique_dates=sorted(unique_dates)
    violations_day=dict()
    ratio=dict()
    
  
    for date in unique_dates:
        
        deadline_violated_activities=event_log[event_log["Starttime"].dt.date>event_log["SettlementDeadline"].dt.date]
    
        deadline_violated_activities_day=deadline_violated_activities[deadline_violated_activities["Starttime"].dt.date==date]
        
        id_violating_cases=deadline_violated_activities_day.case_id.unique()
        violations_day[date]=len(id_violating_cases)

        cases_performed_activity=event_log[event_log["Starttime"].dt.date==date]
        id_cases_performed_activity=cases_performed_activity.case_id.unique()
        ratio[date]=len(id_violating_cases)/len(id_cases_performed_activity)*100
        
    # Extract dates and corresponding violations counts from the dictionary
    dates = list(violations_day.keys())
    violations_count = list(violations_day.values())

    # Create the bar chart
    plt.figure(figsize=(15, 8))
    fontsize1=15
    fontsize2=13
    
    bars = plt.bar(dates, violations_count,color='skyblue')

    # Add values on top of the bars
    for bar, value, date in zip(bars, violations_count, dates):
        plt.text(bar.get_x() + bar.get_width() / 2, 
                bar.get_height() + 0.05, 
                f'{value}\n% Of Unique Cases Day: {ratio[date]:.2f}%', 
                ha='center', 
                va='bottom', fontsize=fontsize2)

    plt.title('Number Of Unique Cases Per Day That Performed An Activity After Deadline' ,fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)
    plt.ylabel('Number of Violations',fontsize=fontsize1)
    plt.xticks(dates, rotation=45,fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)
    plt.tight_layout()
    plt.show()
    
    return
"""

def over_deadline_activites(event_log):
    event_log['Starttime'] = pd.to_datetime(event_log['Starttime'])
    closing_time=time(19,30)
    opening_time=time(22,00)
    event_log['SettlementDeadline'] = pd.to_datetime(event_log['SettlementDeadline'])

    violations=dict()
    settled=dict()
    ratio=dict()

    for day in sorted(event_log['Starttime'].dt.date.unique()):
        if str(day) =="2024-03-03":
            pass
        else: 
            closing_day=day
            opening_day=day-timedelta(days=1)
            batch_previous_day=event_log[event_log["Starttime"].dt.date==opening_day]
            batch_previous_day=batch_previous_day[batch_previous_day["Starttime"].dt.time>=opening_time]

            rtp_this_day=event_log[event_log["Starttime"].dt.date==closing_day]
            rtp_this_day=rtp_this_day[rtp_this_day["Starttime"].dt.time<=closing_time]
            
            deadline_violated_rtp=rtp_this_day[rtp_this_day["Starttime"].dt.date>rtp_this_day["SettlementDeadline"].dt.date]

            
            deadline_violated_batch=batch_previous_day[(batch_previous_day["Starttime"].dt.date)+timedelta(days=1)>batch_previous_day["SettlementDeadline"].dt.date]
            
            print("activity deadline violations rpt", len(deadline_violated_rtp.case_id.unique()))
            print("Activity deadline violations batch", len(deadline_violated_batch.case_id.unique()))

            total_deadline_violations=len(deadline_violated_rtp.case_id.unique())+len(deadline_violated_batch.case_id.unique())
            total_activites=len(rtp_this_day.case_id.unique())+len(batch_previous_day.case_id.unique())
            ratio[day]=(total_deadline_violations/ total_activites)*100


    dates = list(ratio.keys())
    ratios = list(ratio.values())

    # Create the bar chart
    fontsize1=15
    fontsize2=13
    plt.figure(figsize=(15, 8))
    
    bars = plt.bar(dates, ratios,color='skyblue')

    # Add values on top of the bars
    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 f"{ratios[i]:.1f}%", ha='center', va='bottom', fontsize=fontsize2)

    plt.title('% of Cases That Perform An Activity After Deadline',fontsize=fontsize1)
    plt.xlabel('Date',fontsize=fontsize1)
    plt.ylabel('% of Violations',fontsize=fontsize1)
    plt.xticks(dates, rotation=45,fontsize=fontsize1)
    plt.yticks(fontsize=fontsize1)

    plt.tight_layout()
    plt.show()
    return


  
    

  




