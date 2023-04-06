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



st.title("Models Overview")

#hier kommt eine Schleife hin welche alle Modelle aus der Datenbank ausliest und dann die Modelle in einer Liste anzeigt
st.subheader("Here you can see all the Models which are available for ordering")
st.text("Click on the Model to get more information about it")
col1, col2, col3, col4 = st.columns(4)
col1.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)
col1.text("Lion Model")
col1.text("Price: 10€")
col1.text("Time: 1h")
col2.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)
col2.text("Lion Model_2")
col2.text("Price: 15€")
col2.text("Time: 2h")
col3.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)
col3.text("Lion Model_3")
col3.text("Price: 20€")
col3.text("Time: 3h")
col4.image("https://files.cults3d.com/uploads/collection/shot_en/131/low_poly_collection_3D_printing_3.jpg", use_column_width=True)
col4.text("Lion Model_4")
col4.text("Price: 25€")
col4.text("Time: 4h")

st.success('How it should look like:'+'https://pasteboard.co/xRhbRKobSary.png')

