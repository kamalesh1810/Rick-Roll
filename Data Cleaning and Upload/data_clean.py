import pandas as pd
# load csv file
df = pd.read_csv('user_data.csv')

# select the first two columns of the dataframe
df1 = df[['name','email']]

# drop rows containing NaN values
df1 = df1.dropna()

# remove whitespaces and convert the email ids to lowercase
df1['email'] = [str(i).lower() for i in df1['email']]
df1['email'] = [str(i).strip() for i in df1['email']]

# drop rows which have duplicare email ids
df1 = df1.drop_duplicates(subset=['email'], keep='first')

# export csv
df1.to_csv('users_list.csv',index=False)