import streamlit as st
from io import BytesIO
import gzip
from PIL import Image
import pyrender
import trimesh
import os
from tempfile import NamedTemporaryFile
import math
import numpy as np
import pyglet
import threading
import secret as s # Moduke sexret not fdound, aber vorhanden (DB-ZUgänge) --> prüfen

# Verbindung zur MongoDB herstellen
client = s.client

# Datenbank und Collection auswählen
db = client['Website']
collection = db['Models']

# Funktionen für die Schaltflächen
def select_model():
    # Abfrage aller Modelle in der Collection
    models = list(collection.find())
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


def render_model(stl_file_data):
    try:
        # STL-File laden und anzeigen  
        with NamedTemporaryFile(delete=False, suffix='.stl') as tmp_file:
            tmp_file.write(stl_file_data)
            tmp_file.close() # temporäre Datei schließen

            mesh = trimesh.load(tmp_file.name)
            scene = pyrender.Scene()
            mesh_node = pyrender.Mesh.from_trimesh(mesh)
            scene.add(mesh_node)
            camera = pyrender.PerspectiveCamera(yfov=math.pi / 3.0, aspectRatio=1.0)
            camera_pose = np.eye(4)
            camera_pose[:3, 3] = np.array([0, 0, 2])
            scene.add(camera, pose=camera_pose)

            # Pyrender-Viewer erstellen und anzeigen
            r = pyrender.OffscreenRenderer(viewport_width=800, viewport_height=800)
            color, _ = r.render(scene)
            image = Image.fromarray(color)
            st.image(image, caption="3D-Modell")

            os.unlink(tmp_file.name) # temporary file entfernen
    except Exception as e:
        st.error("Fehler beim Laden des 3D-Modells: {}".format(str(e)))

# Handler für das Ereignis "on_close"
def close_viewer():
    pyglet.app.exit()


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

    # STL-File dekomprimieren und anzeigen
    st.write("3D-Modell:")
    stl_file_data = decompress_data(model['stlFile'])
    if st.button("View Model"):
        global viewer_thread
        viewer_thread = threading.Thread(target=render_model, args=(stl_file_data,))
        viewer_thread.start()

    # Prüfen, ob der Viewer-Thread noch läuft und ihn beenden, wenn der Nutzer die Seite verlässt
    if 'viewer_thread' in globals() and viewer_thread.is_alive():
        if st.button("Viewer schließen"):
            viewer_thread.stop()

       
if __name__ == '__main__':
     main()