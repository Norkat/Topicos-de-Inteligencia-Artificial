/**
 * Controllers para el manejo de solicitudes relacionados a los autos
 * @module controllers/car
 */
const detectPlateService = require("../services/detect-plate.service");

/**
 * Controller para la deteccion de placas de autos.
 *
 * Esta funcion maneja la deteccion de placas de autos con los siguientes pasos:
 * 1. Extraer la imagen de la placa del request body.
 * 2. Validar que la imagen si haya sido enviada
 * - Responer con HTTP 400 si es que falta
 * 3. Llamar al metodo `detectPlateService.detectPlate` para que regrese la placa en la imagen
 * 4. Retornar el numero de placa
 *
 * @async
 * @function detectPlate
 * @param {Object} req - El objeto request.
 * @param {Object} res - El objeto response.
 * @throws {400} Respondera con 400 Bad Request si la imagen requerida esta faltando.
 * @throws {500} Respondera con 500 Internal Server Error 
 * @returns {Promise<void>} Envia en res la placa detectada en la imagen.
 */
const detectPlate = async (req, res) => {
    try {
        const plateImage = req.file

        // Validacion
        if (!plateImage) {
            return res.status(400).json({
                error: "La imagen de la placa es requerida."
            });
        }

        // Llamada al servicio: aquí va tu modelo real
        const detectedPlate = await detectPlateService.detectPlate(plateImage);

        // Si no es encontrada
        if (!detectedPlate) {
            return res.status(404).json({
                error: "No se pudo detectar ninguna placa en la imagen."
            });
        }

        return res.status(200).json({
            plate: detectedPlate
        });
    } catch (error) {
        console.error("Error en detectPlate:", error);

        return res.status(500).json({
            error: "Error interno al procesar la imagen."
        });
    }
};

module.exports = { detectPlate };