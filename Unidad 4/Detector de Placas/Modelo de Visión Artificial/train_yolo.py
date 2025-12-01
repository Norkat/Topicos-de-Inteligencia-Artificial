from ultralytics import YOLO

##
# FUNCIÓN PRINCIPAL DE ENTRENAMIENTO YOLOv8
##

def main():
    """
    Función principal que inicia y gestiona el proceso de entrenamiento 
    de un modelo de detección de objetos YOLOv8.

    El entrenamiento utiliza el modelo pre-entrenado 'yolov8n.pt' (versión nano) 
    como punto de partida y configura hiperparámetros clave.
    """

    # 1. Inicialización del modelo: Carga el modelo base YOLOv8 nano (el más pequeño
    #    y rápido) con pesos pre-entrenados para transfer learning.
    model = YOLO("yolov8n.pt") 

    # 2. Entrenamiento del modelo (Fine-tuning o Entrenamiento desde cero):
    #    Define la configuración clave del proceso de entrenamiento.
    results = model.train(
        # Especifica la ruta al archivo de configuración del conjunto de datos
        # (incluye rutas a imágenes y archivos de clases/etiquetas).
        data="data.yaml",
        
        # Número total de épocas o ciclos de entrenamiento a realizar.
        # Una época representa una pasada completa sobre todo el conjunto de datos.
        epochs=50,
        
        # Tamaño de la imagen de entrada (altura y anchura) a la cual se escalarán
        # las imágenes antes de pasarlas a la red. Un valor común es 640.
        imgsz=640,
        
        # Tamaño del lote (batch size): Número de imágenes procesadas
        # simultáneamente por la GPU en cada paso de entrenamiento.
        batch=16
    )

    # 3. Mensaje de finalización: Se ejecuta una vez que el bucle de entrenamiento
    #    ha terminado (ya sea por alcanzar las 50 épocas o por interrupción).
    print("Entrenamiento terminado!")


if __name__ == "__main__":
    main()