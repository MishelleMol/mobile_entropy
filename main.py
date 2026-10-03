import zipfile
import pandas as pd

# Lista con las 9 pruebas realizadas
archivos = [
    "quieto1.zip",
    "quieto2.zip",
    "quieto3.zip",
    "mano1.zip",
    "mano2.zip",
    "mano3.zip",
    "movimiento1.zip",
    "movimiento2.zip",
    "movimiento3.zip"
]

# Recorremos cada prueba
for nombre in archivos:

    # Buscamos el archivo dentro de la carpeta datos
    ruta = "datos/" + nombre

    # Abrimos el archivo ZIP
    with zipfile.ZipFile(ruta, "r") as zip:

        # Abrimos el CSV que está dentro
        with zip.open("Raw Data.csv") as csv:

            # Convertimos el CSV en una tabla
            datos = pd.read_csv(csv)

    # Mostramos el nombre de la prueba
    print("\nPrueba:", nombre)

    # Mostramos cuántas mediciones contiene
    print("Cantidad de mediciones:", len(datos))