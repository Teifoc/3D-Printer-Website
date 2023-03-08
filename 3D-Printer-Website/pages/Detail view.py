import streamlit as st

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
form = st.form("Ordering form")

form.selectbox("Material", ["PLA", "ABS", "PETG", "Wood", "Metal", "Other"], help= "Select the material you want to print with")
form.color_picker("Pick a color")
pieces = form.number_input("Quantity", min_value=1, max_value=100, value=1, help="How many pieces do you want to print?")
#form.form_submit_button("Buy")

# Buy-Button
# ToDo: Replace warning with dialogue box with Yes / No option
if form.form_submit_button("Buy", help="Click here to buy the selected material"):
        # Prompt the user to confirm the order
        if st.warning("Do you want to continue ordering?"):
            # If the user confirms, go to the "Editing Models" page
            st.experimental_set_query_params(page="editing_models")
        else:
            # If the user cancels, go back to the home page
            st.experimental_set_query_params(page="home")
            

