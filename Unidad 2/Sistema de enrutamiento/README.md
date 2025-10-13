# Sistema de Enrutamiento
## Integrantes
- Payan Urquidez Rafael Alberto
- Quiñonez Ramirez Nestor de Jesus

## Resumen
Este proyecto aborda una versión extendida del Problema del Viajante (TSP) en un contexto logístico real, 
donde existen múltiples centros de distribución y un conjunto de tiendas. 
El objetivo es generar rutas eficientes que minimicen la distancia total recorrida, respetando que cada 
ruta comience y termine en un centro de distribución.
Se implementó la técnica de optimización heurística:
- Tabu Search con operador *relocate* para mover clientes entre rutas, evitando ciclos y mejorando la solución iterativamente.

## Datos de Entrada
Los datos de entrada son los archivos csv proporcionados en la carpeta, es necesario localizar
el programa junto a ambos archivos antes de ejecutarlos.
- Una matriz de distancias entre todos los nodos (centros y tiendas).  
- Un listado de centros de distribución y tiendas, incluyendo nombre y coordenadas.

## Resultados
- Se obtuvieron soluciones que minimizan la distancia total recorrida.  
- Cada ruta comienza y termina en su centro de distribución asignado.  
- El algoritmo permite flexibilidad: algunas rutas pueden quedar sin tiendas si no contribuyen a la reducción de coste.

## Dependencias
Instalar pandas
```bash
pip install pandas numpy
