import streamlit as st
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
    ("Lion Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "10€", "1h"),
    ("Tiger Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "15€", "2h"),  
    ("Mouse Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "20€", "3h"), 
    ("Elephant Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "20€", "3h"),
    ("Giraffe Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "25€", "4h"),
    ("Panda Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "25€", "4h"),
    ("Dog Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "30€", "5h"),
    ("Cat Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "30€", "5h"),
    ("Horse Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "35€", "6h"),
    ("Cow Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "35€", "6h"),
    ("Sheep Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "40€", "7h"),
    ("Chicken Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "40€", "7h"),
    ("Pig Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "45€", "8h"),
    ("Duck Model", "https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", "45€", "8h"),
    ]

st.text("Here you can see all the Models which are available for ordering")
st.text("Click on the Model to get more information about it")

for i in range(0, len(models), 4):
    row = st.columns(4)
    for j in range(4):
        if i+j < len(models):
            model = models[i+j]
            with row[j]:
                st.image(model[1], use_column_width=True)
                st.text(model[0])
                st.text("Price: {}".format(model[2]))
                st.text("Time: {}".format(model[3]))
                if st.button("Order "+str(model[0])):
                    st.success("You ordered the {} Model".format(model[0]))
                if st.button("More Info about "+str(model[0])+" Model"):
                    #st.set_query_params("/Detail_view/"+model=model[0])
                    st.write("https://share.streamlit.io/3d-printer-website/3d-printer-website/main/Detail_view.py?model="+model[0])


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



