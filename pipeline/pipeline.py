import sys
import pandas as pd 
# parametization to treat data for a specific month 
print('arguments', sys.argv)

month = int(sys.argv[1])

# Definition of the data frame
df = pd.DataFrame({"day": [1,2], "num_passengers": [3,4]})
df['month'] = month
print(df.head())

# save evrything to parquet (parquet is a binary format fo data and is optimised compared to CSV)
df.to_parquet(f"output_{month}.parquet")

print(f'Hello pipeline, month={month}')
