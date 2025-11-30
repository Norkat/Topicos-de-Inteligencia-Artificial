/**
 * Express router para rutas relacionadas con los propietarios
 * @module routes/owner
 */

const express = require("express");
const router = express.Router();
const ownerController = require("../controllers/owner.controller.js");

/**
 * POST /api/owner/register
 * Ruta para crear un nuevo propietario
 * @name Register
 * @function
 * @memberof module:routes/owner
 */
router.post("/register", ownerController.register);

/**
 * GET /api/owner/owners
 * Ruta para obtener todos los propietarios.
 * 
 * @name GetOwners
 * @function
 * @memberof module:routes/owner
 */
router.get("/owners", ownerController.getOwners);

module.exports = router;