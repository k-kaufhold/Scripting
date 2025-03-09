#!/bin/bash

# Verzeichnis für Downloads
downloads=~/Downloads
bilder_ordner="$downloads/Bilder"

# Prüfen, ob Bilddateien existieren
if find "$downloads" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.bmp" -o -iname "*.webp" \) | grep -q .; then
    # Falls der Bilder-Ordner nicht existiert, erstelle ihn
    [ -d "$bilder_ordner" ] || mkdir "$bilder_ordner"
    
    # Verschiebe die Bilder in den Ordner
    find "$downloads" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.bmp" -o -iname "*.webp" \) -exec mv {} "$bilder_ordner" \;
    
    echo "Bilddateien wurden nach $bilder_ordner verschoben."
else
    echo "Keine Bilddateien gefunden."
fi

