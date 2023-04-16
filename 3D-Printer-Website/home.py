import streamlit as st
import io
import gzip
import pymongo

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def hide_anchor_link():
    st.markdown(
        body="""
        <style>
            h1 > div > a {
                display: none;
            }
            h2 > div > a {
                display: none;
            }
            h3 > div > a {
                display: none;
            }
            h4 > div > a {
                display: none;
            }
            h5 > div > a {
                display: none;
            }
            h6 > div > a {
                display: none;
            }
        </style>
        """,
         unsafe_allow_html=True,
)

hide_anchor_link()

#import secret as s




st.markdown("<h1 style='text-align: center; color: red;'>3D-Printer Website</h1>", unsafe_allow_html=True)

with st.expander("Info about Website"):
    st.header("Welcome to the 3D-Printer Website")
    st.text("Here you can order your 3D-Printed Models")    
    st.info("Info: To view the 3D-Printer Queue just go to the Queue Page")
    st.error("Error: If you have any problems with the Website just contact the Admin")
    st.success('How it should look like:'+'https://pasteboard.co/xRhbRKobSary.png')



st.subheader("Models Overview")


# Connect to the MongoDB database
client = pymongo.MongoClient(st.secrets["db_link"])
#client = s.client
db = client["Website"]
models = db["Models"]

# def read_models():
#     """Retrieves all models from the database."""
#     return list(models.find())

def read_models():
    """Retrieves all models from the database."""
    models = list(db["Models"].find())
    return models


 #("Lion", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "10€", "1h"),

st.text("Here you can see all the Models which are available for ordering")
st.text("Click on the Model to get more information about it")

with st.spinner("Loading Models from Database..."):
     models =list(read_models())

# iterate through the models
num_rows = (len(models) + 3) // 4

# iterate through the rows
for row_index in range(num_rows):
    # create a new row of 4 columns
    columns = st.columns(4)

    # iterate through the columns in the current row
    for col_index in range(4):
        # calculate the index of the current model
        model_index = row_index * 4 + col_index

        # check if the current model index is within the range of the models list
        if model_index < len(models):
            model = models[model_index]
            with columns[col_index]:
                with st.form(key=model["name"]):
                    model_binary_picture = model["picture"]
                    with gzip.GzipFile(fileobj=io.BytesIO(model_binary_picture)) as f:
                        model_image = f.read()
                        st.image(model_image, use_column_width=True)
                    st.text(model["name"])
                    st.text("Price: {}".format(model["price"]) +" €")
                    st.text("Time: {}".format(model["printTime"]) +" hour(s)")

                    
                    url = "http://localhost:8501/Detail_view?id={}".format(str(model['_id']))


                    # Create a centered button with custom CSS
                    st.write(f'''
                        <style>
                            .center {{
                                display: flex;
                                height: 100%;
                            }}
                            .my-button {{
                                background-color: #ff0000;
                                border: none;
                                color: white;
                                padding: 5px 10px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 14px;
                                border-radius: 5px;
                                cursor: pointer;
                            }}
                            .my-button:hover {{
                                background-color: #c40000;
                            }}
                        </style>
                        <a target="_self" href="{url}">
                            <div class="center">
                                <button class="my-button">
                                    Detail view
                                </button>
                            </div>
                        </a>
                    ''',
                    unsafe_allow_html=True)
       
                    like = st.form_submit_button("Like!", help="Click here to Like a Model")
                    if like:
                        st.success("You liked the model!")
                        # there is nothing happenig here yet

                        
