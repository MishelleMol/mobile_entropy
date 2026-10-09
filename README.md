# mobile_entropy

## Estructura del Proyecto
* Se tiene una carpeta de datos en la cual se encuentran 9 carpetas comprimidas .zip, las cuales forman parte de las pruebas realizadas utilizando el sensor de inercia del teléfono. Para capturar estos datos se utilizó la aplicación Phyphox bajo tres escenarios: sosteniendo el teléfono en la mano, con el dispositivo en movimiento y con el dispositivo quieto.
* En el archivo `main.py` se miden las variaciones en cada uno de los ejes para evaluar si los datos recolectados son de utilidad para el objetivo del proyecto. Dentro de este script se leen los archivos comprimidos mediante la librería zipfile y se procesan las lecturas para calcular las variaciones, mostrándolas posteriormente en gráficas con matplotlib.
* El archivo `extractor.py` constituye la primera capa de la lógica del sistema. De forma similar, lee los archivos .zip, extrae las mediciones de los tres ejes, calcula las diferencias respecto al valor anterior en cada eje y guarda estos resultados en una carpeta intermedia. Luego, dicha carpeta se recorre para extraer bits dependiendo de si el cambio calculado es positivo, cero o negativo. Estos bits crudos se almacenan en el archivo `bits_crudos.txt`. A continuación se aplica un procedimiento de acondicionamiento donde se filtran los datos y se descartan los bits pares para reducir correlaciones, guardando el resultado en `bits_acondicionados.txt`. Por último, se calculan los porcentajes de ceros y unos para inspeccionar el balance de los datos.
* El archivo `hashing.py` representa el siguiente nivel de la arquitectura. Su uso es necesario debido a que, tras el acondicionamiento, la cantidad de bits útiles disminuyó y se requería alcanzar la meta de 160,000 enteros. En este archivo se ejecuta un primer ciclo con 4,100 iteraciones para obtener suficientes bits de salida; en cada iteración se genera el hash SHA-256 de una cadena formada por los bits acondicionados como base junto con un contador incremental. Un segundo ciclo agrupa el flujo resultante en bloques de 4 bits, los cuales representan valores enteros del 0 al 15. Por diseño del proyecto, se aplica muestreo por rechazo para conservar únicamente los números en el rango de 0 a 9. Finalmente, se trunca la secuencia a exactamente 160,000 muestras y se exporta en el archivo `enteros.csv`.
* En el notebook de evaluación provisto se ejecutaron las pruebas correspondientes, las cuales validaron el correcto funcionamiento del pipeline. La secuencia superó las pruebas estadísticas de uniformidad (Chi-cuadrado), rachas y pares consecutivos, además de presentar un patrón de ruido estático homogéneo en la prueba visual de 400 × 400 píxeles.

## Resultados del verificador
A continuación se mostrarán los resultados y un péqueño análisis de cada prueba

1.  **Chi Cuadrado**: 
    ![Chi cuadrado](images/chi_cuadrado.png)
    Se observa que hay varios puntos distribuidos en diferentes zonas de la gráfica y ninguno muestra una forma clara lo que demuestra la aleatoriedad del sistema. Además, todos entran dentro de la desviación estandar.

2. **Rachas**: 
    ![Rachas](images/rachas.png)
    Se logra observar como como los puntos azules logran caer sobre toda la linea punteada. Esto confirma que los números no se quedan pegados en secuencias repetitivas ni alternan de manera artificial

3. **Pares Consecutivos**:
    'Niveles: 10   Combinaciones: 100   Frecuencia esperada por combinación: 800.0
    Estadístico chi cuadrado: 109.41   Grados de libertad: 99
    p-valor: 0.2228
    Veredicto: PASA'
    Gracias a esta prueba se puede ntoar que no hay valores que condicionen al siguiente ni dependencias entre valores adyacentes. Cada número es estadísticamente independiente del anterior.

4. **Prueba Visual** 
    ![Prueba Visual](images/prueba_visual.png)
    Gracias a esta prueba es donde se puede ver de manera clara el funcionamiento del sistema. En comparación con el cuadro de referencian no se notan diferencias, en la imagen del sistema se ve un ruido uniforme que no tiene ninguna estructura ni zonas con ciertas tendencias. 
    ![Mapa de Pares](images/mapa_de_pares.png)
    Esta prueba muestra un cuadro homogéneo en gris sin líneas, rejillas, diagonales o huecos oscuros. Cada celda de la cuadrícula se iluminó de forma balanceada, confirmando que la probabilidad de transición de cualquier número hacia el siguiente es uniforme y no está condicionada.

5. **Conclusión**: Se pudo observar a lo largo de las pruebas que el sistema diseñado si representa un true randomness, que da numeros aleatorios por medio de la recolección de datos externos y el manejo de los mismos mediante un hashing.
