# import streamlit as st
#
#
# import pymongo
# import streamlit as st
# import secret as s
#
# # Connect to the MongoDB database
# client = s.client
# db = client["Website"]
# models = db["Models"]
#
#
# def create_model(name, description):
#     """Creates a new model in the database."""
#     model = {"name": name, "description": description}
#     result = models.insert_one(model)
#     return result.inserted_id
#
#
# def read_models():
#     """Retrieves all models from the database."""
#     return list(models.find())
#
#
# def update_model(model_id, name=None, description=None):
#     """Updates an existing model in the database."""
#     new_values = {}
#     if name is not None:
#         new_values["name"] = name
#     if description is not None:
#         new_values["description"] = description
#     result = models.update_one({"_id": model_id}, {"$set": new_values})
#     return result.modified_count
#
#
# def delete_model(model_id):
#     """Deletes an existing model from the database."""
#     result = models.delete_one({"_id": model_id}) 
#     return result.deleted_count
#
#
# # Define the Streamlit app
# def app():
#
#     st.title("Editing Models")
#     st.text("Hier kann man die Modelle bearbeiten oder neue Hinzufügen welche in der Datenbank gespiechert sind")
#
#     # Show a form to create a new model
#     st.header("Create a new model")
#     name = st.text_input("Name")
#     description = st.text_area("Description")
#     if st.button("Create"):
#         create_model(name, description)
#         st.success("Model created successfully.")
#
#     # Show a list of all models
#     st.header("List of models")
#     model_list = read_models()
#     for model in model_list:
#         st.write(f"**{model['name']}**: {model['description']}")
#         with st.beta_expander("Edit"):
#             edit_name = st.text_input("Name", model["name"])
#             edit_description = st.text_area("Description", model["description"])
#             if st.button("Update"):
#                 update_model(model["_id"], edit_name, edit_description)
#                 st.success("Model updated successfully.")
#         if st.button("Delete"):
#             delete_model(model["_id"])
#             st.success("Model deleted successfully.")
#
# app()   



# import streamlit as st
# import pymongo
# import secret as s
# import gzip
# import io
#
# # Connect to the MongoDB database
# client = s.client
# db = client["Website"]
# models = db["Models"]
#
# def create_model(name, description, image, stl_file):
#     """Creates a new model in the database."""
#     with gzip.open(filename="compressed_image.gz", mode="wb") as f:
#         f.write(image.read())
#     compressed_image = io.BytesIO()
#     with gzip.GzipFile(fileobj=compressed_image, mode="wb") as f:
#         f.write(stl_file.read())
#     compressed_stl_file = compressed_image.getvalue()
#     model = {"name": name, "description": description, "image": compressed_image.getvalue(), "stl_file": compressed_stl_file}
#     result = models.insert_one(model)
#     return result.inserted_id
#
#
#
# def read_models():
#     """Retrieves all models from the database."""
#     return list(models.find())
#
#
# def update_model(model_id, name=None, description=None, image=None, stl_file=None):
#     """Updates an existing model in the database."""
#     new_values = {}
#     if name is not None:
#         new_values["name"] = name
#     if description is not None:
#         new_values["description"] = description
#     if image is not None:
#         new_values["image"] = image
#     if stl_file is not None:
#         new_values["stl_file"] = stl_file
#     result = models.update_one({"_id": model_id}, {"$set": new_values})
#     return result.modified_count
#
#
# def delete_model(model_id):
#     """Deletes an existing model from the database."""
#     result = models.delete_one({"_id": model_id}) 
#     return result.deleted_count
#
#
# # Define the Streamlit app
# def app():
#
#     st.title("Editing Models")
#     st.text("Hier kann man die Modelle bearbeiten oder neue Hinzufügen welche in der Datenbank gespiechert sind")
#
#     # Show a form to create a new model
#     st.header("Create a new model")
#     name = st.text_input("Name")
#     description = st.text_area("Description")
#     image = st.file_uploader("Upload an image of the model", accept_multiple_files=False, type=["png", "jpg", "jpeg"])
#     stl_file = st.file_uploader("Upload the STL file", accept_multiple_files=False, type=["stl"])
#
#     if st.button("Create"):
#         # create_model(name, description, image.read(), stl_file.read())
#         # st.success("Model created successfully.")
#         image_file = io.BytesIO(image.read())
#         stl_file_obj = io.BytesIO(stl_file.read())
#         create_model(name, description, image_file, stl_file_obj)
#         st.success("Model created successfully.")
#
#
#     # Show a list of all models
#     st.header("List of models")
#     model_list = read_models()
#     for model in model_list:
#         st.write(f"**{model['name']}**: {model['description']}")
#         with st.beta_expander("Edit"):
#             edit_name = st.text_input("Name", model["name"])
#             edit_description = st.text_area("Description", model["description"])
#             edit_image = st.file_uploader("Upload a new image of the model")
#             edit_stl_file = st.file_uploader("Upload a new STL file")
#             if st.button("Update"):
#                 if edit_image is not None:
#                     image = edit_image.read()
#                 else:
#                     image = model["image"]
#                 if edit_stl_file is not None:
#                     stl_file = edit_stl_file.read()
#                 else:
#                     stl_file = model["stl_file"]
#                 update_model(model["_id"], edit_name, edit_description, image, stl_file)
#                 st.success("Model updated successfully.")
#         if st.button("Delete"):
#             delete_model(model["_id"])
#             st.success("Model deleted successfully.")
#
# app()



