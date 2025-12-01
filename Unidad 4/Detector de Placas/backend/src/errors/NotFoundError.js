/**
 * Clase de error personalizada para representar errores de tipo "No encontrado".
 * 
 * Esta clase extiende la clase `Error` y se utiliza para 
 * lanzar errores cuando un recurso solicitado no se encuentra en la base de datos.
 *
 * @class NotFoundError
 * @extends Error
 */
class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = "NotFoundError";
  }
}

module.exports = NotFoundError;