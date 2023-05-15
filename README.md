# Finance Manager

## Descripción
Finance Manager es una página web que ayuda a ordenar las finanzas de un usuario, guardando todas las transacciones financieras realizadas por un usuario.

## Features
+ Crear, modificar y borrar ingresos/egresos.
+ Ver tu saldo disponible.
+ Asignar categorias a tus ingresos/egresos.
+ (To Be Implemented) Listar tus ingresos/egresos por categoria.
+ (To Be Implemented) Listar tus ingresos/egresos en un rango de fechas.

## Modelo ER

![Modelo ER](https://i.imgur.com/5ma6QPz.jpg "Modelo ER")

## Modelo Relacional

*Usuario*(**ID**:int, nombreDeUsuario:string, contraseña:string, saldo:int)

*Transaccion*(**ID**:int, nombre:string, tipo:string, categoria:string, monto:int, fecha:string, ID_Usuario:int)

## Bocetos del Frontend de baja fidelidad

### Página Principal
![Modelo ER](https://i.imgur.com/CuxqDu5.jpg)

### Formulario de Ingreso
![Modelo ER](https://i.imgur.com/CpJ9kRX.jpg)

## Vista Actual

### Pagina Principal (Logged Out)

### Pagina Principal (Logged In)

### Formulario de Ingreso