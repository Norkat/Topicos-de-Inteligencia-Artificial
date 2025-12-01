/**
 * Controllers para el manejo de solicitudes relacionados a los propietarios de auto
 * @module controllers/owner
 */
const ownerService = require("../services/owner.service");

/**
 * Controller para el registro de propietarios de auto.
 *
 * Esta funcion maneja el registro de propietarios con los siguientes pasos:
 * 1. Extraer los datos del propietario en el request body.
 * 2. Validar que todos los campos hayan sido dados.
 * - Responer con HTTP 400 si algun dato falta
 * 3. Llamar al metodo `ownerService.register` para crear el nuevo propietario
 * 4. Responder con status HTTP 201 y un objeto JSON conteniendo el propietario creado 
 *
 * @async
 * @function register
 * @param {Object} req - El objeto request. Espera `firstName`, `lastName`, `email`, `phone` en `req.body`.
 * @param {Object} res - El objeto response.
 * @throws {400} Respondera con 400 Bad Request si algun dato requerido esta faltando.
 * @throws {500} Respondera con 500 Internal Server Error 
 * @returns {Promise<void>} Envia en res un JSON con el propietario recien creado.
 */
const register = async (req, res) => {
    try {
        const { firstName, lastName, email, phone } = req.body;
        // Validate parameters
        if (!firstName || !lastName || !email || !phone) {
            return res.status(400).json({ error: "Falta informacion" });
        }

        const owner = await ownerService.register(firstName, lastName, email, phone);
        res.status(201).json({ message: "Propietario creado", owner });
    }
    catch (error) {
        console.error("Server Error:", error);
        return res.status(500).json({ 
            error: "Sucedio une error inesperado"
        });
    }
}

/**
 * Controller para obtener todos los propietarios del auto
 * Obtiene todos los registros de la tabla owners con el servicio.
 *
 * @async
 * @function getUsers
 * @param {Object} req - El objeto request.
 * @param {Object} res - El objeto response.
 * @throws {500} Respondera con 500 Internal Server Error 
 * @returns {Promise<void>} Envia en res un JSON con todos los propietarios.
 */
const getOwners = async (req, res) => {
    try {
        const data = await ownerService.getOwners();
        res.json(data);
    }
    catch (error) {
        console.error("Server Error:", error);
        return res.status(500).json({ 
            error: "Sucedio une error inesperado"
        });
    }
}

module.exports = { register, getOwners };