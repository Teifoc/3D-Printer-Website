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

# Check if the "_id" column exists in the DataFrame
if "_id" in df.columns:
    # Rename the "_id" column to "Order ID"
    df.rename(columns={"_id": "Order ID"}, inplace=True)


# Check if the "code" column exists in the DataFrame
if "code" in df.columns:
    # Drop the "code" column
    df = df.drop("code", axis=1)

# Check if the "Order ID" column exists in the DataFrame
if "Order ID" in df.columns:
    # Set the index to the Order ID column
    df.set_index("Order ID", inplace=True)

# Display the DataFrame or a message in a Streamlit component
if df.empty:
    st.warning("No orders in the database.")
else:
    st.dataframe(df)

    # Add a text input for the user to enter the order number to delete
    order_to_delete = st.text_input("Enter the order ID to delete:")
    # Add a text input for the user to enter the random code
    token = st.text_input("Enter the token:")
    
    # Add a button to initiate the deletion process
    if st.button("Delete order"):
        try:
            # Convert the user input order number to an ObjectId
            order_id = ObjectId(order_to_delete)
        except ValueError:
            st.warning(f"{order_to_delete} is not a valid order ID.")
        else:
            # Find the order with the given order number and random code in the collection
            result = collection.find_one({"_id": order_id, "token": token})
    
            if result is None:
                st.warning("Order ID and token combination not found in the database.")
            else:
                # Delete the order from the collection
                collection.delete_one({"_id": order_id, "token": token})
                st.success(f"Order {order_to_delete} deleted from the database.")
    
                # Filter the DataFrame to exclude the deleted order
                df = df[df.index != order_id]
                st.dataframe(df)

                
                
                
                
     # Add a text input for the user to enter the order number to delete
    # order_to_delete = st.text_input("Enter the order ID to delete:")
    #
    # # Add a button to initiate the deletion process
    # if st.button("Delete order"):
    #     try:
    #         # Convert the user input order number to an ObjectId
    #         order_id = ObjectId(order_to_delete)
    #     except ValueError:
    #         st.warning(f"{order_to_delete} is not a valid order ID.")
    #     else:
    #         # Find the order with the given order number in the collection
    #         result = collection.find_one({"_id": order_id})
    #
    #         if result is None:
    #             st.warning(f"No order found with order ID {order_to_delete}.")
    #         else:
    #             # Delete the order from the collection
    #             collection.delete_one({"_id": order_id})
    #             st.success(f"Order {order_to_delete} deleted from the database.")
    #
    #             # Filter the DataFrame to exclude the deleted order
    #             df = df[df.index != order_id]
    #             st.dataframe(df)

