# Finance Manager

## Descripción
Finance Manager es una página web que ayuda a ordenar las finanzas de un usuario, guardando todas las transacciones financieras realizadas por un usuario.

## Features
+ Crear, modificar y borrar ingresos/egresos.
+ Ver tu saldo disponible.
+ Asignar categorias a tus ingresos/egresos.
+ Listar tus ingresos/egresos por categoria.
+ Listar tus ingresos/egresos en un rango de fechas.

## Modelo ER y Modelo Relacional
<details><summary> Detalles </summary>

### Modelo ER
<img src="https://i.imgur.com/5ma6QPz.jpg" alt= "Modelo ER" width="25%" height="25%">

### Modelo Relacional

*Usuario*(**ID**:int, nombreDeUsuario:string, contraseña:string, saldo:int)

*Transaccion*(**ID**:int, nombre:string, tipo:string, categoria:string, monto:int, fecha:string, ID_Usuario:int)

</details>

## Bocetos

<details><summary> Frontend de baja fidelidad </summary>

### Página Principal
<img src="https://i.imgur.com/CuxqDu5.jpg" alt= "Pagina Principal" width="50%" height="50%">

### Formulario de Ingreso
<img src="https://i.imgur.com/CpJ9kRX.jpg" alt= "Formulario de Ingreso" width="50%" height="50%">

</details>

## Vista actual

<details><summary> Version alpha </summary>

### Pagina Principal (Logged Out)
<img src="https://i.imgur.com/bsWWNkF.jpg" alt= "Pagina Principal (Logged Out)" width="50%" height="25%">

### Pagina Principal (Logged In)
<img src="https://i.imgur.com/n3qpvUd.jpg" alt= "Pagina Principal (Logged In)" width="50%" height="25%">

### Formulario de Ingreso
<img src="https://i.imgur.com/2d0XUnK.jpg" alt= "Formulario de Ingreso" width="25%" height="25%">

### Formulario de Egreso
<img src="https://i.imgur.com/I2m6qQ8.jpg" alt= "Formulario de Egreso" width="25%" height="25%">

### Formulario de Modificación
<img src="https://i.imgur.com/2ZcQc9B.jpg" alt= "Formulario de Modificación" width="25%" height="25%">

</details>

<details><summary> Version beta </summary>

### Pagina Principal (Logged Out)
<img src="https://i.imgur.com/KeGoLVh.jpg" alt= "Pagina Principal (Logged Out)" width="50%" height="25%">

### Registro
<img src="https://i.imgur.com/r4D0n6H.jpg" alt= "Registro" width="50%" height="25%">

### Inicio de Sesión
<img src="https://i.imgur.com/nNKVkmm.jpg" alt= "Inicio de Sesión" width="50%" height="25%">

### Pagina Principal (Logged In)
<img src="https://i.imgur.com/T9n2Q8C.jpg" alt= "Pagina Principal (Logged In)" width="50%" height="25%">

### Formulario de Ingreso
<img src="https://i.imgur.com/qA1lVCe.jpg" alt= "Formulario de Ingreso" width="50%" height="25%">

### Formulario de Egreso
<img src="https://i.imgur.com/WImHPic.jpg" alt= "Formulario de Egreso" width="50%" height="25%">

### Formulario de Modificación
<img src="https://i.imgur.com/mLEqfWw.jpg" alt= "Formulario de Modificación" width="50%" height="25%">

</details>