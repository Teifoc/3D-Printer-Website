import streamlit as st

#  @Fabian: nach updaten eines Modells tritt die folgende Fehlermeldung auf:
# UnidentifiedImageError: cannot identify image file <_io.BytesIO object at 0x000002232  [Titel anhand dieser ISBN in Citavi-Projekt übernehmen]  [Titel anhand dieser ISBN in Citavi-Projekt übernehmen] D4B4180>
# Traceback:
#
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 565, in _run_script
#     exec(code, module.__dict__)
# File "C:\Users\Maxka\git\3D-Printer-Website\3D-Printer-Website\home.py", line 125, in <module>
#     st.image(model_image, use_column_width=True)
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\streamlit\runtime\metrics_util.py", line 311, in wrapped_func
#     result = non_optional_func(*args, **kwargs)
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\streamlit\elements\image.py", line 169, in image
#     marshall_images(
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\streamlit\elements\image.py", line 536, in marshall_images
#     proto_img.url = image_to_url(
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\streamlit\elements\image.py", line 416, in image_to_url
#     image_format = _validate_image_format_string(image_data, output_format)
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\streamlit\elements\image.py", line 217, in _validate_image_format_string
#     pil_image = Image.open(io.BytesIO(image_data))
# File "C:\Users\Maxka\AppData\Local\Programs\Python\Python310\lib\site-packages\PIL\Image.py", line 3283, in open
#     raise UnidentifiedImageError(msg)
#
# Nach dem Löschen eines Modells aus der Datenbank funktiert der Reload ensprechend ohne Probleme...


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

import secret as s
import io
import gzip
import pymongo



st.markdown("<h1 style='text-align: center; color: red;'>3D-Printer Website</h1>", unsafe_allow_html=True)

with st.expander("Info about Website"):
    st.header("Welcome to the 3D-Printer Website")
    st.text("Here you can order your 3D-Printed Models")    
    st.info("Info: To view the 3D-Printer Queue just go to the Queue Page")
    st.error("Error: If you have any problems with the Website just contact the Admin")
    st.success('How it should look like:'+'https://pasteboard.co/xRhbRKobSary.png')



st.subheader("Models Overview")


# Connect to the MongoDB database
client = s.client
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

                    # @Max hier muss man noch den link zum detail view einfügen bei .format(model[0])
                    url = "http://localhost:8501/Detail_view?site={}".format(model["name"])
                    #url = "http://localhost:8501/Detail_view?site={}".format(str(model['_id']))


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
                    test = st.form_submit_button("Add", help="Click here to add a Moddel to your Shopping Cart")
                    if test:
                        st.success("You added the {} to your shopping cart".format(model["name"]))
                        
