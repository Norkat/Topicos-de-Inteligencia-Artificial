## 📄 Documentación Técnica y Manual de Instalación LPR

Este documento detalla la arquitectura, especificaciones técnicas y los procedimientos de instalación y despliegue del subsistema de Reconocimiento de Placas (LPR), basado en **Ultralytics YOLOv8** y **PyTesseract (OCR)**.

---

## 1\. ⚙️ Manual de Instalación y Configuración

Esta sección guía a los administradores de sistemas a través de la configuración inicial de las dependencias y el despliegue del entorno de desarrollo/producción.

### 1.1. Requisitos Previos del Sistema

| Requisito             | Descripción                                    | Notas                                                                              |
| :-------------------- | :--------------------------------------------- | :--------------------------------------------------------------------------------- |
| **Sistema Operativo** | Linux (Ubuntu 20.04+), Windows 10/11, o macOS. | Se recomienda Linux para despliegues en producción.                                |
| **Python**            | Versión 3.11 o superior.                       | Necesario para las librerías `ultralytics` y `opencv-python`.                      |
| **Tesseract OCR**     | Motor Tesseract OCR.                           | Debe estar instalado a nivel de sistema operativo para que `pytesseract` funcione. |
| **NVIDIA CUDA**       | Toolkit 11.8+ y cuDNN 8+                       | **Opcional:** Necesario solo para el entrenamiento y la inferencia rápida con GPU. |

### 1.2. Instalación de Dependencias de Software

#### 1.2.1. Instalación del Motor Tesseract OCR

El motor Tesseract debe instalarse primero a nivel del sistema.

- **En Debian/Ubuntu:**
  ```bash
  sudo apt update
  sudo apt install tesseract-ocr
  ```
- **En Windows (Recomendado):**
  Descargar el instalador oficial y asegurar que la ruta al ejecutable (`tesseract.exe`) se añada a las variables de entorno del sistema (o especificar la ruta en el código Python).

#### 1.2.2. Configuración del Entorno Python

Se recomienda el uso de un entorno virtual (`venv` o `conda`) para aislar las dependencias del proyecto.

1.  **Crear y activar el entorno virtual:**

    ```bash
    python3 -m venv venv-lpr
    source venv-lpr/bin/activate  # En Linux/macOS
    # venv-lpr\Scripts\activate  # En Windows
    ```

2.  **Instalar librerías Python:**

    ```bash
    pip install ultralytics opencv-python pytesseract numpy pandas
    ```

### 1.3. Configuración del Dataset y Entrenamiento

El modelo YOLO requiere de un archivo de configuración (`data.yaml`) y el modelo entrenado (`best.pt`).

1.  **Preparación del Dataset (Roboflow):**

    - Descargar el dataset pre-procesado desde **Roboflow** en formato **YOLOv8 PyTorch**.
    - Colocar las carpetas de imágenes (`train`, `val`) y etiquetas (`labels`) en la estructura de directorios del proyecto.

2.  **Archivo `data.yaml`:**

    - Crear un archivo llamado `data.yaml` en la raíz del proyecto. Este archivo es la base del entrenamiento:

    <!-- end list -->

    ```yaml
    # Ruta donde se encuentran las imágenes de entrenamiento y validación
    path: /ruta/absoluta/a/tu/dataset

    train: images/train
    val: images/val

    # Clases (solo una: "plate")
    names:
      0: plate
    ```

3.  **Ejecución del Entrenamiento:**

    - Ejecutar el script de entrenamiento (basado en el código provisto) para generar el modelo `best.pt`.
    - El modelo entrenado se guardará en la ruta: `runs/detect/trainX/weights/best.pt`.

    <!-- end list -->

    ```bash
    python train_model.py # o el nombre del archivo de entrenamiento
    ```

4.  **Configuración de Inferencia:**

    - El script de inferencia principal (`main.py`) debe apuntar al modelo entrenado:
      ```python
      model = YOLO("runs/detect/train2/weights/best.pt") # Asegúrese de que la ruta sea correcta
      ```

---

## 2\. 🖥️ Especificaciones Técnicas de la Arquitectura

### 2.1. Arquitectura del Sistema

El subsistema LPR opera bajo un flujo de trabajo de **visión por computadora** en dos etapas (Pipeline):

1.  **Detección (YOLOv8):** Localiza y clasifica la placa en la imagen de entrada.
2.  **Reconocimiento (OCR/Tesseract):** Extrae la cadena de caracteres de la región de interés detectada.

### 2.2. Componentes Clave y Librerías

| Componente            | Función                                                                                           | Librería/Tecnología    | Notas                                                        |
| :-------------------- | :------------------------------------------------------------------------------------------------ | :--------------------- | :----------------------------------------------------------- |
| **Detección**         | Localización precisa de la placa.                                                                 | **Ultralytics YOLOv8** | Modelo entrenado para la clase única: `plate`.               |
| **Inferencia**        | Preprocesamiento, recorte y ejecución del OCR.                                                    | **OpenCV (`cv2`)**     | Manejo de imágenes (filtros, umbralización, morfología).     |
| **OCR**               | Reconocimiento óptico de caracteres.                                                              | **PyTesseract**        | Interfaz Python al motor Tesseract OCR.                      |
| **Reglas de Negocio** | Limpieza, corrección de errores (`smart_corrections`) y validación de formato (`is_valid_plate`). | **Python (`re`)**      | Implementa patrones RegEx para formatos de placas mexicanas. |

