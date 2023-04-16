import streamlit as st
import webbrowser
import io
import gzip
#import secret as s
import random
from bson.objectid import ObjectId
import pymongo

query = st.experimental_get_query_params()

if 'id' not in query:
    st.info("Please select a product first")
    st.info("Please go to the Homepage and select a product")
    st.info("https://3d-printer-website.streamlit.app")

    url = "https://3d-printer-website.streamlit.app"
    st.write(f'''
        <a target="_self" href="{url}">
        <div class="center">
            <button>
               Click here to select a Product on the Home Page
            </button>
        </div>
        </a>
    ''',
    unsafe_allow_html=True
    )

    st.stop()

# Retrieve the model name from the query parameters, with error handling
model_id = query.get("id")
if not model_id:
    st.error("No model ID specified in query parameters.")
    st.stop()

model_id = model_id[0]



object_id = ObjectId(model_id)

# Connect to the MongoDB database
db = pymongo.MongoClient(st.secrets["db_link"]).Website

# Retrieve the model data from the database
model_data = db.DModels.find_one({'_id':object_id})

if not model_data:
    st.error("Model not found in database.")
    st.stop()

model_name = model_data['name']

st.title("Here you can get more info about the Product")
st.header("Model Name: " + model_name)

col_left, col_right = st.columns(2)

# Retrieve the model image from the database
model_binary_picture = model_data['picture']
with gzip.GzipFile(fileobj=io.BytesIO(model_binary_picture)) as f:
    model_image = f.read()

col_left.subheader("Product Image")
col_left.image(model_image, use_column_width=True)

description = model_data['description']

st.subheader("Details of Printing")
# Retrieve printtime and price data from the database
printtime = model_data['printTime']
price = model_data['price']
st.text("Time: {}".format(printtime) +" hour(s)")
st.text("Price for the model: {}".format(price) +" € / pc")
st.text("Description: {}".format(description))

st.subheader("Optional parameters")
# Creating form for the ordering process
form = st.form(key="Ordering form")

material_options = ["PLA", "ABS", "PETG", "Wood", "Metal", "Other"]

selected_material = form.selectbox("Material", material_options, help="Select the material you want to print with", key="material")
pieces = form.number_input("Pieces:", min_value=1, value=1, help="How many pieces do you want to order?")
color_picker = form.color_picker("Pick a color")
quantity = form.number_input("Quantity", min_value=1, max_value=100, value=1, help="Select the number of quantity")
infill = form.number_input("Infill", 0, 100, 1, help="Select here the percentage of the infill (values from 0 to 100 % are allowed)")

# Add checkbox to confirm the ordering
confirm_order = form.checkbox("Yes, I want to continue ordering.", key="confirm_order")             

if confirm_order:
    if form.form_submit_button("Confirm", help="Click here to buy the selected material"):

        # Generate a random 4-digit token
        token = random.randint(1000, 9999)

        # Convert the token to a string
        token_str = str(token)

        # Prepare data for the new document
        data = {
            'name': model_name,
            'material': selected_material,
            'pieces': pieces,
            'color': color_picker,
            'quantity': quantity,
            'infill': infill,
            'token': token_str  # Add the token to the data
        }

        # Insert the new document into the collection
        result = db.Orders.insert_one(data)

        # Remove the 'id' parameter from the URL
        st.experimental_set_query_params()

        # Display the success info to the user
        st.success("Order created successfully with Order ID: {}".format(result.inserted_id))
        
        
        # Provide a way for the user to download the token
        # token_bytes = token_str.encode('utf-8')
        # token_file = io.BytesIO(token_bytes)
        # st.download_button(label="Download token", data=token_file, file_name=f"order_token_{result.inserted_id}.txt", mime="text/plain")
        
        # Define the additional information
        additional_info = f"{result.inserted_id} --> order ID\n\nThis is a important information. You will need the order ID and the token to delete the order from the list of print jobs on the page 'Queue' if necessary."
        
        # Append the additional information to the token_str
        token_str += " --> token \n" + additional_info
        
        # Encode the token_str and create the token_file
        token_bytes = token_str.encode('utf-8')
        token_file = io.BytesIO(token_bytes)

        # Download the token file with the additional information
        st.download_button(label="Download token", data=token_file, file_name=f"order_token_{result.inserted_id}.txt", mime="text/plain")
        

        # Add an explanation of the token's purpose
        st.info(f"Please download the token above. You will need the order ID and the token to delete the order with the ID '{result.inserted_id}' from the list of print jobs on the page 'Queue' if necessary.")
else:
    form.form_submit_button("Confirm", help="Click here to buy the selected material")









