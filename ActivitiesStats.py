from matplotlib import pyplot as plt
import seaborn as sns

def activities(eventlog):
    eventlog.groupby('Activity').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
    plt.gca().spines[['top', 'right',]].set_visible(False)
    plt.show()
    num_events=len(eventlog)
    num_cases = len(eventlog.case_id.unique())
    print("Number of events: {}\nNumber of cases: {}".format(num_events, num_cases))
    return