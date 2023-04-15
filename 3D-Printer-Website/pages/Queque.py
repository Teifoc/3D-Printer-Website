             
import streamlit as st
import pymongo
from bson import ObjectId
import pandas as pd
import secret as s

st.title("This visualises the 3D-Printer Queue")

st.info("All orders that are stored in the database are displayed here.")

# connection to MongoDB
client = s.client
# select DB and Collection
db = client["Website"]
collection = db["Orders"]

# Retrieve all entries from the collection and convert them into a pandas DataFrame
results = list(collection.find())
df = pd.DataFrame(results)

# Rename the _id column to "Order number"
df.rename(columns={"_id": "Order ID", "name": "model name"}, inplace=True)

# Set the index to the Order ID column
df.set_index("Order ID", inplace=True)

# Display the DataFrame or a message in a Streamlit component
if df.empty:
    st.warning("No orders in the database.")
else:
    st.dataframe(df)

    # Add a text input for the user to enter the order number to delete
    order_to_delete = st.text_input("Enter the order number to delete:")

    # Add a button to initiate the deletion process
    if st.button("Delete order"):
        try:
            # Convert the user input order number to an ObjectId
            order_id = ObjectId(order_to_delete)
        except ValueError:
            st.warning(f"{order_to_delete} is not a valid order number.")
        else:
            # Find the order with the given order number in the collection
            result = collection.find_one({"_id": order_id})

            if result is None:
                st.warning(f"No order found with order number {order_to_delete}.")
            else:
                # Delete the order from the collection
                collection.delete_one({"_id": order_id})
                st.success(f"Order {order_to_delete} deleted from the database.")
                
                # Filter the DataFrame to exclude the deleted order
                df = df[df.index != order_id]
                st.dataframe(df)
