/**
 * Controllers para el manejo de solicitudes relacionados a los autos
 * @module controllers/car
 */
const carService = require("../services/car.service");
const NotFoundError = require("../errors/NotFoundError");

/**
 * Controller para el registro de autos.
 *
 * Esta funcion maneja el registro de autos con los siguientes pasos:
 * 1. Extraer los datos del auto en el request body.
 * 2. Validar que todos los campos hayan sido dados.
 * - Responer con HTTP 400 si algun dato falta
 * 3. Llamar al metodo `carService.register` para crear el nuevo auto
 * 4. Responder con status HTTP 201 y un objeto JSON conteniendo el auto creado 
 *
 * @async
 * @function register
 * @param {Object} req - El objeto request. Espera `licencePlate`, `model`, `brand`, `yaer`, `color`, `ownerId` en `req.body`.
 * @param {Object} res - El objeto response.
 * @throws {400} Respondera con 400 Bad Request si algun dato requerido esta faltando.
 * @throws {500} Respondera con 500 Internal Server Error 
 * @returns {Promise<void>} Envia en res un JSON con el propietario recien creado.
 */
const register = async (req, res) => {
    try {
        const { licencePlate, model, brand, year, color, ownerId } = req.body;
        // Validate parameters
        if (!licencePlate || !model || !brand || !year || !color || !ownerId) {
            return res.status(400).json({ error: "Falta informacion" });
        }

        const car = await carService.register(licencePlate, model, brand, year, color, ownerId);
        res.status(201).json({ message: "Propietario creado", car });
    }
    catch (error) {
        if(error.message === "Error: CAR_NOT_FOUND"){
            return res.status(404).json({
                error: "Car not found"
            })
        }

        console.error("Server Error:", error);
        return res.status(500).json({ 
            error: "Sucedio une error inesperado"
        });
    }
}

/**
 * Controller para obtener un auto con la placa especificada
 * Obtiene los datos de la tabla cars con el servicio.
 *
 * @async
 * @function getCar
 * @param {Object} req - El objeto request. Espera `licencePlate` en req.params
 * @param {Object} res - El objeto response.
 * @throws {500} Respondera con 500 Internal Server Error 
 * @returns {Promise<void>} Envia en res un JSON con todos los propietarios.
 */
const getCar = async (req, res) => {
    try {
        const { licencePlate } = req.params;

        const data = await carService.getCar(licencePlate);
        res.json(data);
    }
    catch (error) {
        if (error instanceof NotFoundError) {
            return res.status(404).json({ error: error.message });
        }

        console.error("Server Error:", error);
        return res.status(500).json({ 
            error: "Sucedio une error inesperado"
        });
    }
}

module.exports = { register, getCar };