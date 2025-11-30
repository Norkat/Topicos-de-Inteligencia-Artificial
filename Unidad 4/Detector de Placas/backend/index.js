/**
 * Principal punto de entrada de la aplicacion
 * Este archivo inizializa el servidor y lo comienza en el puerto especificado.
 * @module index
 */
const app = require("./src/app");

/**
 * El numero de puerto por el que el server estara "escuchando"
 * Por defecto, si es que no es especificado un puerto, el numero sera 3001
 * @constant {number}
 */
const PORT = process.env.PORT || 3001;

/**
 * Comienza el servirdor y queda pendiende en escuchar solicitudes al puerto especificado.
 * @listens {number} PORT - El numero del puerto.
 */
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running in http://localhost:${PORT}`);
});