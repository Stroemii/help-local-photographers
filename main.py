from PIL import Image
import os
import pyqrcode
import png

# Aufgabe:
# 
# Wir möchten den Workflow für einen Fotografen automatisieren. 
# 
# Als Ausgangsbasis können wir hierzu den Code von "08 - Teil 08" verwenden, wo 
# bisher nur unser Logo auf dem Bild platziert wurde.
# 
# Wie könnte dieser Workflow insgesamt aussehen?
#
# - Ein Ordner mit Bildern soll eingelesen werden (hier: "../Bilder")
# - Die Original-Version des Bildes (48MP) soll herunterskaliert werden, sodass wir diese
#   Bilder später einfacher versenden können
# - Auf jedem Bild soll ein QR-Code mit einem Link zu unserer Webseite auf dem Bild 
#   platziert werden, sowie das Logo von unserer Firma (logo2.png) 
# - Die Ausgabe-Bilder sollen dann in einem neuen Ordner hineingeschrieben werden (als .jpg)
#
# Tipp: Generiere den QR-Code vorab, und speichere ihn als Datei z.B. im aktuellen Ordner 
#       ab. Anschließend kannst du ihn mit Pillow einlesen (Image.open).

####################
# QR-Code erstellen
url = pyqrcode.create('https://www.loremipsum.de/')
# QR-Code als PNG speichern
url.png('qr_code.png', scale=8)

# Dateipfade für Bilder und Bilder-Versand-Ordner (Ziel) in Variablen abspeichern
IMAGE_FOLDER = 'C:/Users/Stroemi/Desktop/Python-Einstieg/Kursmaterialien/07 - pillow/11 - Teil 11/Bilder'
BILDER_VERSAND = os.path.join(IMAGE_FOLDER, 'Bilder_Versand')

# Neuen Ordner anlegen, in welchem die bearbeiteten Bilder abgespeichert werden sollen
if not os.path.isdir(os.path.join(BILDER_VERSAND)):
    os.mkdir(BILDER_VERSAND)


# Alle Bilder im Ordner ermitteln (Ornder aussortieren)...
for image in os.listdir(IMAGE_FOLDER):
    image_path = os.path.join(IMAGE_FOLDER, image)
    if os.path.isfile(image_path):  # wenn Datei ein File (also Bild) ist, dann...
        with Image.open(image_path) as im, Image.open('qr_code.png') as qr_code, Image.open("logo2.png") as logo:           # ... Bild, QR-Code mit Image.open öffnen
            width, height = im.size                  # Größe des Bildes in Variablen abspeichern
            if width > 400:                  # wenn die Breite des Bildes größer als 400 Pixel, soll das Bild verkleinert werden...
                new_width = 400                     # auf 400 Pixel
                new_height = int(height / (width / new_width))          # die Höhe des Bildes soll im gleichen Maßstab (also Weite/neue Weite) verkleinert werden
            else:
                new_width = width
                new_height = height                 # Wenn das Bild schmaler als 400 Pixel ist, soll es gleich bleiben
            #print(new_height, new_width)

            im = im.resize((new_width, new_height)) # das Bild anhand der neuen Abmaße neu skaliert
            #print(im, qr_code)
            
            # QR-Code:
            size_qr_code = int(new_width / 5)           # Kantenlänge des QR-Codes soll ein fÜNFTEL der Breite des Bildes betragen
            qr_code = qr_code.resize((size_qr_code, size_qr_code))      # Resizing des QR-Codes
            
            # print(qr_code)
            
            # nächster Schritt: QR-Code einfügen:
            im.paste(qr_code, (0, (new_height-size_qr_code)))           # QR-Code soll in der unteren linken Ecke sein (also Position Bilderhöhe minus QR-Code-Size)
            
            width_logo, height_logo = logo.size                         # Logo-Sizes abspeichern
            new_width_logo = int(new_width / 2)                         # Logo-Breite soll halb so breit sein, wie das Bild
            
            new_height_logo = int(height_logo / (width_logo / new_width_logo))  # Höhe des Logos soll entsprechend dem Verkleinerung der Breite angepasst werden
            logo = logo.resize((new_width_logo, new_height_logo))       # Logo-Resizing

            im.paste(logo, (new_width_logo, new_height-new_height_logo), logo)

            im.save(os.path.join(BILDER_VERSAND, image))                # Bild abspeichern

