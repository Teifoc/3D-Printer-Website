import streamlit as st
from io import BytesIO
import gzip
from PIL import Image
import trimesh
import pyvista as pv
from stpyvista import stpyvista
import secret as s


# Verbindung zur MongoDB herstellen
client = s.client
# Datenbank und Collection auswählen
db = s.client.get_database('Website')
collection = db['Models']

# Dummy-Modelle
# models = [
#     {
#         "name": "Modell 1",
#         "picture": gzip.compress(b"Dummy picture data"),
#         "stlFile": gzip.compress(b"Dummy STL file data")
#     },
#     {
#         "name": "Modell 2",
#         "picture": gzip.compress(b"Dummy picture data"),
#         "stlFile": gzip.compress(b"Dummy STL file data")
#     }
# ]

# Cache für die Datenbankabfrage
model_cache = {}

# Funktionen für die Schaltflächen
def select_model(models):
    # Abfrage aller Modelle in der Collection
    if 'models' not in model_cache:
        model_cache['models'] = list(collection.find())
    models = model_cache['models']

    # Dropdown-Menü erstellen, um das Modell auszuwählen
    model_names = [model['name'] for model in models]
    selected_model_name = st.selectbox("Wähle ein Modell aus:", model_names)
    # Das ausgewählte Modell zurückgeben
    return next((model for model in models if model['name'] == selected_model_name), None)



def decompress_data(compressed_data):
    if compressed_data[:2] == b'\x1f\x8b':
        # Daten sind gzip-komprimiert
        data = gzip.decompress(compressed_data)
    else:
        data = compressed_data
    return data


# Streamlit-App
def main():
    st.title("3D-Modelle")

    # Modell auswählen
    model = select_model(models)
    if model is None:
        st.error("Kein Modell gefunden!")
        return

    # Bilddatei dekomprimieren und anzeigen
    picture_data = decompress_data(model['picture'])
    picture = Image.open(BytesIO(picture_data))
    st.image(picture, caption="Bild des 3D-Modells")

    # STL-File dekomprimieren und als PyVista-Gitter laden
    st.write("3D-Modell:")
    stl_file_data = decompress_data(model['stlFile'])
    mesh = trimesh.load(BytesIO(stl_file_data), file_type="stl")
    grid = pv.PolyData(mesh.vertices, mesh.faces)

    # ipythreejs does not support scalar bars :(
    pv.global_theme.show_scalar_bar = False 

    # Initialize a plotter object
    plotter = pv.Plotter(window_size=[400,400])

    # Add the mesh to the plotter
    plotter.add_mesh(grid, color="white")

    # Final touches
    plotter.background_color = "black"
    plotter.view_isometric()

    # Pass a key to avoid re-rendering at each time something changes in the page
    stpyvista(plotter, key="document")

    # Informationen zum Modell anzeigen
    st.write("Name:", model['name'])
    st.write("Beschreibung:", model['description'])
    st.write("Tags:", model['tags'])
    st.write("Autor:", model['author'])
    st.write("Datum:", model['date'].strftime("%d.%m.%Y"))

    # 3D-Ansicht des Modells als STL-File
    st.write("STL-File herunterladen:")
    st.download_button(
        label="Download",
        data=stl_file_data,
        file_name=model['name']+".stl",
        mime="application/octet-stream"
    )


if __name__ == '__main__':
    main()
 
 
 
 
    
    
    
# import streamlit as st
# import pyvista as pv
# from stpyvista import stpyvista
#
# # ipythreejs does not support scalar bars :(
# pv.global_theme.show_scalar_bar = False 
#
# ## Initialize a plotter object
# plotter = pv.Plotter(window_size=[400,400])
#
# ## Create a mesh with a cube 
# mesh = pv.Cube(center=(0,0,0))
#
# ## Add some scalar field associated to the mesh
# mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]
#
# ## Add mesh to the plotter
# plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)
#
# ## Final touches
# plotter.background_color = "black"
# plotter.view_isometric()
#
# ## Pass a key to avoid re-rendering at each time something changes in the page
# stpyvista(plotter, key="pv_cube")



