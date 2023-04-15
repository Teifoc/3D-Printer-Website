import streamlit as st
import pymongo
import secret as s
import gzip
import io
from bson import ObjectId

# Connect to the MongoDB database
client = s.client
db = client["Website"]
models = db["Models"]

def create_model(name, description, image, stl_file):
    """Creates a new model in the database."""
    compressed_image = gzip.compress(image.read())
    compressed_stl_file = gzip.compress(stl_file.read())
    model = {"name": name, "description": description, "image": compressed_image, "stl_file": compressed_stl_file}
    result = models.insert_one(model)
    created_model = models.find_one({"_id": result.inserted_id})
    return created_model


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
        compressed_image = gzip.compress(image.read())
        new_values["image"] = compressed_image
    if stl_file is not None:
        compressed_stl_file = gzip.compress(stl_file.read())
        new_values["stl_file"] = compressed_stl_file
    result = models.update_one({"_id": ObjectId(model_id)}, {"$set": new_values})
    return result.modified_count



def delete_model(model_id):
    """Deletes an existing model from the database."""
    #result = models.delete_one({"_id": pymongo.ObjectId(model_id)})
    result = models.delete_one({"_id": ObjectId(model_id)})
    return result.deleted_count


# Define the Streamlit app
def app():
    st.title("Editing Models")
    st.text("Here can you edit the models or add new ones that are stored in the database.")

    # Show a form to create a new model
    st.header("Create a new model")
    name = st.text_input("Name")
    description = st.text_area("Description")
    image = st.file_uploader("Upload an image of the model", accept_multiple_files=False, type=["png", "jpg", "jpeg"], key="image")
    stl_file = st.file_uploader("Upload the STL file", accept_multiple_files=False, type=["stl"], key="stl_file")

    if st.button("Create"):
        image_file = io.BytesIO(image.read())
        stl_file_obj = io.BytesIO(stl_file.read())
        create_model(name, description, image_file, stl_file_obj)
        st.success(f"Model created successfully.")

    # Show a list of all models
    st.header("List of models")
    model_list = read_models()
    for model in model_list:
        st.write(f"**{model['name']}**: {model['description']}")
        with st.expander("Edit"):
            edit_name = st.text_input("Name", model["name"])
            edit_description = st.text_area("Description", model["description"])
            edit_image = st.file_uploader("Upload a new image of the model", key="edit_image_" + str(model["_id"]))
            edit_stl_file = st.file_uploader("Upload a new STL file", key="edit stl_file"+ str(model["_id"]))
            if st.button("Update", key=f"update button {model['_id']}"):
                if edit_image is not None:
                    image = edit_image.read()
                else:
                    image = model["image"]
                if edit_stl_file is not None:
                    stl_file = edit_stl_file.read()
                else:
                    stl_file = model["stl_file"]
                update_model(model["_id"], edit_name, edit_description, image, stl_file)
                st.success(f"Model {model['name']} updated successfully.")
        if st.button("Delete", key=f"delete button {model['_id']}"):
            delete_model(model["_id"])
            st.success(f"Model {model['name']} deleted successfully.")


app()



