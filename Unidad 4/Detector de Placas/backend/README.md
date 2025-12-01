# Backend de la aplicación
## Integrantes
- Payan Urquidez Rafael Alberto
- Quiñonez Ramirez Nestor de Jesus

## Resumen
El backend fue realizado en Node junto con Express.
El backend ofrece los siguientes endpoints:
- /api/owner/register: Para registar un propietario del auto
- /api/owner/owners: Para obtener todos los propietarios registrados en la base de datos
- /api/car/register: Para registrar un auto
- /api/car/cars/licensePlate: Para regresar el auto que este registrado con la placa dada, o mencionar su inexistencia en caso de que no haya ningnuno auto con esa placa.
- /api/ia/detectPlate: Para pasar una imagen que pueda procesar el modelo de vision artificial y regrese la placa contenida en la imagen

## Dependencias
Para el backend es necesario tener instalado en el dispositivo node y express:
https://nodejs.org/en
```bash
npm install express

Una vez todo este instalado, dentro del proyecto instalar todas las dependencias:
```bash
npm install
