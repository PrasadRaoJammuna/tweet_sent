import pandas as  pd
import sqlite3

conn = sqlite3.connect('twitter.db')

c = conn.cursor()

df  = pd.read_sql("SELECT *FROM sentiment WHERE tweet LIKE '%market%' ORDER BY unix DESC LIMIT 1000",conn)
df.sort_values('unix',inplace=True)
df['smoothed_sentiment'] = df['sentiment'].rolling(int(len(df)/7)).mean()

df.dropna(inplace=True)

print(df.head())
print(df.shape)