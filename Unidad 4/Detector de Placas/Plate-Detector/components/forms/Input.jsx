/**
 * Componente Input
 *
 * Campo de texto reutilizable con label opcional.
 *
 * Props:
 * - label: texto que aparece arriba del input
 * - value: valor del input
 * - onChangeText: función que actualiza el valor
 * - placeholder: texto de ayuda dentro del input
 * - secureTextEntry: para contraseñas o datos privados
 */
import { View, Text, TextInput } from "react-native";

export default function Input({
  label,
  value,
  onChangeText,
  placeholder,
  secureTextEntry,
}) {
  return (
    <View
      style={{
        marginBottom: 16, // mb-4
      }}
    >
      {/* Etiqueta del campo */}
      {label && (
        <Text
          style={{
            color: "#374151",   // text-gray-700
            marginBottom: 4,    // mb-1
            fontWeight: "500",  // font-medium
            fontSize: 16,       // text-base
          }}
        >
          {label}
        </Text>
      )}

      {/* Caja de entrada */}
      <TextInput
        style={{
          backgroundColor: "white",
          padding: 16,         // p-4
          borderRadius: 16,    // rounded-2xl
          borderWidth: 1,
          borderColor: "#d1d5db", // border-gray-300
          fontSize: 16,
        }}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        secureTextEntry={secureTextEntry}
      />
    </View>
  );
}
