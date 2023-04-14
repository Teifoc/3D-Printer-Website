import streamlit as st
import webbrowser
import io
import gzip
import secret as s

query = st.experimental_get_query_params()

if len(query) == 0:
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
model_name = query.get("site")
if not model_name:
    st.error("No model name specified in query parameters.")
    st.stop()

model_name = model_name[0]

st.title("Here you can get more info about the Product")
st.header("Model Name: " + model_name)


# Connect to the MongoDB database
db = s.client.Website


col_left, col_right = st.columns(2)

# Retrieve the model image from the database
model_data = db.Models.find_one({'name': model_name})

if model_data:
    model_binary_picture = model_data['picture']
    with gzip.GzipFile(fileobj=io.BytesIO(model_binary_picture)) as f:
        model_image = f.read()
    
    col_left.subheader("Product Image")
    col_left.image(model_image, use_column_width=True)
else:
    st.error("Model image not found in database.")
    st.stop()

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

# Set default values
url_yes = "https://3d-printer-website.streamlit.app/Editing_Models"
url_no = "https://3d-printer-website.streamlit.app/"

# Add checkbox input fields for "Yes" and "No" options
confirm_order = form.checkbox("Yes, I want to continue ordering.", key="confirm_order")

if confirm_order:
    if form.form_submit_button("Confirm", help="Click here to buy the selected material"):

        # Prepare data for the new document
        data = {
            'name': model_name,
            'material': selected_material,
            'pieces': pieces,
            'color': color_picker,
            'quantity': quantity,
            'infill': infill
        }
        

        # Insert the new document into the collection
        result = db.Orders.insert_one(data)

        # Print success message with the inserted ID
        st.success("Order created successfully with ID: {}".format(result.inserted_id))
else:
    form.form_submit_button("Confirm", help="Click here to buy the selected material")



# # Alternatives for the implmentation of the buy-button (The links to the webpages don't open in this cases):
# url_yes = "https://3d-printer-website.streamlit.app/Editing_Models"
# url_no = "https://3d-printer-website.streamlit.app/"
#
# buy_clicked = False
# yes_or_no_clicked = False
#
# # Prompt the user to confirm the order
# if form.form_submit_button("Buy", help="Click here to buy the selected material"):     
#     st.warning("Do you want to continue ordering?")
#     buy_clicked = True
#     if st.button("Yes"):
#          yes_or_no_clicked = True
#          url = url_yes
#     if st.button("No"):
#         yes_or_no_clicked = True
#         url = url_no
#
# if buy_clicked and yes_or_no_clicked:
#     # Navigate to the URL
#     st.experimental_set_query_params(buy_clicked=True)
#     st.experimental_set_query_params(yes_or_no_clicked=yes_or_no_clicked)
#     st.experimental_set_query_params(url=url)
#
#
# #########
# # ToDo: Links to the webpages do not work, when clicking on the button. We have to evaluate and fix that.
# # Set default values
# url_yes = "https://3d-printer-website.streamlit.app/Editing_Models"
# url_no = "https://3d-printer-website.streamlit.app/"
#
# buy_clicked = False
# yes_or_no_clicked = False
#
# # Prompt the user to confirm the order
# if form.form_submit_button("Buy", help="Click here to buy the selected material"):     
#     st.warning("Do you want to continue ordering?")
#     buy_clicked = True
#     if st.button("Yes"):
#          yes_or_no_clicked = True
#          url = url_yes
#     if st.button("No"):
#         yes_or_no_clicked = True
#         url = url_no
#
# if buy_clicked and yes_or_no_clicked:
#     # Open the URL
#     webbrowser.open_new_tab(url)
