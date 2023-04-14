import streamlit as st

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




#client = MongoClient(s.db_url) #st.secrets["db_username"]
#db = client.get_database(s.db_name)
#collection = db.get_collection(s.db_collection)
#db.authenticate(s.db_username, s.db_password)

st.markdown("<h1 style='text-align: center; color: red;'>3D-Printer Website</h1>", unsafe_allow_html=True)




with st.expander("Info about Website"):
    st.header("Welcome to the 3D-Printer Website")
    st.text("Here you can order your 3D-Printed Models")    
    st.info("Info: To view the 3D-Printer Queue just go to the Queue Page")
    st.error("Error: If you have any problems with the Website just contact the Admin")
    st.success('How it should look like:'+'https://pasteboard.co/xRhbRKobSary.png')



st.subheader("Models Overview")


models = [
    ("Lion", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "10€", "1h"),
    ("Tiger", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "15€", "2h"),  
    ("Mouse", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "20€", "3h"), 
    ("Elephant", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "20€", "3h"),
    ("Giraffe", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "25€", "4h"),
    ("Panda", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "25€", "4h"),
    ("Dog", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "30€", "5h"),
    ("Cat", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "30€", "5h"),
    ("Horse", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "35€", "6h"),
    ("Cow", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "35€", "6h"),
    ("Sheep", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "40€", "7h"),
    ("Chicken", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "40€", "7h"),
    ("Pig", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "45€", "8h"),
    ("Duck", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "45€", "8h"),
    ]

st.text("Here you can see all the Models which are available for ordering")
st.text("Click on the Model to get more information about it")

for i in range(0, len(models), 4):
    row = st.columns(4)
    for j in range(4):
        if i+j < len(models):
            model = models[i+j]
            with row[j]:
                form = st.form(key=model[0])
                with form:
                    st.image(model[1], use_column_width=True)
                    st.text(model[0])
                    st.text("Price: {}".format(model[2]))
                    st.text("Time: {}".format(model[3]))
                    
                    # @Max hier muss man noch den link zum detail view einfügen bei .format(model[0])
                    url = "http://localhost:8501/Detail_view?site={}".format(model[0])

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
                    test = form.form_submit_button("Add", help="Click here to add a Moddel to your Shopping Cart")
                    if test:
                        st.success("You added the {} to your shopping cart".format(model[0]))
                    # wenn dieser knopf gedrück wird soll es zum shopping cart hinzugefügt werden

                    #if st.button("More Info about "+str(model[0])+" Model"):
                        #st.set_query_params("/Detail_view/"+model=model[0])
                    #    st.write("https://share.streamlit.io/3d-printer-website/3d-printer-website/main/Detail_view.py?model="+model[0])


st.sidebar.header("Order Form")
st.sidebar.text("List of all your Orders")
st.sidebar.text("just click on a Model to delete it")
#//divide the sidebar into two colums
row = st.sidebar.columns(2)
with row[0]:
    st.button("Delete Lion Model")
    st.text("Tiger Model")
    st.text("Mouse Model")

with row[1]:
    st.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)
    st.text("Elephant Model")
    st.text("Giraffe Model")
    st.text("Panda Model")



