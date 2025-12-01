# **Sistema de Detección y Reconocimiento Automático de Matrículas Vehiculares**

*(React Native + Node.js + Supabase + YOLO + OCR)*

Este proyecto implementa un sistema completo para **detectar matrículas vehiculares**, **reconocer su texto mediante OCR**, y **vincularlas con información de vehículos y propietarios** almacenada en una base de datos en la nube. Combina visión artificial, servicios backend y una aplicación móvil para ofrecer una solución escalable y funcional.

---

Enlace al video creado para mostrar la aplicación funcionando: https://youtube.com/shorts/2hz5o0SdI0s

---

## **Tecnologías utilizadas**

### **Frontend**

* React Native
* Expo Go
* Fetch API

### **Backend**

* Node.js
* Express
* Render (deploy)

### **Base de Datos**

* Supabase (PostgreSQL)

### **Visión Artificial**

* YOLOv8 (Ultralytics)
* Roboflow (dataset)
* Python
* OpenCV
* Tesseract OCR

### **Otros**

* Ngrok (túnel HTTPS para el modelo)

---

## 📌 **Características principales**

### 🔹 **1. Detección de matrículas con YOLO**

* Entrenamiento personalizado usando Ultralytics YOLO.
* Dataset creado con Roboflow: imágenes reales y datasets públicos.
* Exportación del modelo para uso en producción.
* Recorte automático de la región de matrícula detectada.

### 🔹 **2. Reconocimiento de texto (OCR)**

* Implementación con **Tesseract**.
* Preprocesamiento avanzado:

  * Escala de grises
  * Filtro bilateral
  * Umbralización adaptativa
  * Corrección automática de errores (O→0, I→1, S→5)
* Validación mediante expresiones regulares de patrones de placas mexicanas.
* Reintento automático si la primera lectura falla.

### 🔹 **3. Base de datos en la nube (Supabase + PostgreSQL)**

* API REST generada automáticamente.
* Acceso desde backend y aplicación móvil.

### 🔹 **4. Backend Principal (Node.js + Express + Render)**

Expone endpoints para:

* Registrar propietarios.
* Registrar vehículos.
* Consultar un vehículo y su propietario a partir de una placa en texto.

> 📌 *Nota:*
> El backend **no procesa imágenes**.
> Solo recibe texto de la matrícula y consulta Supabase.

### 🔹 **5. Backend del modelo (YOLO + OCR) usando Ngrok**

* Servidor local donde corre YOLO + OCR.
* Exposición temporal mediante **Ngrok** para integrarlo con el backend principal.
* Se envían imágenes → devuelve texto de la placa o error.

### 🔹 **6. Aplicación móvil (React Native + Expo Go)**

* Captura imágenes con la cámara.
* Envía fotos al endpoint del modelo (Ngrok).
* Recibe la matrícula detectada.
* Envía la matrícula en texto al backend principal.
* Muestra la información del vehículo y propietario si existe.

---

## 📂 **Arquitectura General**

```
React Native (captura imagen)
        ↓
Ngrok → Servidor del modelo (YOLO + OCR)
        ↓
Matrícula reconocida (texto)
        ↓
Backend Node.js (Render)
        ↓
Supabase (PostgreSQL)
        ↓
Información del vehículo + propietario
```
---

## 🧠 Flujo completo del sistema

1. El usuario captura una imagen desde la app móvil.
2. La imagen se envía al servidor del modelo usando Ngrok.
3. YOLO detecta la matrícula y recorta la región.
4. OCR procesa el recorte y devuelve el texto.
5. La app envía el texto de la matrícula al backend (Render).
6. El backend consulta Supabase.
7. Devuelve información del propietario y el vehículo.

