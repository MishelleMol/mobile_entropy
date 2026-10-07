import zipfile
import pandas as pd
import matplotlib.pyplot as plt

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

variaciones = []

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

    # Calculamos cuánto varía cada eje
    variacion_x = datos["Linear Acceleration x (m/s^2)"].std()
    variacion_y = datos["Linear Acceleration y (m/s^2)"].std()
    variacion_z = datos["Linear Acceleration z (m/s^2)"].std()
    #.std() calcula desviación estándar: Esto nos permite comprobar con datos si quieto, mano y movimiento producen cantidad diferentes de variación


    # Mostramos los resultados
    print("Variación X:", variacion_x)
    print("Variación Y:", variacion_y)
    print("Variación Z:", variacion_z)

    # Calculamos la variación promedio de los tres ejes
    variacion_promedio = (variacion_x + variacion_y + variacion_z) / 3

    print("Variación promedio:", variacion_promedio)

    variaciones.append(variacion_promedio)

    
# Gráfica para comparar la variación de las 9 pruebas
plt.figure(figsize=(10, 5))

plt.bar(archivos, variaciones)

plt.title("Variación promedio de aceleración")
plt.xlabel("Prueba")
plt.ylabel("Variación promedio")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()  