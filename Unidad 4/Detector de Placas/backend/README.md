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
- /api/car/cars/<plate>: Para regresar el auto que este registrado con la <plata> dada, o mencionar su inexistencia en caso de que no haya ningnuno.
- 

## Dependencias
Instalar pandas para la lectura de datos en csv y el uso de dataframes.
Instalar numpy para el uso de sus vectores y funciones avanzadas.
Instalar matplotlib para el uso de graficas visuales.
```bash
pip install numpy pandas matplotlib
