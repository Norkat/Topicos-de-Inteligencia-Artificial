/**
 * PlateScanner - Pantalla para escanear placas vehiculares
 *
 * Funcionalidades:
 * - Solicita permisos de cámara si no están otorgados.
 * - Muestra la vista de cámara usando CameraView.
 * - Permite el reconocimiento de la placa al tomar la foto
 * - Busca la placa en la DB de autos y muestra resultado.
 *
 * Diseño:
 * - La parte inferior contiene un "panel" estilo modal con fondo blanco.
 * - El botón "Procesar" ejecuta el reconocimiento.
 */

import { View, Text, TouchableOpacity, Alert } from "react-native";
import { CameraView, useCameraPermissions } from "expo-camera";
import { useRef } from "react";
import Button from "../../components/ui/Button";

const API_URL = "https://plate-detector-backend.onrender.com";
const LOCAL_API_URL = "https://misguidedly-theistical-darius.ngrok-free.dev";

export default function PlateScanner() {
  const [permission, requestPermission] = useCameraPermissions();
  const cameraRef = useRef(null);

  // Cuando no hay permisos aún
  if (!permission?.granted)
    return (
      <View
        style={{
          flex: 1,
          justifyContent: "center",
          alignItems: "center",
          padding: 24,
        }}
      >
        <Text style={{ fontSize: 18, color: "#1f2937" }}>
          Permiso de cámara requerido
        </Text>

        <TouchableOpacity
          onPress={requestPermission}
          style={{
            padding: 16,
            backgroundColor: "#7c3aed",
            marginTop: 16,
            borderRadius: 16,
          }}
        >
          <Text style={{ color: "white", fontWeight: "600" }}>
            Conceder permiso
          </Text>
        </TouchableOpacity>
      </View>
    );

  // Buscar auto en backend
  const fetchCarInfo = async (plate) => {
    try {
      const res = await fetch(`${API_URL}/api/car/cars/${plate}`); 

      if (res.status === 404) {
        Alert.alert("No encontrado", `No existe ningún auto con la placa: ${plate}`);
        return;
      }

      if (!res.ok) throw new Error("Error en la petición");

      const data = await res.json();

      Alert.alert(
        "Auto encontrado",
        `Placa: ${data.licence_plate}\nModelo: ${data.car_model}\nMarca: ${data.car_brand}\nAño: ${data.car_year}\nColor: ${data.car_color}\n\nPropietario:\n${data.owners.owner_first_name} ${data.owners.owner_last_name}\nTel: ${data.owners.owner_phone}\nEmail: ${data.owners.owner_email}`
      );
    } catch (err) {
      Alert.alert("Error", err.message);
    }
  };

  // Lógica principal de procesamiento
  const processPlate = async () => {
    Alert.alert("Procesando...", "Tomando foto y detectando placa...");

    // Tomar la foto
    let photo = null;
    if (cameraRef.current) {
      try {
        photo = await cameraRef.current.takePictureAsync({
          quality: 0.8, // Calidad de imagen
          base64: false, // Evitar base64, usar URI de archivo
        });
      } catch (e) {
        Alert.alert("Error de cámara", "No se pudo tomar la foto. Intenta de nuevo.");
        console.error("Camera error:", e);
        return;
      }
    }

    // Verificar la foto
    if (!photo || !photo.uri) {
      Alert.alert("Error", "No se pudo obtener la URI de la imagen.");
      return;
    }
    
    // Preparar el envío con la URI
    try {
      const formData = new FormData();
      const fileName = photo?.uri ? photo.uri.split('/').pop() : 'plate.jpg';
      const fileType = 'image/jpeg';
      
      let fileToSend;

      if (photo && photo.uri) {
        fileToSend = { 
            uri: photo.uri, 
            type: fileType,
            name: fileName,
        };
      } else {
         // Fallback si photo es null en móvil (ya capturado arriba, pero por seguridad)
         Alert.alert("Error", "No se pudo obtener la imagen para enviar.");
         return;
      }

      // Adjuntar el objeto
      formData.append("plateImage", fileToSend); 

      // Enviar al endpoint de detección
      const res = await fetch(`${LOCAL_API_URL}/api/ia/detectPlate`, { 
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json(); // Leer respuesta de error del backend
        Alert.alert("Error", errorData.error || `Error en la detección: ${res.status}`);
        return;
      }

      const data = await res.json();

      if (!data.plate) {
        Alert.alert("Error", "No se pudo detectar ninguna placa en la imagen.");
        return;
      }

      // Buscar en la DB
      fetchCarInfo(data.plate);

    } catch (err) {
      Alert.alert("Error de conexión", err.message);
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: "black" }}>
      {/* Asignar la referencia a la CameraView */}
      <CameraView style={{ flex: 1 }} ref={cameraRef} />

      {/* Panel inferior */}
      <View
        style={{
          position: "absolute",
          bottom: 0,
          width: "100%",
          padding: 20,
        }}
      >
        <View
          style={{
            backgroundColor: "white",
            padding: 20,
            borderRadius: 28,
            shadowColor: "#000",
            shadowOpacity: 0.25,
            shadowRadius: 6,
            shadowOffset: { width: 0, height: 3 },
            elevation: 6,
          }}
        >
          <View style={{ marginTop: 12 }}>
            <Button title="Procesar" onPress={processPlate} />
          </View>
        </View>
      </View>
    </View>
  );
}
