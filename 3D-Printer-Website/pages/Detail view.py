import streamlit as st
import webbrowser
import secret as s




querry = st.experimental_get_query_params()

if len(querry) == 0:

    st.info("Please select a product first")
    st.info ("Please go to the Homepage and select a product")
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

# dieser Aufruf ist zum testen
st.write(querry['site'][0])

# Connect to the MongoDB database


product_name = "Lion Model"

st.title("Here you can get more info about the Product")

st.header("Product Name: "+product_name)
col_left, col_right = st.columns(2)

col_left.subheader("Product Image")
col_left.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)

st.subheader("Optional parameters")
# Creating form for the ordering process
form = st.form(key="Ordering form")

material_options = ["PLA", "ABS", "PETG", "Wood", "Metal", "Other"]

selected_material = form.selectbox("Material", material_options, help="Select the material you want to print with", key="material")
color_picker = form.color_picker("Pick a color")
pieces = form.number_input("Quantity", min_value=1, max_value=100, value=1, help="How many pieces do you want to print?")
infill = form.number_input("Infill", 0, 100, 1, help="Select here the percentage of the infill (values from 0 to 100 % are allowed)")

form.subheader("Details of Printing")
form.text("Time: Placeholder for the estimated printtime")
form.text("Price for the model: Placeholder for the price")

# Set default values
url_yes = "https://3d-printer-website.streamlit.app/Editing_Models"
url_no = "https://3d-printer-website.streamlit.app/"

# Add checkbox input fields for "Yes" and "No" options
confirm_order = form.checkbox("Yes, I want to continue ordering.", key="confirm_order")

if confirm_order:
    if form.form_submit_button("Confirm", help="Click here to buy the selected material"):

        # Prepare data for the new document
        data = {
            'material': selected_material,
            'color': color_picker,
            'quantity': pieces,
            'infill': infill
        }
        
        #s.db.Models.insert_one(data)

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
