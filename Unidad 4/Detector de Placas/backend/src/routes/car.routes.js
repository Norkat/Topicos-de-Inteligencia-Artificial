/**
 * Express router para rutas relacionadas con los autos
 * @module routes/car
 */

const express = require("express");
const router = express.Router();
const carController = require("../controllers/car.controller.js");

/**
 * POST /api/car/register
 * Ruta para crear un nuevo auto
 * @name Register
 * @function
 * @memberof module:routes/car
 */
router.post("/register", carController.register);

/**
 * GET /api/car/cars/:licencePlate
 * Ruta para obtener todos los propietarios.
 * 
 * @name GetCar
 * @function
 * @memberof module:routes/car
 */
router.get("/cars/:licencePlate", carController.getCar);

module.exports = router;