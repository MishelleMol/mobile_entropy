import math
import zipfile
import pandas as pd

# Este archivo evalúa los bits FÍSICOS (antes del hashing).
# Solo lee archivos; no modifica bits_crudos.txt ni bits_acondicionados.txt.
#
# Limitaciones importantes:
# - Pasar estas pruebas no demuestra aleatoriedad verdadera; solo significa
#   que no se detectó ese tipo específico de problema.
# - Un balance 50/50 de ceros y unos NO implica independencia:
#   la secuencia 010101... está balanceada y es totalmente predecible.
# - Los valores p usan la aproximación normal, que es adecuada porque
#   tenemos decenas de miles de bits.

ALFA = 0.01


def leer_bits(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        texto = archivo.read().strip()
    return [int(caracter) for caracter in texto]


def valor_p_normal(z):
    # Valor p de dos colas para un estadístico z con distribución normal
    return math.erfc(abs(z) / math.sqrt(2))


def veredicto(p):
    if p < ALFA:
        return "NO PASA"
    return "PASA"


def prueba_balance(bits):
    # Prueba de frecuencia (monobit): ¿hay tantos unos como ceros?
    # Limitación: no mira el orden de los bits.
    n = len(bits)
    unos = sum(bits)
    ceros = n - unos
    z = (unos - ceros) / math.sqrt(n)
    return ceros, unos, z, valor_p_normal(z)


def correlacion_consecutiva(bits):
    # Correlación de Pearson entre cada bit y el siguiente.
    # Con bits independientes debería estar cerca de 0.
    # Limitación: solo detecta dependencia lineal entre vecinos inmediatos.
    a = bits[:-1]
    b = bits[1:]
    n = len(a)
    media_a = sum(a) / n
    media_b = sum(b) / n
    covarianza = sum((a[i] - media_a) * (b[i] - media_b) for i in range(n))
    var_a = sum((x - media_a) ** 2 for x in a)
    var_b = sum((x - media_b) ** 2 for x in b)
    r = covarianza / math.sqrt(var_a * var_b)
    # Si no hay correlación, r * raíz(n) se comporta aproximadamente como una normal
    z = r * math.sqrt(n)
    return r, z, valor_p_normal(z)


def prueba_rachas(bits):
    # Prueba de rachas de Wald-Wolfowitz (la misma fórmula que usa el notebook).
    # Una racha es un tramo seguido de bits iguales.
    # Pocas rachas: los bits se "pegan". Demasiadas: alternan artificialmente.
    # Limitación: no detecta patrones más largos que no cambien el número de rachas.
    n = len(bits)
    n1 = sum(bits)
    n0 = n - n1
    rachas = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            rachas += 1
    esperado = 2 * n0 * n1 / n + 1
    varianza = 2 * n0 * n1 * (2 * n0 * n1 - n) / (n ** 2 * (n - 1))
    z = (rachas - esperado) / math.sqrt(varianza)
    return rachas, esperado, z, valor_p_normal(z)


def analizar(nombre_archivo):
    bits = leer_bits(nombre_archivo)
    n = len(bits)

    print("\n==========", nombre_archivo, "==========")
    print("Cantidad total de bits:", n)

    ceros, unos, z, p = prueba_balance(bits)
    print("Ceros:", ceros, f"({ceros / n * 100:.2f} %)")
    print("Unos: ", unos, f"({unos / n * 100:.2f} %)")
    print(f"Balance (monobit): z = {z:.3f}   p = {p:.4g}   -> {veredicto(p)}")

    r, z, p = correlacion_consecutiva(bits)
    print(f"Correlación entre bits consecutivos: r = {r:+.4f}   z = {z:.2f}   p = {p:.4g}   -> {veredicto(p)}")

    rachas, esperado, z, p = prueba_rachas(bits)
    print(f"Rachas: observadas = {rachas}   esperadas = {esperado:.1f}")
    print(f"        z = {z:.3f}   p = {p:.4g}   -> {veredicto(p)}")


def correlacion_por_grabacion():
    # Repite el mismo extractor (signo del cambio) por cada grabación y eje,
    # para ver en qué condiciones los bits están más correlacionados.
    archivos = [
        "quieto1", "quieto2", "quieto3",
        "mano1", "mano2", "mano3",
        "movimiento1", "movimiento2", "movimiento3"
    ]

    print("\n========== Correlación entre bits consecutivos por grabación ==========")
    print(f"{'Grabación':<14}{'Eje x':>9}{'Eje y':>9}{'Eje z':>9}")

    for nombre in archivos:
        with zipfile.ZipFile("datos/" + nombre + ".zip", "r") as archivo_zip:
            with archivo_zip.open("Raw Data.csv") as archivo_csv:
                datos = pd.read_csv(archivo_csv)

        fila = f"{nombre:<14}"
        for eje in ["x", "y", "z"]:
            cambios = datos[f"Linear Acceleration {eje} (m/s^2)"].diff().dropna()
            bits = [1 if cambio > 0 else 0 for cambio in cambios]
            r, z, p = correlacion_consecutiva(bits)
            fila += f"{r:>+9.3f}"
        print(fila)

    print("Referencia: para cambios de ruido independiente se espera alrededor de -0.33,")
    print("porque dos cambios seguidos comparten una medición.")


analizar("bits_crudos.txt")
analizar("bits_acondicionados.txt")
correlacion_por_grabacion()

print(f"\nNivel de significancia usado: {ALFA}")
print("Recuerde: pasar una prueba no demuestra aleatoriedad; fallarla sí indica un problema.")
