import streamlit as st
import webbrowser

product_name = "Lion Model"


st.title("Here you can get more info about the Product")

st.header("Product Name: "+product_name)
col_left, col_right = st.columns(2)

col_left.subheader ("Product Image")
col_left.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)

#col_right.subheader("Optional parameters")


#col_right.text("Material / PLA")
#col_right.selectbox("Material", ["PLA", "ABS", "PETG", "Wood", "Metal", "Other"], help= "Select the material you want to print with")
#col_right.color_picker("Pick a color")
#pieces = col_right.number_input("Quantity", min_value=1, max_value=100, value=1, help="How many pieces do you want to print?")



st.subheader("Optional parameters")
# Creating form for the ordering process
form = st.form(key="Ordering form")

material_options = ["PLA", "ABS", "PETG", "Wood", "Metal", "Other"]

selected_material = form.selectbox("Material", material_options, help= "Select the material you want to print with", key="material")
form.color_picker("Pick a color")
pieces = form.number_input("Quantity", min_value=1, max_value=100, value=1, help="How many pieces do you want to print?")

# ToDo: Links to the webpages do not work, when clicking on the button. We have to evaluate and fix that.
# Set default values
url_yes = "https://3d-printer-website.streamlit.app/Editing_Models"
url_no = "https://3d-printer-website.streamlit.app/"

# Prompt the user to confirm the order
if form.form_submit_button("Buy", help="Click here to buy the selected material"):     
    st.warning("Do you want to continue ordering?")
    button_clicked = False
    if st.button("Yes"):
         button_clicked = True
    if st.button("No"):
        button_clicked = True
    if button_clicked:
        # Set the URLs based on the button clicked
        if st.button("Yes"):
            url = url_yes
        else:
            url = url_no
        # Open the URL
        webbrowser.open_new_tab(url)

