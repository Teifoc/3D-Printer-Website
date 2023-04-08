import streamlit as st


import pymongo
import streamlit as st

# Connect to the MongoDB database
client = pymongo.MongoClient("<mongo-db-uri>")
db = client["<database-name>"]
models = db["models"]


def create_model(name, description):
    """Creates a new model in the database."""
    model = {"name": name, "description": description}
    result = models.insert_one(model)
    return result.inserted_id


def read_models():
    """Retrieves all models from the database."""
    return list(models.find())


def update_model(model_id, name=None, description=None):
    """Updates an existing model in the database."""
    new_values = {}
    if name is not None:
        new_values["name"] = name
    if description is not None:
        new_values["description"] = description
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
    if st.button("Create"):
        create_model(name, description)
        st.success("Model created successfully.")

    # Show a list of all models
    st.header("List of models")
    model_list = read_models()
    for model in model_list:
        st.write(f"**{model['name']}**: {model['description']}")
        with st.beta_expander("Edit"):
            edit_name = st.text_input("Name", model["name"])
            edit_description = st.text_area("Description", model["description"])
            if st.button("Update"):
                update_model(model["_id"], edit_name, edit_description)
                st.success("Model updated successfully.")
        if st.button("Delete"):
            delete_model(model["_id"])
            st.success("Model deleted successfully.")

app()   