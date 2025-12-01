/**
 * Pantalla de Inicio
 *
 * - Muestra las 3 acciones principales de la app.
 * - Usa CardButton para mantener un diseño limpio y consistente.
 * - Cada botón redirige a una ruta usando expo-router.
 */

import { View, Text } from "react-native";
import { Link } from "expo-router";
import CardButton from "../components/ui/CardButton";

export default function Home() {
  return (
    <View
      style={{
        flex: 1,
        backgroundColor: "#f3f4f6", // bg-gray-100
        padding: 24, // p-6
        justifyContent: "center",
      }}
    >
      {/* Título principal */}
      <Text
        style={{
          fontSize: 32,        // text-4xl
          fontWeight: "800",   // font-extrabold
          color: "#111827",    // text-gray-900
          marginBottom: 56,    // mb-14
          textAlign: "center", // text-center
        }}
      >
        Detector de Placas
      </Text>

      {/* Contenedor de las opciones */}
      <View
        style={{
          gap: 16, // space-y-4
        }}
      >
        {/* Registrar Propietario */}
        <Link href="/(owners)/OwnerForm" asChild>
          <CardButton icon="user-plus" title="Registrar Propietario" />
        </Link>

        {/* Registrar Auto */}
        <Link href="/(cars)/CarForm" asChild>
          <CardButton icon="car" title="Registrar Auto" />
        </Link>

        {/* Escanear Placa */}
        <Link href="/(plates)/PlateScanner" asChild>
          <CardButton icon="camera" title="Escanear Placa" />
        </Link>
      </View>
    </View>
  );
}
