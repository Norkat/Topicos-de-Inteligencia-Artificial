# Optimizacion de localizacion de sensores para sistemas de riego
## Integrantes
- Payan Urquidez Rafael Alberto
- Quiñonez Ramirez Nestor de Jesus

## Resumen
Este proyecto tiene el objetivo de optimizar la ubicación de sensores de humedad en campos agrícolas de la región de Guasave, Sinaloa, mediante la implementación del algoritmo de Enjambre de Partículas (PSO), con el fin de mejorar la eficiencia del riego y el aprovechamiento de los recursos hídricos.

## Datos de Entrada
Los datos de entrada son los archivos csv proporcionados en la carpeta data, es necesario localizar
el script main junto a la carpeta data y el resto de scripts antes de ejecutarlo.
Los archivos csv contienen los siguientes datos
- Humedad del punto de cultivo representado en porcentaje (0 - 100)
- Tipo de Cultivo plantado en el punto especifico. El cultivo puede ser Chile, Tomate o Maíz.
- Elevación del punto de cultivo. Tipo de dato medio en metros (m).
- Salinidad del punto de cultivo. Tipo de dato medido en dS/m.
- Temperatura del punto de cultivo. Medido en grados Celcius (C°).
- Coordenadas geograficas de cada punto (latitud y longitud).
Tambien hay un tipo de prueba el cual no requiere un archivo csv, ya que este funciona generando
datos aleatorios para toda la información.

## Resultados
Para los resultados tenemos dos tipos de forma de reportarlos.
- Reporte por Consola. En consola se imprime la siguiente información:
  - La mejor solución encontrada. Un arreglo bidimensional de sensores de tamaño n x 2. Donde n es la cantidad de sensores.       Los dos atributos con las coordenadas donde esta ubicado el sensor (Latitud y Longitud).
  - El valor calculado por la funcion objetivo que representa la mejor solución.
  - Un arreglo de valores donde se encuentra el mejor valor encontrado que hubo por iteración.
- Reporte grafico. Se muestran dos tipos de graficas para mostrar los resultados:
  - Una grafica que muestra la mejor solución global encontrada por cada iteración donde se puede apreciar como va mejorando la solución encontrada.
  - Un plano cartesiano donde se ven graficado los puntos de cultivo junto a los sensores para que se pueda apreciar de forma grafica la solución

## Dependencias
Instalar pandas para la lectura de datos en csv y el uso de dataframes.
Instalar numpy para el uso de sus vectores y funciones avanzadas.
Instalar matplotlib para el uso de graficas visuales.
```bash
pip install numpy pandas matplotlib
