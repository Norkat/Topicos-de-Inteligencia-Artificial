# Solucionador del Problema del Viajante (TSP) con Algoritmo Genético

Este proyecto implementa un **Algoritmo Genético (AG)** para encontrar una solución cercana a la óptima para el clásico **Problema del Viajante (Travelling Salesperson Problem, TSP)**. El TSP busca la ruta más corta posible que visita un conjunto de municipios (ciudades) y regresa al municipio de origen.

---

## Descripción del Algoritmo Genético

Un **Algoritmo Genético (AG)** es una técnica de optimización inspirada en el proceso de **selección natural y la genética evolutiva**. Es un potente método heurístico para resolver problemas de optimización, especialmente aquellos donde el espacio de soluciones es demasiado grande para ser explorado completamente (como el TSP).

El algoritmo opera sobre una población de posibles soluciones (llamadas **individuos** o **rutas** en este contexto) y las mejora a lo largo de múltiples **generaciones** mediante los siguientes pasos principales:

1.  **Población Inicial:** Se crean soluciones aleatorias.
2.  **Función de Aptitud (Fitness):** Cada ruta se evalúa. En el TSP, la aptitud es inversamente proporcional a la distancia total de la ruta (una distancia más corta significa una aptitud más alta).
3.  **Selección:** Las rutas con mayor aptitud son seleccionadas para la reproducción. Este código usa una combinación de **Elitismo** (los mejores pasan directamente) y **Selección por Ruleta**.
4.  **Cruce (Crossover):** Los individuos seleccionados se "cruzan" para generar nuevos **hijos**. Se utiliza un método de cruce ordenado (`Ordered Crossover - OX`) para asegurar que todos los municipios sean visitados exactamente una vez.
5.  **Mutación:** Se introduce una pequeña probabilidad de que los genes (municipios en la ruta) de un hijo sean intercambiados aleatoriamente (`Swap Mutation`) para explorar nuevas soluciones y evitar caer en óptimos locales.
6.  **Nueva Generación:** Los nuevos hijos reemplazan a la población anterior, y el proceso se repite hasta alcanzar el número máximo de generaciones.

---

## Dependencias y Bibliotecas

Este script de Python utiliza varias bibliotecas estándar para realizar cálculos numéricos, manipulación de datos y visualización.

Necesitas tener **Python 3.x** instalado. Las siguientes librerías de terceros son requeridas y deben ser instaladas:

| Librería     | Propósito                                                                | Comando de Instalación   |
| :----------- | :----------------------------------------------------------------------- | :----------------------- |
| `numpy`      | Funciones matemáticas y manipulación de arrays.                          | `pip install numpy`      |
| `pandas`     | Manipulación de estructuras de datos (usado en la Selección por Ruleta). | `pip install pandas`     |
| `matplotlib` | Generación de gráficos para visualizar el progreso y la ruta final.      | `pip install matplotlib` |

Una vez que tengas Python, puedes instalar todas las dependencias con el siguiente comando:

```bash
pip install numpy pandas matplotlib
```
