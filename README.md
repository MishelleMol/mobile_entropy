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

5. **Conclusión**: Se pudo observar a lo largo de las pruebas que el sistema diseñado si representa un "true randomness", que da numeros aleatorios por medio de la recolección de datos externos y el manejo de los mismos mediante un hashing.

## Justificación del Método de Captura
Como se mecionó anteriormente, se ralizaron 9 tomas de datos mediante la aplicación Phyphox, a una tasa de muestreo de aproximadamente 100 Hz durante sesiones de captura en tres condicones: reposo, en mano y en movimiento. Esta tasa permitió registrar cientos de miles de fluctuaciones analógicas infinitesimales generadas por el movimiento involuntario. Estos datos físicos sirvieron como una semilla altamente volatil que luego fue condicionada para alimentar al extractor SHA-256, logrando cubrir ampliamente los 160K enteros requeridos sin sesgos de muestreo.

## Escalabilidad y análisis de costos
Para que el proyecto pueda generar números aleatorios cada segundo durante todo un año, se propone mejorar el sistema actual de la siguiente manera:

1. **Raspberry Pi:** En lugar de utilizar un teléfono, se utilizará una Raspberry Pi 4, ya que es pequeña, consume poca energía y tiene suficiente capacidad para ejecutar el código de Python continuamente.

2. **Sensor de aceleración:** Se utilizará un sensor conectado directamente a la Raspberry Pi, capaz de tomar 100 mediciones por segundo. Además, tendremos dos sensores de repuesto.

3. **Almacenamiento SSD:** Se utilizará un SSD para guardar el sistema operativo y evitar el desgaste de las tarjetas de memoria tradicionales.

4. **Procesamiento en RAM:** Los datos del sensor se procesarán directamente en la memoria RAM, sin necesidad de guardar archivos intermedios. Esto permitirá trabajar más rápido y reducir el desgaste del almacenamiento.

5. **Entrega de números:** Se mantendrán números previamente procesados en memoria para que el sistema pueda entregarlos cada segundo mediante una API local, sin tener que esperar a que se generen en ese momento.

### Presupuesto del proyecto
El presupuesto se divide en dos partes: **CapEx**, que representa la inversión inicial en los componentes, y **OpEx**, que corresponde a los gastos necesarios para mantener el sistema funcionando.

| Componente | Tipo | Costo (USD) |
|---|---|---:|
| Raspberry Pi 4 (4 GB) | CapEx | $75.00 |
| 3 sensores de aceleración | CapEx | $15.00 |
| SSD de 120 GB | CapEx | $25.00 |
| Batería de respaldo (Mini-UPS) | CapEx | $40.00 |
| Caja protectora y cables | CapEx | $20.00 |
| Electricidad anual | OpEx | $12.50 |
| Mantenimiento anual | OpEx | $30.00 |
| **Total estimado del primer año** | | **$217.50** |

Esta propuesta busca que el proyecto sea económicamente rentable, que no priorice ni la generación de números ni el consumo monetario, sino que sea una balanza entre ambos y que, sobretodo, no esté lejos del alcance de estudiantes como nosotros. Por eso este sistema consume poca energía y puede funcionar sin depender de un teléfono móvil.