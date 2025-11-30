/**
 * Modulo de servicios para la logica relacionada a cars
 * @module services/car
 */
const supabase = require("../db/supabase");
const NotFoundError = require("../errors/NotFoundError");

/**
 * Registrar un nuevo auto con la informacion dada.
 *
 * La funcion crea un nuevo registro en la tabla cars dentro de la DB con los datos proporcionados.
 * Retorna el auto recien creado.
 *
 * @async
 * @function register
 * @param {string} licencePlate - Placa del auto
 * @param {string} model - Modelo del auto
 * @param {string} brand - Marca del auto
 * @param {string} year - Año del auto
 * @param {string} color - Color del auto
 * }@param {string} ownerId - Id del propietario del auto
 * @returns {Promise<Object>} Una promesa que envuelve al auto recien creado.
 */
const register = async (licencePlate, model, brand, year, color, ownerId) => {

    const { data, error } = await supabase
    .from("cars")
    .insert([
      {
        licence_plate: licencePlate,
        car_model: model,
        car_brand: brand,
        car_year: year,
        car_color: color,
        car_owner_id: ownerId
      }
    ])
    .select();

    if (error) throw new Error(error.message);

    return data[0];
}

/**
 * Retornar la informacion del auto y su propietario, al que le corresponda la placa dada
 *
 * @async
 * @function getCar
 * @returns {Promise<Object>} Una promesa que envuelve el auto y propietario que corresponde a la placa.
 */
const getCar = async(licencePlate) => {
    const { data, error } = await supabase
    .from("cars")
    .select(`
      *,
      owners:car_owner_id (
        owner_first_name,
        owner_last_name,
        owner_email,
        owner_phone
      )
    `)
    .eq("licence_plate", licencePlate)

    if (error) throw new Error(error.message); 

    if (!data || data.length === 0) throw new NotFoundError("Car not found");

    return data[0];
}

module.exports = { register, getCar };