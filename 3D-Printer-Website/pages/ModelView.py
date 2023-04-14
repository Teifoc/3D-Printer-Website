#

# import gzip
# import tempfile
# import streamlit as st
# import pyvista as pv
# import secret as s
#
# # Verbindung zur MongoDB herstellen
# client = s.client
# db = client["Website"]
# collection = db["Models"]
#
# # Liste von verfügbaren 3D-Modellen aus der Datenbank abrufen
# model_names = [doc["name"] for doc in collection.find({}, {"name": 1})]
#
# # Dropdown-Menü zur Auswahl eines Modells erstellen
# model_name = st.selectbox("Wähle ein Modell aus", model_names)
#
# # STL-Datei des ausgewählten Modells aus der Datenbank laden und entpacken
# model_doc = collection.find_one({"name": model_name})
# stl_bytes = gzip.decompress(model_doc["stlFile"])
#
# # Bytes der STL-Datei in eine temporäre Datei schreiben
# with tempfile.NamedTemporaryFile(delete=False) as temp_file:
#     temp_file.write(stl_bytes)
#     temp_file.flush()
#
#     # PyVista-Gitter aus der temporären Datei laden
#     mesh = pv.read(temp_file.name)
#
#     # Temporäre Datei löschen
#     temp_file.unlink(temp_file.name)
#
# # 3D-Modell mit PyVista anzeigen
# plotter = pv.Plotter()
# plotter.add_mesh(mesh, show_edges=True)
# plotter.show()



# import streamlit as st
# import pyvista as pv
# from stpyvista import stpyvista
# import secret as s
#
# # Verbindung zur MongoDB-Datenbank herstellen
# client = s.client
# db = client["Website"]
# models_coll = db["Models"]
#
#
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

import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

# pythreejs does not support scalar bars :(
pv.global_theme.show_scalar_bar = False 

## Initialize a plotter object
plotter = pv.Plotter(window_size=[400,400])

## Create a mesh with a cube 
mesh = pv.Cube(center=(0,0,0))

## Add some scalar field associated to the mesh
mesh['myscalar'] = mesh.points[:, 2]*mesh.points[:, 0]

## Add mesh to the plotter
plotter.add_mesh(mesh, scalars='myscalar', cmap='bwr', line_width=1)

## Final touches
plotter.view_isometric()
plotter.add_scalar_bar()
plotter.background_color = 'white'

## Pass a key to avoid re-rendering at each time something changes in the page
stpyvista(plotter, key="pv_cube")

import streamlit as st
import pyvista as pv
from stpyvista import stpyvista
import secret as s
import io
import gzip

# Verbindung zur MongoDB-Datenbank herstellen
client = s.client
db = client["Website"]
models_coll = db["Models"]

# Alle Modelle aus der Datenbank abrufen
models = list(models_coll.find())

# Eine Liste der Modellnamen erstellen
model_names = [model["name"] for model in models]

# Modell auswählen
model_name = st.selectbox("Select a model", model_names)

# Binärdaten des ausgewählten Modells abrufen
model_data = models_coll.find_one({"name": model_name})["stlFile"]

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






