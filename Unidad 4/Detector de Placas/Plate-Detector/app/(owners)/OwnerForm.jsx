/**
 * OwnerForm - Formulario para registrar propietarios
 *
 * - Permite ingresar datos personales de un propietario.
 * - Utiliza Input y Button de tu UI kit para mantener consistencia visual.
 * - Guarda el propietario en la base de datos
 * - Incluye ScrollView para evitar que el teclado tape los campos.
 */

import { View, Text, ScrollView, Alert } from "react-native";
import Input from "../../components/forms/Input";
import Button from "../../components/ui/Button";
import { useState } from "react";

const API_URL = "https://plate-detector-backend.onrender.com";

export default function OwnerForm() {

  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: ""
});

  const update = (k, v) => setForm({ ...form, [k]: v });

  // Validación de campos
  const validateForm = () => {
    const { firstName, lastName, email, phone } = form;

    // Validar vacíos
    if (!firstName || !lastName || !email || !phone) {
      Alert.alert("Campos incompletos", "Por favor llena todos los campos.");
      return false;
    }

    // Validar teléfono (solo números)
    if (!/^\d+$/.test(phone)) {
      Alert.alert("Teléfono inválido", "El teléfono debe contener solo números.");
      return false;
    }

    // Validar correo
    if (!/\S+@\S+\.\S+/.test(email)) {
      Alert.alert("Correo inválido", "Ingresa un correo electrónico válido.");
      return false;
    }

    return true; // Todo correcto
  };

  const handleSave = async () => {
    // 1️⃣ Validación
    if (!validateForm()) return;

    try {
      // 2️⃣ Enviar datos al backend
      const response = await fetch(`${API_URL}/api/owner/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        Alert.alert("Error", data.message || "No se pudo registrar");
        return;
      }

      Alert.alert("Éxito", "Propietario registrado correctamente");

      // 3️⃣ Limpiar formulario
      setForm({
        firstName: "",
        lastName: "",
        email: "",
        phone: "",
      });

    } catch (error) {
      console.error("Error al conectar:", error);
      Alert.alert("Error", "No fue posible conectar al servidor");
    }
  };

  return (
    <ScrollView
      style={{
        flex: 1,
        backgroundColor: "#f3f4f6",
        padding: 24,
      }}
    >
      {/* Título */}
      <Text
        style={{
          fontSize: 28,
          fontWeight: "700",
          color: "#111827",
          marginBottom: 24,
        }}
      >
        Registrar Propietario
      </Text>

      {/* Inputs */}
      <Input label="Nombre" value={form.firstName} onChangeText={(t) => update("firstName", t)} />
      <Input label="Apellidos" value={form.lastName} onChangeText={(t) => update("lastName", t)} />
      <Input label="Teléfono" value={form.phone} onChangeText={(t) => update("phone", t)} />
      <Input label="Correo" value={form.email} onChangeText={(t) => update("email", t)} />

      {/* Botón Guardar */}
      <View style={{ marginTop: 16 }}>
        <Button title="Guardar" onPress={handleSave} />
      </View>
    </ScrollView>
  );
}