import streamlit as st
import pymongo
import secret as s
import gzip
import io

# Connect to the MongoDB database
client = s.client
db = client["Website"]
models = db["Models"]

def create_model(name, description, image, stl_file):
    """Creates a new model in the database."""
    with gzip.open(filename="compressed_image.gz", mode="wb") as f:
        f.write(image.read())
    compressed_image = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed_image, mode="wb") as f:
        f.write(stl_file.getvalue())
    compressed_stl_file = compressed_image.getvalue()
    model = {"name": name, "description": description, "image": compressed_image.getvalue(), "stl_file": compressed_stl_file}
    result = models.insert_one(model)
    return result.inserted_id

def read_models():
    """Retrieves all models from the database."""
    return list(models.find())

def update_model(model_id, name=None, description=None, image=None, stl_file=None):
    """Updates an existing model in the database."""
    new_values = {}
    if name is not None:
        new_values["name"] = name
    if description is not None:
        new_values["description"] = description
    if image is not None:
        new_values["image"] = image
    if stl_file is not None:
        with gzip.open(filename="compressed_image.gz", mode="wb") as f:
            f.write(image.read())
        compressed_image = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_image, mode="wb") as f:
            f.write(stl_file.getvalue())
        compressed_stl_file = compressed_image.getvalue()
        new_values["stl_file"] = compressed_stl_file
    result = models.update_one({"_id": model_id}, {"$set": new_values})
    return result.modified_count

def delete_model(model_id):
    """Deletes an existing model from the database."""
    result = models.delete_one({"_id": model_id}) 
    return result.deleted_count

# Define the Streamlit app
def app():
    st.title("Editing Models")
    st.text("Hier kann man die Modelle bearbeiten oder neue Hinzufügen welche in der Datenbank gespiechert sind")

    # Show a form to create a new model
    st.header("Create a new model")
    name = st.text_input("Name")
    description = st.text_area("Description")
    image = st.file_uploader("Upload an image of the model", accept_multiple_files=False, type=["png", "jpg", "jpeg"])
    stl_file = st.file_uploader("Upload the STL file", accept_multiple_files=False, type=["stl"])
    
    if st.button("Create"):
        image_file = io.BytesIO(image.read())
        stl_file_obj = io.BytesIO(stl_file.read())
        create_model(name, description, image_file, stl_file_obj)
        st.success("Model created successfully.")


    # Show a list of all models
    st.header("List of models")
    model_list = read_models()
    for model in model_list:
        st.write(f"**{model['name']}**: {model['description']}")
        with st.beta_expander("Edit"):
            edit_name = st.text_input("Name", model["name"])
            edit_description = st.text_area("Description", model["description"])
            edit_image = st.file_uploader("Upload a new image of the model")
            edit_stl_file = st.file_uploader("Upload a new STL file")
            if st.button("Update"):
                if edit_image is not None:
                    image = edit_image.read()
                else:
                    image = model["image"]
                if edit_stl_file is not None:
                    stl_file = edit_stl_file.read()
                else:
                    stl_file = model["stl_file"]
                update_model(model["_id"], edit_name, edit_description, image, stl_file)
                st.success("Model updated successfully.")
        if st.button("Delete"):
            delete_model(model["_id"])
            st.success("Model deleted successfully.")

app()



