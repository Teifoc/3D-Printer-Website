import streamlit as st
import pymongo
import secret as s
import gzip
import io
from bson import ObjectId
import random

#TODO: Token-Logik auch hier noch ergänzen (vgl. Detail view)

# Connect to the MongoDB database
client = s.client
db = client["Website"]
models = db["Models"]

# Generate a random 4-digit token
token = random.randint(1000, 9999)

# Convert the token to a string
token_str = str(token)

def create_model(name, description, picture, stl_file, price, print_time):
    """Creates a new model in the database."""
    if not picture or not stl_file:
        raise ValueError("Please select both a picture and an STL file to upload.")
    
    if not name or not description or not price or not print_time:
        raise ValueError("All fields of the form must be filled out to submit the form.")
    
    if name and description and picture and stl_file and price and print_time:
        try:
            compressed_picture = gzip.compress(picture.read())
            compressed_stl_file = gzip.compress(stl_file.read())
        except AttributeError:
            raise ValueError("Please select both a picture and an STL file to upload.")
        
        # # Generate a random 4-digit token
        # token = random.randint(1000, 9999)
        #
        # # Convert the token to a string
        # token_str = str(token)
    
        model = {
            "name": name,
            "description": description,
            "picture": compressed_picture,
            "stlFile": compressed_stl_file,
            "price": price,
            "printTime": print_time,
            "token": token_str
        }
        
        result = models.insert_one(model)
        created_model = models.find_one({"_id": result.inserted_id})
        return created_model



def read_models():
    """Retrieves all models from the database."""
    return list(models.find())


def update_model(model_id, name=None, description=None, picture=None, stl_file=None, price=None, print_time=None):
    """Updates an existing model in the database."""
    model = models.find_one({"_id": ObjectId(model_id)})
    new_values = {"name": model["name"], "description": model["description"], "picture": model["picture"], "stlFile": model["stlFile"], "price": model["price"], "printTime": model["printTime"]}
    if name is not None:
        new_values["name"] = name
    if description is not None:
        new_values["description"] = description
    if picture is not None:
        if isinstance(picture, bytes):
            picture = io.BytesIO(picture)
        compressed_picture = gzip.compress(picture.read())
        new_values["picture"] = compressed_picture
    if stl_file is not None:
        if isinstance(stl_file, bytes):
            stl_file = io.BytesIO(stl_file)
        compressed_stl_file = gzip.compress(stl_file.read())
        new_values["stlFile"] = compressed_stl_file
    if price is not None:
        new_values["price"] = price
    if print_time is not None:
        new_values["printTime"] = print_time
    result = models.update_one({"_id": ObjectId(model_id)}, {"$set": new_values})
    return result.modified_count



# def update_model(model_id, name=None, description=None, picture=None, stl_file=None, price=None, print_time=None):
#     """Updates an existing model in the database."""
#     model = models.find_one({"_id": ObjectId(model_id)})
#     new_values = {"name": model["name"], "description": model["description"], "picture": model["picture"], "stlFile": model["stlFile"], "price": model["price"], "printTime": model["printTime"]}
#     if name is not None:
#         new_values["name"] = name
#     if description is not None:
#         new_values["description"] = description
#     if picture is not None:
#         if isinstance(picture, bytes):
#             picture = io.BytesIO(picture)
#         compressed_picture = gzip.compress(picture.read())
#         new_values["picture"] = compressed_picture
#         # Update the picture in home.py
#         model_binary_picture = new_values["picture"]
#         with gzip.GzipFile(fileobj=io.BytesIO(model_binary_picture)) as f:
#             picture = f.read()
#         st.cache()(lambda picture: st.image(picture))(picture)
#     if stl_file is not None:
#         if isinstance(stl_file, bytes):
#             stl_file = io.BytesIO(stl_file)
#         compressed_stl_file = gzip.compress(stl_file.read())
#         new_values["stlFile"] = compressed_stl_file
#     if price is not None:
#         new_values["price"] = price
#     if print_time is not None:
#         new_values["printTime"] = print_time
#     result = models.update_one({"_id": ObjectId(model_id)}, {"$set": new_values})
#     return result.modified_count





