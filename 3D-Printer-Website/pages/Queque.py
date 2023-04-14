import streamlit as st
import secret as s
import pandas as pd

st.title("This visulises the 3D-Printer Queue")

st.info("Hier werden alle Aufträge angezeigt die in der Datenbank gespeichert sind")

# connection to MongoDB
client = s.client
# select DB and Collection
db = s.client.get_database('Website')
collection = db['Orders']

# Retrieve all entries from the collection and convert them into a pandas DataFrame
results = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(results)

# Check whether the _id column is present in the DataFrame before it is removed
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# DataFrame in Streamlit-Table anzeigen
st.table(df)