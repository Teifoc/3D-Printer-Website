# import streamlit as st
# from io import BytesIO
# import pymongo
# import gzip
# from PIL import Image
# import trimesh
# import os
# from tempfile import NamedTemporaryFile
# import math
# import numpy as np
# import pyglet
# import secret as s
#
# os.environ["PYOPENGL_PLATFORM"] = "egl"
# import pyrender
#
# # Verbindung zur MongoDB herstellen
# s.client = pymongo.MongoClient("mongodb+srv://admin:KX2JOZ4N8M5IjQu0@3dmodeldatabase.1govbh4.mongodb.net/?retryWrites=true&w=majority")
#
# # Datenbank und Collection auswählen
# db = s.client['Website']
# collection = db['Models']
#
# # Cache für die Datenbankabfrage
# model_cache = {}
#
#
# # Funktionen für die Schaltflächen
# def select_model():
#     # Abfrage aller Modelle in der Collection
#     if 'models' not in model_cache:
#         model_cache['models'] = list(collection.find())
#     models = model_cache['models']
#
#     # Dropdown-Menü erstellen, um das Modell auszuwählen
#     model_names = [model['name'] for model in models]
#     selected_model_name = st.selectbox("Wähle ein Modell aus:", model_names)
#     # Das ausgewählte Modell zurückgeben
#     return next((model for model in models if model['name'] == selected_model_name), None)
#
#
# def decompress_data(compressed_data):
#     if compressed_data[:2] == b'\x1f\x8b':
#         # Daten sind gzip-komprimiert
#         data = gzip.decompress(compressed_data)
#     else:
#         data = compressed_data
#     return data
#
#
# import threading
#
#
# def render_model(stl_file_data):
#     try:
#         # STL-File laden und anzeigen
#         with NamedTemporaryFile(delete=False, suffix='.stl') as tmp_file:
#             tmp_file.write(stl_file_data)
#             mesh = trimesh.load(tmp_file.name)
#             scene = pyrender.Scene()
#             mesh_node = pyrender.Mesh.from_trimesh(mesh)
#             scene.add(mesh_node)
#             camera = pyrender.PerspectiveCamera(yfov=math.pi / 3.0, aspectRatio=1.0)
#             camera_pose = np.eye(4)
#             camera_pose[:3, 3] = np.array([0, 0, 2])
#             scene.add(camera, pose=camera_pose)
#
#             # Viewer starten
#             config = pyglet.gl.Config(double_buffer=True)
#             with pyglet.window.Window(config=config, visible=False):
#                 viewer = pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)
#                 pyglet.app.run()
#
#         os.unlink(tmp_file.name) # temporary file entfernen
#     except Exception as e:
#         st.error("Fehler beim Laden des 3D-Modells: {}".format(str(e)))
#
#
#
# # Streamlit-App
# def main():
#
#     pyglet.options['shadow_window'] = False
#     pyglet.options['debug_gl'] = False
#     pyglet.options['debug_gl_trace'] = False
#     pyglet.options['debug_gl_trace_args'] = False
#     pyglet.options['debug_gl_trace_stack'] = False
#     pyglet.options['gl_max_texture_size'] = 16384
#     pyglet.options['gl_min_texture_size'] = 1
#     pyglet.options['gl_extension_debug'] = False
#
#     st.title("3D-Modelle")
#
#     # Modell auswählen
#     model = select_model()
#     if model is None:
#         st.error("Kein Modell gefunden!")
#         return
#
#     # Bilddatei dekomprimieren und anzeigen
#     picture_data = decompress_data(model['picture'])
#     picture = Image.open(BytesIO(picture_data))
#     st.image(picture, caption="Bild des 3D-Modells")
#
#     # STL-File dekomprimieren und anzeigen
#     st.write("3D-Modell:")
#     stl_file_data = decompress_data(model['stlFile'])
#     render_model(stl_file_data)
#
#
# if __name__ == '__main__':
#     main()





import streamlit as st
from io import BytesIO
import pymongo
import gzip
from PIL import Image
import trimesh
import os
from tempfile import NamedTemporaryFile
import math
import numpy as np
import pyvista as pv
import secret as s

os.environ["PYOPENGL_PLATFORM"] = "egl"
import pyrender

# Verbindung zur MongoDB herstellen
client = s.client
# Datenbank und Collection auswählen
db = client['Website']
collection = db['Models']

# Cache für die Datenbankabfrage
model_cache = {}


# Funktionen für die Schaltflächen
def select_model():
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
    model = select_model()
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
    # mesh = trimesh.load(BytesIO(stl_file_data))
    # grid = pv.PolyData(mesh.vertices, mesh.faces)
    mesh = trimesh.load(BytesIO(stl_file_data), file_type="stl")
    grid = pv.PolyData(mesh.vertices, mesh.faces)


    # PyVista-Visualisierung anzeigen
    plotter = pv.Plotter()
    plotter.add_mesh(grid)
    plotter.show()


if __name__ == '__main__':
    main()
