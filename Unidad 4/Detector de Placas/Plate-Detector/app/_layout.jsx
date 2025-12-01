/**
 * Layout global para toda la aplicación
 * 
 * - Define un header personalizado reutilizable
 * - Centraliza los títulos mediante TITLE_MAP
 * - Reemplaza los headers nativos de Expo Router
 * - Mantiene el botón de regreso y el título centrado.
 */
import { Stack } from "expo-router";
import { StatusBar, TouchableOpacity, Text, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";

// Mapa de títulos
const TITLE_MAP = {
  index: "Inicio",
  "(owners)/OwnerForm": "Registrar Propietario",
  "(cars)/CarForm": "Registrar Auto",
  "(plates)/PlateScanner": "Escanear Placa",
};

export default function Layout() {
  return (
    <>
      <StatusBar barStyle="dark-content" />

      <Stack
        screenOptions={{
          header: ({ navigation, route }) => {
            const canGoBack = navigation.canGoBack();
            const title = TITLE_MAP[route.name] || route.name;

            return (
              <View
                style={{
                  backgroundColor: "white",
                  paddingHorizontal: 16, // px-4
                  paddingVertical: 12,   // py-3
                  flexDirection: "row",
                  alignItems: "center",
                  // shadow-sm equivalente:
                  shadowColor: "#000",
                  shadowOffset: { width: 0, height: 1 },
                  shadowOpacity: 0.12,
                  shadowRadius: 2,
                  elevation: 2, // Android shadow
                }}
              >
                {/* Botón regresar */}
                {canGoBack ? (
                  <TouchableOpacity
                    onPress={navigation.goBack}
                    style={{
                      marginRight: 12, // mr-3
                      padding: 8,      // p-2
                      borderRadius: 999,
                    }}
                  >
                    <Ionicons name="chevron-back" size={26} color="#4B5563" />
                  </TouchableOpacity>
                ) : (
                  <View style={{ width: 40 }} /> // simetría
                )}

                {/* Título */}
                <View style={{ flex: 1 }}>
                  <Text
                    style={{
                      textAlign: "center",
                      fontSize: 18, // text-lg
                      fontWeight: "600", // font-semibold
                      color: "#1f2937", // text-gray-900
                    }}
                  >
                    {title}
                  </Text>
                </View>

                {/* espacio simétrico */}
                <View style={{ width: 40 }} />
              </View>
            );
          },
        }}
      />
    </>
  );
}
