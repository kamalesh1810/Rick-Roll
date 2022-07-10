import firebase_functions
import pandas as pd

# load the cleaned csv file with names and emails
df = pd.read_csv('users_list.csv')

emails = df['email'].tolist()
names = df['name'].tolist()

# upload each email and name to firebase
count = 0
for email in emails:
    firebase_functions.set_field('name',names[count],email)
    count+=1
