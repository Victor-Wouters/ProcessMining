import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
participants=5
transactions=5000
df = pd.DataFrame(columns=['sender', 'receiver'])
random_weight_matrix = np.random.rand(participants, participants)

# Make the matrix symmetric
random_weight_matrix = (random_weight_matrix + random_weight_matrix.T) / 2
print(random_weight_matrix)

transaction_counter=0
while transaction_counter<transactions:
    x = np.random.randint(0, participants)
    y = np.random.randint(0, participants-1) 
    if y == x:
        y += 1
    random_link=np.random.uniform()

    if random_weight_matrix[x,y]>random_link:
        df.loc[transaction_counter] = [x,y]
        transaction_counter+=1


print(df)
'''
#read your transaction data here
df=pd.read_csv('data/TRANSACTION1.csv', sep=';')
df=df[df["FromAccountId"]!=0]
pair_counts = df.groupby(['FromParticipantId', 'ToParticipantId']).size().reset_index(name='count')


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


