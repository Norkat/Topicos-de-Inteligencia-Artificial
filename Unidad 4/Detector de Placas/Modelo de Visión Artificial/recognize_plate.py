import cv2
from ultralytics import YOLO
import pytesseract
import json
import re

##
# MÓDULO OCR AVANZADO PARA PLACAS
##

def ocr_plate(img):
    """
    Aplica preprocesamiento avanzado optimizado para placas mexicanas
    y realiza OCR con Tesseract para extraer la matrícula.

    El preprocesamiento incluye: escala de grises, filtro bilateral, 
    umbralización adaptativa (Gaussian), y limpieza morfológica.

    Args:
        img (numpy.ndarray): Imagen de la placa de vehículo recortada.

    Returns:
        str: La cadena de texto (matrícula) extraída de la placa.
    """

    # 1. Escala de grises: Simplifica la imagen, manteniendo información de brillo.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Bilateral Filter: Reduce ruido de manera efectiva mientras preserva los bordes
    #    clave de los caracteres (un paso crucial para la calidad del OCR).
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # 3. Adaptive Threshold (GAUSSIAN_C): Crea una imagen binaria (blanco y negro).
    #    Esencial para Tesseract, se adapta a las variaciones de iluminación
    #    en diferentes áreas de la placa.
    th = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        17, 9  # Bloque de 17 y C=9 (valor ajustado para placas)
    )

    # 4. Apertura morfológica (MORPH_OPEN): Elimina pequeños puntos de ruido y
    #    artefactos que pueden confundir a Tesseract (p. ej., suciedad o reflejos).
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)

    # 5. Configuración de Tesseract:
    #    - --oem 3: Usar el motor de Tesseract predeterminado (LSTM).
    #    - --psm 8: Asume que la imagen contiene una sola palabra o una línea de texto.
    #    - -c ...: Define la lista blanca de caracteres (letras mayúsculas, dígitos y guión).
    config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'

    # 6. Aplicar OCR
    text = pytesseract.image_to_string(th, config=config)

    # 7. Normalización y limpieza inicial: Convierte a mayúsculas, elimina espacios,
    #    saltos de línea y caracteres no permitidos.
    text = text.upper().replace(" ", "").replace("\n", "")
    text = re.sub(r'[^A-Z0-9-]', '', text).strip('-')

    # 8. Correcciones inteligentes de ambigüedades comunes de OCR (p. ej., O/0, I/1).
    text = smart_corrections(text)

    # 9. Validación y Reintento: Si el resultado no coincide con un patrón típico
    #    de placa, se intenta un modo de segmentación alternativo (PSM 7: línea única).
    if not is_valid_plate(text):
        config_alt = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'
        text_alt = pytesseract.image_to_string(th, config=config_alt)
        text_alt = text_alt.upper().replace(" ", "").replace("\n", "")
        text_alt = re.sub(r'[^A-Z0-9-]', '', text_alt).strip('-')
        text_alt = smart_corrections(text_alt)
        
        # Devuelve el resultado alternativo solo si es válido.
        if is_valid_plate(text_alt):
            return text_alt

    return text


def smart_corrections(text):
    """
    Corrige errores comunes de OCR (confusión de caracteres) 
    sin modificar matrículas que ya cumplen con el formato estándar.

    Args:
        text (str): El texto extraído por Tesseract.

    Returns:
        str: El texto corregido.
    """
    # Evita correcciones si el texto ya parece un patrón válido
    if is_valid_plate(text):
        return text

    # Reemplazos condicionales:
    # 'O' (letra) por '0' (número)
    text = text.replace("O", "0") 
    # 'I' (letra) por '1' (número)
    text = text.replace("I", "1") 
    # 'S' (letra) por '5' (número)
    text = text.replace("S", "5") 
    return text


def is_valid_plate(text):
    """
    Valida si el texto extraído se ajusta a patrones comunes de placas mexicanas
    utilizando expresiones regulares.

    Args:
        text (str): La cadena de texto a validar.

    Returns:
        bool: True si el texto coincide con algún patrón de placa, False en caso contrario.
    """
    patterns = [
        r'^[A-Z]{3}-\d{3}-[A-Z]$',      # Ej: VML-191-D (Placas Federales/nuevas)
        r'^[A-Z]{2}-\d{2}-\d{3}$',      # Ej: UL-10-609 (Patrones anteriores)
        r'^[A-Z]{3}-\d{3,4}$',          # Ej: ABC-1234 (Patrones comunes con guion)
        r'^[A-Z]{3}\d{3}[A-Z]?$'        # Ej: ABC123D (Patrones sin guion, comunes)
    ]
    # Comprueba si el texto coincide con CUALQUIERA de los patrones.
    return any(re.match(p, text) for p in patterns)


##
# FUNCIÓN PRINCIPAL DE EJECUCIÓN
##

def main():
    """
    Función principal que ejecuta el proceso completo de detección de placas:
    1. Carga el modelo YOLO y la imagen.
    2. Detecta la placa.
    3. Aplica una heurística para seleccionar la mejor detección (relación de aspecto).
    4. Recorta la placa.
    5. Ejecuta el OCR optimizado.
    6. Imprime el resultado en formato JSON.
    """
    img_path = "calis7.jpg"

    # Cargar el modelo de detección de objetos YOLO (entrenado previamente)
    model = YOLO("runs/detect/train2/weights/best.pt")

    # Cargar la imagen
    img = cv2.imread(img_path)

    if img is None:
        result = {"status": False, "message": f"Error: No se pudo cargar la imagen: {img_path}"}
        print(json.dumps(result))
        return

    # Detección: Ejecuta YOLO en la imagen
    results = model(img, verbose=False)[0]

    if len(results.boxes) == 0:
        result = {"status": False, "message": "No se detectó ninguna placa."}
        print(json.dumps(result))
        return

    # Heurística de selección: Calcula una puntuación para cada detección
    # basada en el área y la relación de aspecto típica de una placa (≈ 2:1).
    def plate_score(box):
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        w, h = x2 - x1, y2 - y1
        aspect_ratio = w / h
        # Solo asigna puntuación si la relación de aspecto está entre 1.8 y 2.5
        return w * h if 1.8 < aspect_ratio < 2.5 else 0

    # Selecciona la caja delimitadora (Bounding Box) con la puntuación más alta.
    box = max(results.boxes, key=plate_score)
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    # Recorte de la placa usando las coordenadas seleccionadas
    plate_crop = img[y1:y2, x1:x2]

    if plate_crop.shape[0] == 0 or plate_crop.shape[1] == 0:
        result = {"status": False, "message": "Recorte de placa inválido (dimensiones cero)."}
        print(json.dumps(result))
        return

    # OCR optimizado: Procesa la imagen recortada para obtener el texto
    text = ocr_plate(plate_crop)

    # Generación del resultado final en formato JSON
    if not text:
        result = {"status": False, "message": "Placa detectada pero texto no legible o inválido."}
    else:
        result = {"status": True, "plate": text}

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()