## 2.3. Dataset y Entrenamiento 📊

| Especificación                | Detalle                                                                             |
| :---------------------------- | :---------------------------------------------------------------------------------- |
| **Plataforma de Creación**    | **Roboflow** (para gestión de dataset y control de versiones).                      |
| **Fuente de Datos**           | Imágenes propias y datasets de uso libre.                                           |
| **Metodología de Etiquetado** | **Bounding Boxes** manuales para la clase única: `plate`.                           |
| **Formato de Exportación**    | **YOLOv5 PyTorch** (Estándar de compatibilidad con YOLOv8).                         |
| **Modelo Base**               | **YOLOv8n (nano)**.                                                                 |
| **Justificación del Modelo**  | Elegido por su buen equilibrio entre **velocidad** (baja latencia) y **precisión**. |
| **Función de Pérdida**        | Pérdida de **Clasificación**, **Regresión** y **DFL** (Distribution Focal Loss).    |
| **Hyperparámetros Clave**     | `epochs=50`, `imgsz=640`, `batch=16`.                                               |

### 2.4. Esquema de Salida (API)

El sistema de inferencia genera una salida estructurada en formato **JSON** para una fácil integración con otros módulos:

| Parámetro | Tipo   | Descripción                                                            | Ejemplo                          |
| :-------- | :----- | :--------------------------------------------------------------------- | :------------------------------- |
| `status`  | `bool` | Indica si el proceso de LPR fue exitoso (detección y lectura legible). | `True` o `False`                 |
| `plate`   | `str`  | La matrícula reconocida, solo si `status` es `True`.                   | `"VML-191-D"`                    |
| `message` | `str`  | Mensaje de error o estado, solo si `status` es `False`.                | `"No se detectó ninguna placa."` |

---

## 3\. 🛡️ Consejos para la Solución de Problemas (Troubleshooting)

### Problema 1: `pytesseract.TesseractNotFoundError`

**Error:** El sistema no puede encontrar el ejecutable de Tesseract.

**Solución:**

1.  **Verificar Instalación:** Asegúrese de que el motor Tesseract OCR esté instalado a nivel del sistema (Ver sección 1.2.1).
2.  **Verificar Ruta (Windows/macOS):** Si Tesseract está instalado pero no se encuentra, la ruta no está en la variable `PATH`. Solucione esto agregando el directorio de instalación de Tesseract a `PATH` o especifique la ruta en el código Python:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract' # Ejemplo de ruta Linux
    # o r'C:\Program Files\Tesseract-OCR\tesseract.exe' para Windows
    ```

### Problema 2: El OCR Detecta una Placa, Pero el Texto es Incorrecto o Vacío

**Síntoma:** El modelo YOLO detecta la placa, pero la salida de `ocr_plate` es basura o un string vacío.

**Solución:**

1.  **Ajuste del Preprocesamiento:** Modifique los parámetros de `cv2.adaptiveThreshold` (`17, 9`). Valores más pequeños o grandes pueden mejorar la segmentación en diferentes condiciones de iluminación/resolución.
2.  **Revisar `tessedit_char_whitelist`:** Asegúrese de que la lista blanca (`-c tessedit_char_whitelist=...`) contenga todos los caracteres esperados.
3.  **Inspeccionar la Imagen Binaria:** Temporalmente, muestre la imagen binarizada (`th` en `ocr_plate`) usando `cv2.imshow('Thresholded', th)` para verificar si los caracteres son legibles para un ojo humano. Si no lo son, el preprocesamiento necesita más ajustes.
4.  **Reentrenamiento:** Si el modelo base `yolov8n.pt` no es lo suficientemente preciso, considere reentrenar con **más imágenes** o usar un modelo más grande (ej. `yolov8s.pt`) si hay suficiente capacidad de cómputo.

### Problema 3: `KeyError: 'xyxy'` o `IndexError` al Acceder a Resultados YOLO

**Error:** Ocurre al intentar acceder a `results.boxes` en la función `main()`.

**Solución:**
Esto generalmente significa que no se detectó **ninguna** caja. El código ya maneja esto, pero si ocurre después de la verificación inicial, significa que la heurística de `plate_score` eliminó todas las detecciones.

1.  **Revisar la Heurística:** La relación de aspecto (`1.8 < aspect_ratio < 2.5`) puede ser demasiado estricta. Intente relajarla (ej. `1.5 < aspect_ratio < 3.0`) o eliminar la heurística temporalmente para ver si el error desaparece.
2.  **Ajustar Confianza:** El modelo puede estar detectando con una confianza muy baja. Al llamar a `model()`, se puede establecer un umbral de confianza mínimo: `model(img, conf=0.5, verbose=False)`.
