import zipfile
import pandas as pd

# Archivos con las mediciones del acelerómetro
archivos = [
    "datos/quieto1.zip",
    "datos/quieto2.zip",
    "datos/quieto3.zip",
    "datos/mano1.zip",
    "datos/mano2.zip",
    "datos/mano3.zip",
    "datos/movimiento1.zip",
    "datos/movimiento2.zip",
    "datos/movimiento3.zip"
]

# Lista donde guardaremos todos los cambios
todos_los_cambios = []

# Recorremos cada archivo
for archivo in archivos:

    # Abrimos el archivo ZIP
    with zipfile.ZipFile(archivo, "r") as zip:

        # Abrimos las mediciones del acelerómetro
        with zip.open("Raw Data.csv") as csv:

            # Convertimos las mediciones en una tabla
            datos = pd.read_csv(csv)

    # Tomamos las mediciones de los tres ejes
    eje_x = datos["Linear Acceleration x (m/s^2)"]
    eje_y = datos["Linear Acceleration y (m/s^2)"]
    eje_z = datos["Linear Acceleration z (m/s^2)"]

    # Calculamos los cambios de cada eje
    cambios_x = eje_x.diff().dropna()
    cambios_y = eje_y.diff().dropna()
    cambios_z = eje_z.diff().dropna()

    # Guardamos los cambios de los tres ejes
    todos_los_cambios.extend(cambios_x)
    todos_los_cambios.extend(cambios_y)
    todos_los_cambios.extend(cambios_z)


# Mostramos información de los cambios
print("\nCantidad total de cambios:", len(todos_los_cambios))

print("\nPrimeros 10 cambios:")
print(todos_los_cambios[:10])


# Lista donde guardaremos los bits
bits = []

# Recorremos todos los cambios
for cambio in todos_los_cambios:

    # Si el cambio es positivo, guardamos 1
    if cambio > 0:
        bits.append(1)

    # Si el cambio es negativo o cero, guardamos 0
    else:
        bits.append(0)


# Mostramos los primeros 50 bits
print("\nPrimeros 50 bits:")
print(bits[:50])


# Contamos cuántos bits generamos
cantidad_bits = len(bits)

# Contamos cuántos ceros y unos tenemos
cantidad_ceros = bits.count(0)
cantidad_unos = bits.count(1)

print("\nCantidad total de bits:", cantidad_bits)
print("Cantidad de 0:", cantidad_ceros)
print("Cantidad de 1:", cantidad_unos)



# Lista donde guardaremos los bits acondicionados
bits_acondicionados = []

# Recorremos los bits de dos en dos
for i in range(0, len(bits) - 1, 2):

    primer_bit = bits[i]
    segundo_bit = bits[i + 1]

    # Si tenemos 01, guardamos 0
    if primer_bit == 0 and segundo_bit == 1:
        bits_acondicionados.append(0)

    # Si tenemos 10, guardamos 1
    elif primer_bit == 1 and segundo_bit == 0:
        bits_acondicionados.append(1)

    # Los pares 00 y 11 se descartan


# Mostramos los resultados después del acondicionamiento
print("\nDESPUÉS DEL ACONDICIONAMIENTO")
print("Cantidad de bits:", len(bits_acondicionados))
print("Cantidad de 0:", bits_acondicionados.count(0))
print("Cantidad de 1:", bits_acondicionados.count(1))

print("\nPrimeros 50 bits acondicionados:")
print(bits_acondicionados[:50])


# Calculamos el porcentaje de 0 y 1 antes del acondicionamiento
porcentaje_ceros_antes = bits.count(0) / len(bits) * 100
porcentaje_unos_antes = bits.count(1) / len(bits) * 100

# Calculamos el porcentaje de 0 y 1 después del acondicionamiento
porcentaje_ceros_despues = (
    bits_acondicionados.count(0) / len(bits_acondicionados) * 100
)

porcentaje_unos_despues = (
    bits_acondicionados.count(1) / len(bits_acondicionados) * 100
)


print("\nANTES DEL ACONDICIONAMIENTO")
print("Porcentaje de 0:", porcentaje_ceros_antes)
print("Porcentaje de 1:", porcentaje_unos_antes)

print("\nDESPUÉS DEL ACONDICIONAMIENTO")
print("Porcentaje de 0:", porcentaje_ceros_despues)
print("Porcentaje de 1:", porcentaje_unos_despues)

# Convertimos los bits en texto
bits_texto = ""

for bit in bits_acondicionados:
    bits_texto = bits_texto + str(bit)

# Guardamos los bits en un archivo
with open("bits_acondicionados.txt", "w") as archivo_salida:
    archivo_salida.write(bits_texto)

print("\nBits acondicionados guardados en bits_acondicionados.txt")

bits_crudos_texto = ""

for bit in bits:
    bits_crudos_texto = bits_crudos_texto + str(bit)

with open("bits_crudos.txt", "w") as archivo_salida:
    archivo_salida.write(bits_crudos_texto)

print("Bits crudos guardados en bits_crudos.txt")