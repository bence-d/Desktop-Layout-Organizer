import os

# Pfad 
src = "C:/Users/Bence/Onedrive - HTBLA Leonding/Schule"

# Alle Files unter dem Pfad in einem Array speichern
entries = os.listdir(src)

# Ausgeben von allen Files von Ordner definiert unter
for file in entries:
   print(file)


