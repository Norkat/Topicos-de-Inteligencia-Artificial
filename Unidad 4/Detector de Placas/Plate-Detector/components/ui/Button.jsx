/**
 * Componente Button
 *
 * Botón reutilizable con tres variantes:
 * - primary: botón principal de acciones importantes
 * - secondary: botón oscuro de soporte
 * - outline: botón transparente con borde
 *
 * Props:
 * - title: texto visible dentro del botón
 * - onPress: función a ejecutar al presionar
 * - variant: estilo visual del botón ("primary" por defecto)
 * - className: clases adicionales de Tailwind para personalizar
 */
import { TouchableOpacity, Text } from "react-native";

export default function Button({
  title,
  onPress,
  variant = "primary",
}) {
  // Estilos base
  const baseStyle = {
    padding: 16,         // p-4
    borderRadius: 16,    // rounded-2xl
    alignItems: "center",
    justifyContent: "center",
  };

  // Estilos por variante
  const variantStyles = {
    primary: {
      backgroundColor: "#7c3aed", // bg-purple-600
    },
    secondary: {
      backgroundColor: "#1f2937", // bg-gray-800
    },
    outline: {
      backgroundColor: "transparent",
      borderWidth: 1,
      borderColor: "#9ca3af", // border-gray-400
    },
  };

  // Texto según variante
  const textStyles = {
    primary: { color: "white" },
    secondary: { color: "white" },
    outline: { color: "#374151" }, // text-gray-700
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        ...baseStyle,
        ...variantStyles[variant],
      }}
      activeOpacity={0.8}
    >
      <Text
        style={{
          fontSize: 18,       // text-lg
          fontWeight: "600",  // font-semibold
          ...textStyles[variant],
        }}
      >
        {title}
      </Text>
    </TouchableOpacity>
  );
}
