import streamlit as st
from io import BytesIO
import gzip
from PIL import Image
import trimesh
import pyvista as pv
from stpyvista import stpyvista
import io
import secret as s


# Verbindung zur MongoDB herstellen
client = s.client
# Datenbank und Collection auswählen
db = s.client.get_database('Website')
collection = db['Models']

# Dummy-Modelle
models = [
    # {
    #     "name": "Modell 1",
    #     "picture": gzip.compress(b"Dummy picture data"),
    #     "stlFile": gzip.compress(b"Dummy STL file data")
    # },
    # {
    #     "name": "Modell 2",
    #     "picture": gzip.compress(b"Dummy picture data"),
    #     "stlFile": gzip.compress(b"Dummy STL file data")
    # }
]

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
# def main():
#     st.title("3D-Modelle")
#
#     # Modell auswählen
#     model = select_model(models)
#     if model is None:
#         st.error("Kein Modell gefunden!")
#         return
#
#     # Bilddatei dekomprimieren und anzeigen
#     picture_data = decompress_data(model['picture'])
#     picture = Image.open(BytesIO(picture_data))
#     st.image(picture, caption="Bild des 3D-Modells")
#
#     # STL-File dekomprimieren und als PyVista-Gitter laden
#     # st.write("3D-Modell:")
#     stl_file_data = decompress_data(model['stlFile'])
#     # mesh = trimesh.load(BytesIO(stl_file_data), file_type="stl")
#     # grid = pv.PolyData(mesh.vertices, mesh.faces)
#     #
#     # # ipythreejs does not support scalar bars :(
#     # pv.global_theme.show_scalar_bar = False 
#     #
#     # # Initialize a plotter object
#     # plotter = pv.Plotter(window_size=[400,400])
#     #
#     # # Add the mesh to the plotter
#     # plotter.add_mesh(grid, color="white")
#     #
#     # # Final touches
#     # plotter.background_color = "black"
#     # plotter.view_isometric()
#     #
#     # # Pass a key to avoid re-rendering at each time something changes in the page
#     # stpyvista(plotter, key="document")
#     #
#     # # Informationen zum Modell anzeigen
#     # st.write("Name:", model['name'])
#     # st.write("Beschreibung:", model['description'])
#     # st.write("Tags:", model['tags'])
#     # st.write("Autor:", model['author'])
#     # st.write("Datum:", model['date'].strftime("%d.%m.%Y"))
#     #
#     # # 3D-Ansicht des Modells als STL-File
#     # st.write("STL-File herunterladen:")
#     # st.download_button(
#     #     label="Download",
#     #     data=stl_file_data,
#     #     file_name=model['name']+".stl",
#     #     mime="application/octet-stream"
#     # )
#
#     ## Load the STL file as a Trimesh object
#     mesh_trimesh = trimesh.load(fileobj=BytesIO(stl_file_data), file_type="stl")
#
#     ## Convert the Trimesh object to a PyVista mesh
#     mesh_pv = pv.PolyData(mesh_trimesh.vertices, mesh_trimesh.faces)
#
#     ## Add some scalar field associated to the mesh
#     mesh_pv['myscalar'] = mesh_pv.points[:, 2]*mesh_pv.points[:, 0]
#
#     ## Initialize a plotter object
#     plotter = pv.Plotter(window_size=[400,400])
#
#     ## Add mesh to the plotter
#     plotter.add_mesh(mesh_pv, scalars='myscalar', cmap='bwr', line_width=1)
#
#     ## Final touches
#     plotter.background_color = "black"
#     plotter.view_isometric()
#
#     ## Pass a key to avoid re-rendering at each time something changes in the page
#     stpyvista(plotter, key="pv_stl")




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

    # # STL-File dekomprimieren und als PyVista-Gitter laden
    # stl_file_data = decompress_data(model['stlFile'])
    # mesh = trimesh.load(BytesIO(stl_file_data), file_type="stl")
    # grid = pv.PolyData(mesh.vertices, mesh.faces)
    #
    # # Add some scalar field associated to the mesh
    # grid['myscalar'] = grid.points[:, 2]*grid.points[:, 0]
    #
    # # Initialize a plotter object
    # plotter = pv.Plotter(window_size=[400,400])
    #
    # # Add mesh to the plotter
    # plotter.add_mesh(grid, scalars='myscalar', cmap='bwr', line_width=1)
    #
    # # Final touches
    # plotter.background_color = "black"
    # plotter.view_isometric()
    #
    # # Pass a key to avoid re-rendering at each time something changes in the page
    # stpyvista(plotter, key="pv_stl")
    #
    # # Informationen zum Modell anzeigen
    # st.write("Name:", model['name'])
    # st.write("Beschreibung:", model['description'])
    # st.write("Tags:", model['tags'])
    # st.write("Autor:", model['author'])
    # st.write("Datum:", model['date'].strftime("%d.%m.%Y"))
    #
    # # 3D-Ansicht des Modells als STL-File
    # st.write("STL-File herunterladen:")
    # st.download_button(
    #     label="Download",
    #     data=stl_file_data,
    #     file_name=model['name']+".stl",
    #     mime="application/octet-stream"
    # )
    
    
    # Binärdaten des ausgewählten Modells abrufen
    model_data = collection.find_one({"name": model})["stlFile"]
    
    # Gzip-komprimierte Daten in ein BytesIO-Objekt laden
    model_io = io.BytesIO(model_data)
    with gzip.GzipFile(fileobj=model_io, mode="rb") as f:
        uncompressed_data = f.read()
    
    # STL-Modell aus den unkomprimierten Daten lesen
    model_file = io.BytesIO(uncompressed_data)
    mesh = pv.read(model_file, file_format="stl")
    
    # Plotter initialisieren
    plotter = pv.Plotter(window_size=[400, 400])
    
    # Mesh zum Plotter hinzufügen
    plotter.add_mesh(mesh)
    
    # Plotter anzeigen
    stpyvista(plotter)



# import streamlit as st
# import pyvista as pv
# from stpyvista import stpyvista
# import secret as s
# import io
# import gzip
#
# # Verbindung zur MongoDB-Datenbank herstellen
# client = s.client
# db = client["Website"]
# models_coll = db["Models"]
#
# # Alle Modelle aus der Datenbank abrufen
# models = list(models_coll.find())
#
# # Eine Liste der Modellnamen erstellen
# model_names = [model["name"] for model in models]
#
# # Modell auswählen
# model_name = st.selectbox("Select a model", model_names)
#
# # Binärdaten des ausgewählten Modells abrufen
# model_data = models_coll.find_one({"name": model_name})["stlFile"]
#
# # Gzip-komprimierte Daten in ein BytesIO-Objekt laden
# model_io = io.BytesIO(model_data)
# with gzip.GzipFile(fileobj=model_io, mode="rb") as f:
#     uncompressed_data = f.read()
#
# # STL-Modell aus den unkomprimierten Daten lesen
# model_file = io.BytesIO(uncompressed_data)
# mesh = pv.read(model_file, file_format="stl")
#
# # Plotter initialisieren
# plotter = pv.Plotter(window_size=[400, 400])
#
# # Mesh zum Plotter hinzufügen
# plotter.add_mesh(mesh)
#
# # Plotter anzeigen
# stpyvista(plotter)












if __name__ == '__main__':
    main()
 
 
    
    
    
# import streamlit as st
# import pyvista as pv
# from stpyvista import stpyvista

# ipythreejs does not support scalar bars :(
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



