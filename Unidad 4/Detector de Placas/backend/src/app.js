/**
 * Archivo principal para la aplicacion del server
 * Este archivo declara la aplicacion Express, conecta la base de datos
 * y configura las rutas necesarias
 * @module app
 */
require("dotenv").config(); 
const express = require("express");
const cors = require("cors");
const ownerRoutes = require("./routes/owner.routes");
const carRoutes = require("./routes/car.routes");
const detectPlateRoutes = require("./routes/detect-plate.routes");

const app = express();
app.use(cors());
app.use(express.json()); 

/**
 * Consfigurar la ruta principal para las rutas de propietarios
 * Todas las rutas definidas en owner.routes.js tendra de prefijo '/api/owner/'.
 */
app.use("/api/owner", ownerRoutes);

/**
 * Consfigurar la ruta principal para las rutas de autos
 * Todas las rutas definidas en car.routes.js tendra de prefijo '/api/car/'.
 */
app.use("/api/car", carRoutes);

/**
 * Consfigurar la ruta principal para las rutas que usen el modelo de vision artificial
 * Todas las rutas definidas en detect-plate.routes.js tendra de prefijo '/api/ia/'.
 */
app.use("/api/ia", detectPlateRoutes);

module.exports = app;