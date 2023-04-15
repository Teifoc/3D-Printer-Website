import streamlit as st
import webbrowser
import io
import gzip
import secret as s
import random

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

from bson.objectid import ObjectId

object_id = ObjectId(model_id)

# Connect to the MongoDB database
db = s.client.Website

# Retrieve the model data from the database
model_data = db.Models.find_one({'_id':object_id})

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

        # Generate a random 4-digit code
        code = random.randint(1000, 9999)

        # Convert the code to a string
        code_str = str(code)

        # Prepare data for the new document
        data = {
            'name': model_name,
            'material': selected_material,
            'pieces': pieces,
            'color': color_picker,
            'quantity': quantity,
            'infill': infill,
            'code': code_str  # Add the code to the data
        }

        # Insert the new document into the collection
        result = db.Orders.insert_one(data)

        # Remove the 'id' parameter from the URL
        st.experimental_set_query_params()

        # Display the code to the user
        st.success("Order created successfully with Order ID: {} and Code: {}".format(result.inserted_id, code_str))

        # Provide a way for the user to download the code
        code_bytes = code_str.encode('utf-8')
        code_file = io.BytesIO(code_bytes)
        st.download_button(label="Download code", data=code_file, file_name=f"order_code_{result.inserted_id}.txt", mime="text/plain")

        # Add an explanation of the code's purpose
        st.info("Please download the code above. You will need it to delete the order from the list of print jobs if necessary.")
else:
    form.form_submit_button("Confirm", help="Click here to buy the selected material")









