# 2023-1-Grupo-27

## Modelo ER

![Modelo ER](https://i.imgur.com/5ma6QPz.jpg)

## Modelo Relacional

*Usuario*(**ID**:int, nombreDeUsuario:string, contraseña:string, saldo:int)

*RealizaTransaccion*(**ID_Usuario**:int, **ID_Transaccion**:int, fecha:string)

*Transaccion*(**ID**:int, nombre:string, tipo:string, categoria:string, monto:int)