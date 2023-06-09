# Finance Manager

## Descripción
Finance Manager es una página web que ayuda a ordenar las finanzas de un usuario, guardando todas las transacciones financieras realizadas por un usuario.

## Features
+ Crear, modificar y borrar ingresos/egresos.
+ Ver tu saldo disponible.
+ Asignar categorias a tus ingresos/egresos.
+ (To Be Implemented) Listar tus ingresos/egresos por categoria.
+ Listar tus ingresos/egresos en un rango de fechas.

## Modelo ER

<img src="https://i.imgur.com/5ma6QPz.jpg" alt= "Modelo ER" width="25%" height="25%">

## Modelo Relacional

*Usuario*(**ID**:int, nombreDeUsuario:string, contraseña:string, saldo:int)

*Transaccion*(**ID**:int, nombre:string, tipo:string, categoria:string, monto:int, fecha:string, ID_Usuario:int)

## Bocetos del Frontend de baja fidelidad

### Página Principal
<img src="https://i.imgur.com/CuxqDu5.jpg" alt= "Pagina Principal" width="50%" height="50%">

### Formulario de Ingreso
<img src="https://i.imgur.com/CpJ9kRX.jpg" alt= "Formulario de Ingreso" width="50%" height="50%">

## Vista Actual

### Pagina Principal (Logged Out)
<img src="https://i.imgur.com/bsWWNkF.jpg" alt= "Formulario de Ingreso" width="50%" height="25%">

### Pagina Principal (Logged In)
<img src="https://i.imgur.com/n3qpvUd.jpg" alt= "Formulario de Ingreso" width="50%" height="25%">

### Formulario de Ingreso
<img src="https://i.imgur.com/2d0XUnK.jpg" alt= "Formulario de Ingreso" width="25%" height="25%">

### Formulario de Egreso
<img src="https://i.imgur.com/I2m6qQ8.jpg" alt= "Formulario de Ingreso" width="25%" height="25%">

### Formulario de Modificación
<img src="https://i.imgur.com/2ZcQc9B.jpg" alt= "Formulario de Ingreso" width="25%" height="25%">