def delete_model(model_id, token):
    """Deletes an existing model from the database."""
    model = models.find_one({"_id": ObjectId(model_id)})
    if model is None:
        raise ValueError("Model not found.")
    if token == model["token"]:
        result = models.delete_one({"_id": ObjectId(model_id)})
        if result.deleted_count == 1:
            return "Model successfully deleted."
        else:
            raise ValueError("An error occurred while deleting the model.")
    else:
        raise ValueError("Incorrect token.")




# Define the Streamlit app
def app():
    st.title("Editing Models")
    st.text("Here can you add new models to the website.")

    # Show a form to create a new model
    st.header("Create a new model")
    name = st.text_input("Name")
    description = st.text_area("Description")
    picture = st.file_uploader("Upload a picture of the model", accept_multiple_files=False, type=["png", "jpg", "jpeg"], key="picture")
    stl_file = st.file_uploader("Upload the STL file", accept_multiple_files=False, type=["stl"], key="stlFile")
    price = st.number_input("Price in €")
    print_time = st.number_input("Print time in hours")

    if st.button("Create", key="create"):
        picture_file = io.BytesIO(picture.read())
        stl_file_obj = io.BytesIO(stl_file.read())
        created_model = create_model(name, description, picture_file, stl_file_obj, price, print_time)
        st.success(f"Model '{created_model['name']}' created successfully.")
        
        # Provide a way for the user to download the token
        token_bytes = token_str.encode('utf-8')
        token_file = io.BytesIO(token_bytes)
        st.download_button(label="Download token", data=token_file, file_name=f"model_token_{created_model['name']}_{created_model['_id']}.txt", mime="text/plain", key="download_token")

        # Add an explanation of the token's purpose
        st.info("Please download the token above. You will need it to delete the model from the list of models if you want.")

    # Show a list of all models
    st.header("List of models")
    with st.spinner("Loading List of Models from Database..."):
     model_list = list(read_models())
    
    
    
    for model in model_list:
        st.write(f"**{model['name']}**: {model['description']}")
        st.write(f"Price: {model['price']} €, Print time: {model['printTime']} hour(s).")
        # with st.expander("Edit"):
        #     edit_name = st.text_input("Name", model["name"])
        #     edit_description = st.text_area("Description", model["description"])
        #     edit_picture = st.file_uploader("Upload a new picture of the model", key="edit_picture_" + str(model["_id"]))
        #     edit_stl_file = st.file_uploader("Upload a new STL file", key="edit_stl_file_"+ str(model["_id"]))
        #     edit_price = st.number_input("Price in €", value=float(model['price']), key=f"price_{model['_id']}")
        #     edit_print_time = st.number_input("Print time in hours", value=float(model['printTime']), key=f"print_time_{model['_id']}")
        #
        #
        #     if st.button("Update", key=f"update button {model['_id']}"):
        #         if edit_picture is not None:
        #             picture = edit_picture.read()
        #         else:
        #             picture = model["picture"]
        #         if edit_stl_file is not None:
        #             stl_file = edit_stl_file.read()
        #         else:
        #             stl_file = model["stlFile"]
        #         update_model(model["_id"], edit_name, edit_description, picture, stl_file, edit_price, edit_print_time)
        #         st.success(f"Model '{model['name']}' updated successfully.")

        if st.button("Delete Model", key=f"delete_{model_id}"):
            token_input = st.text_input("Please enter the token to confirm:", type="password")
            if token_input:
                try:
                    result = delete_model(model["_id"], token_input)
                    st.success(result)
                    model = None
                except ValueError as e:
                    st.error(str(e))


app()



