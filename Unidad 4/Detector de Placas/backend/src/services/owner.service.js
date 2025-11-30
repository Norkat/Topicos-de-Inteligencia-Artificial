/**
 * Modulo de servicios para la logica relacionada a owners
 * @module services/owner
 */
const supabase = require("../db/supabase");

/**
 * Registrar un nuevo propietario de auto con la informacion dada.
 *
 * La funcion crea un nuevo registro en la tabla owners dentro de la DB con los datos proporcionados.
 * Retorna el propietario recien creado.
 *
 * @async
 * @function register
 * @param {string} firstName - Nombre del propietario.
 * @param {string} lastName - Apellido del propietario.
 * @param {string} email - Email del propietario
 * @param {string} phone - Telegfono del propietario
 * @returns {Promise<Object>} Una promesa que envuelve al propietario recien creado.
 */
const register = async (firstName, lastName, email, phone) => {

    const { data, error } = await supabase
    .from("owners")
    .insert([
      {
        owner_first_name: firstName,
        owner_last_name: lastName,
        owner_email: email,
        owner_phone: phone
      }
    ])
    .select();

    if (error) throw new Error(error.message);

    return data[0];
}

/**
 * Retornar toda la informacion de todos los propietarios de auto en la tabla owners.
 *
 * @async
 * @function getOwners
 * @returns {Promise<Object>} Una promesa que envuelve todos los propietarios de autos en existencia.
 */
const getOwners = async() => {
    const { data, error } = await supabase
    .from("owners")
    .select("*");

    if (error) throw new Error(error.message); 

    return data;
}

module.exports = { register, getOwners };