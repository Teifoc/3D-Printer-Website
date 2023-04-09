import gzip
from tkinter import Tk, Label, Entry, Button, filedialog
import pymongo
import secret as s

# Verbindung zur MongoDB herstellen
client = s.client

# Datenbank und Collection auswählen

# Globale Variablen
picture_data_compressed = None
stl_file_data_compressed = None

# Funktionen für die Schaltflächen
def select_picture():
    global picture_data, picture_data_compressed
    picture_path = filedialog.askopenfilename(title="Bild des 3D-Modells auswählen")
    with open(picture_path, 'rb') as f:
        picture_data = f.read()
        picture_data_compressed = gzip.compress(picture_data)
        picture_button.config(text=picture_path)

def select_stl_file():
    global stl_file_data, stl_file_data_compressed
    stl_file_path = filedialog.askopenfilename(title="STL-File auswählen")
    with open(stl_file_path, 'rb') as f:
        stl_file_data = f.read()
        stl_file_data_compressed = gzip.compress(stl_file_data)
        stl_button.config(text=stl_file_path)

def upload_model_data():
    name = name_entry.get()
    preis = preis_entry.get()
    printTime = produktionsdauer_entry.get()

    # Daten in die MongoDB hochladen
    model_data = {
        "name": name,
        "picture": picture_data_compressed,
        "stlFile": stl_file_data_compressed,
        "price": preis,
        "printTime": printTime
    }

    result = client.Website.Models.insert_one(model_data)

    if result.acknowledged:
        result_label.config(text="Daten erfolgreich in die MongoDB hochgeladen.")
    else:
        result_label.config(text="Fehler beim Hochladen der Daten in die MongoDB.")

# GUI-Elemente erstellen
root = Tk()
root.title("3D-Modell hinzufügen")

name_label = Label(root, text="Name des 3D-Modells")
name_label.grid(row=0, column=0, padx=10, pady=10)
name_entry = Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

picture_button = Button(root, text="Bild auswählen", command=select_picture)
picture_button = Button(root, text="Bild auswählen", command=select_picture)
picture_button.grid(row=1, column=0, padx=10, pady=10)

stl_button = Button(root, text="STL-File auswählen", command=select_stl_file)
stl_button.grid(row=1, column=1, padx=10, pady=10)

preis_label = Label(root, text="Preis des 3D-Modells")
preis_label.grid(row=2, column=0, padx=10, pady=10)
preis_entry = Entry(root)
preis_entry.grid(row=2, column=1, padx=10, pady=10)

produktionsdauer_label = Label(root, text="Produktionsdauer")
produktionsdauer_label.grid(row=3, column=0, padx=10, pady=10)
produktionsdauer_entry = Entry(root)
produktionsdauer_entry.grid(row=3, column=1, padx=10, pady=10)

submit_button = Button(root, text="Daten hochladen", command=upload_model_data)
submit_button.grid(row=4, column=0, padx=10, pady=10)

result_label = Label(root, text="")
result_label.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()