/**
 * CardButton
 *
 * Botón en forma de tarjeta para la pantalla principal.
 * Incluye ícono + texto y se ve como una opción del menú principal.
 *
 * Props:
 * - icon: nombre del ícono FontAwesome5
 * - title: texto visible de la tarjeta
 * - onPress: función al presionar
 */

import { TouchableOpacity, Text } from "react-native";
import { FontAwesome5 } from "@expo/vector-icons";

export default function CardButton({ icon, title, onPress }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      activeOpacity={0.85} // reemplazo de active:scale-95
      style={{
        backgroundColor: "white", // bg-white
        padding: 20,              // p-5
        borderRadius: 16,         // rounded-2xl
        flexDirection: "row",     // flex-row
        alignItems: "center",     // items-center

        // shadow-sm equivalente
        shadowColor: "#000",
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.15,
        shadowRadius: 2,
        elevation: 2, // sombra Android
      }}
    >
      {/* Ícono principal */}
      <FontAwesome5 name={icon} size={26} color="#6D28D9" />

      {/* Texto */}
      <Text
        style={{
          marginLeft: 16,       // ml-4
          fontSize: 20,         // text-xl
          fontWeight: "600",    // font-semibold
          color: "#1f2937",     // text-gray-800
        }}
      >
        {title}
      </Text>
    </TouchableOpacity>
  );
}
