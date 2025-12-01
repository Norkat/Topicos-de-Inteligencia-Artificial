/**
 * CarForm - Formulario para registrar vehículos
 *
 * - Permite registrar autos y vincularlos con un propietario existente.
 * - Obtiene informacion de la DB para leer propietarios existentes y guardar autos.
 * - Todos los campos usan Input, excepto el Picker (lista de propietarios).
 * - ScrollView evita problemas de teclado.
 */

import { View, Text, ScrollView, Alert } from "react-native";
import Input from "../../components/forms/Input";
import Button from "../../components/ui/Button";
import { Picker } from "@react-native-picker/picker";
import { useState, useEffect } from "react";

const API_URL = "https://plate-detector-backend.onrender.com";

export default function CarForm() {
  // Lista de propietarios
  const [owners, setOwners] = useState([]);

  // Estado del formulario
  const [form, setForm] = useState({
    placa: "",
    modelo: "",
    marca: "",
    año: "",
    color: "",
    ownerId: "",
  });

  const update = (k, v) => setForm({ ...form, [k]: v });

  // Obtener propietarios del backend
  const fetchOwners = async () => {
    try {
      const res = await fetch(`${API_URL}/api/owner/owners`);
      const data = await res.json();
      setOwners(data);
    } catch (error) {
      console.log("Error fetching owners:", error);
      Alert.alert("Error", "No se pudieron cargar los propietarios");
    }
  };

  useEffect(() => {
    fetchOwners();
  }, []);

  // Validar formulario antes de enviar
  const validateForm = () => {
    const { placa, modelo, marca, año, color, ownerId } = form;

    if (!placa || !modelo || !marca || !año || !color || !ownerId) {
      Alert.alert("Campos incompletos", "Todos los campos son obligatorios.");
      return false;
    }

    if (!/^\d+$/.test(año)) {
      Alert.alert("Año inválido", "El campo 'Año' debe contener solo números.");
      return false;
    }

    return true;
  };

  // Guardar auto en backend
  const handleSave = async () => {
    if (!validateForm()) return;

    try {
      const payload = {
        licencePlate: form.placa,
        model: form.modelo,
        brand: form.marca,
        year: form.año,
        color: form.color,
        ownerId: form.ownerId,
      };

      const res = await fetch(`${API_URL}/api/car/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        Alert.alert("Error", data.message || "No se pudo registrar el auto");
        return;
      }

      Alert.alert("Éxito", "Auto registrado correctamente");

      setForm({
        placa: "",
        modelo: "",
        marca: "",
        año: "",
        color: "",
        ownerId: "",
      });

    } catch (error) {
      console.log("Error al conectar:", error);
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
      <Text
        style={{
          fontSize: 28,
          fontWeight: "700",
          color: "#111827",
          marginBottom: 24,
        }}
      >
        Registrar Auto
      </Text>

      {/* Inputs */}
      <Input label="Placa" value={form.placa} onChangeText={(t) => update("placa", t)} />
      <Input label="Modelo" value={form.modelo} onChangeText={(t) => update("modelo", t)} />
      <Input label="Marca" value={form.marca} onChangeText={(t) => update("marca", t)} />
      <Input label="Año" value={form.año} onChangeText={(t) => update("año", t)} />
      <Input label="Color" value={form.color} onChangeText={(t) => update("color", t)} />

      <Text
        style={{
          fontWeight: "500",
          color: "#374151",
          marginTop: 8,
          marginBottom: 4,
        }}
      >
        Propietario
      </Text>

      <View
        style={{
          backgroundColor: "white",
          borderRadius: 16,
          borderWidth: 1,
          borderColor: "#d1d5db",
          marginBottom: 16,
          overflow: "hidden",
        }}
      >
        <Picker
          selectedValue={form.ownerId}
          onValueChange={(v) => update("ownerId", v)}
        >
          <Picker.Item label="Seleccione..." value="" />

          {owners.map((o) => (
            <Picker.Item
              key={o.owner_id}
              label={`${o.owner_first_name} ${o.owner_last_name}`}
              value={o.owner_id}
            />
          ))}
        </Picker>
      </View>

      <Button title="Guardar" onPress={handleSave} />
    </ScrollView>
  );
}