import streamlit as st
import secret as s
import pandas as pd

st.title("This visulises the 3D-Printer Queue")

st.info("Hier werden alle Aufträge angezeigt die in der Datenbank gespeichert sind")

# Verbindung zur MongoDB herstellen
client = s.client
# Datenbank und Collection auswählen
db = s.client.get_database('Website')
collection = db['Orders']

# Alle Einträge aus der Sammlung abrufen und in ein pandas DataFrame umwandeln
results = list(collection.find({}, {"_id": 0}))
df = pd.DataFrame(results)

# Überprüfen, ob die _id-Spalte im DataFrame vorhanden ist, bevor sie entfernt wird
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# DataFrame in Streamlit-Table anzeigen
st.table(df)