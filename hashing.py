import hashlib
import csv

#Leemos el archivo 
with open('bits_acondicionados.txt', 'r') as datos:
    base = datos.read()

# variables en las que luego se agregan cosas
bits_totales =''
enteros = []

# 1er for: para hacer el hash. el 4100 es porque es la cantidad que se necesitan para sacar suficientes bits para luego generar 160k enteros
for contador in range(4100):
    h = hashlib.sha256((base + str(contador)).encode('utf-8')).hexdigest()
    bits_256 = bin(int(h, 16))[2:].zfill(256)
    bits_totales += bits_256
print(len(bits_totales))

# 2do for: para vovler cada 4 bits un entero
for b in range (0, len(bits_totales), 4):
    v_bits = bits_totales[b: b+4]
    i_bits = int(v_bits, 2)
    
    if i_bits < 10:
        enteros.append(i_bits)
    
print (len(enteros))
enteros = enteros[:160000]

# lo guardamos en un csv
with open('enteros.csv', 'w', newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(enteros)
    print('guardado en csv')

