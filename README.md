# Desarrollo local

### Setup

*Aclaración: Para poder seguir los siguientes pasos, necesitás tener Docker instalado en tu máquina.*

Para iniciar los contenedores del backend y la base de datos, ejecutar:
```
./start_dev_containers
```

Si no te permite ejecutar el script anterior, ejecutar (lo mismo para cualquiera de los scripts del repo):
```
chmod +x start_dev_containers
```

Una vez iniciados los contenedores y estando en la terminal dentro del backend, ejecutar el siguiente script para iniciar la API en modo desarrollo:
```
./start_dev
```

Con esto ya podés codear los cambios que quieras para la API, que se reinicia automáticamente cada vez que detecta un cambio en algún archivo.

### Migrations

Para crear un template de DB migration, ejecutar:
```
alembic revision -m "crear tabla usuarios"
```

Para ejecutar la última migration creada, ejecutar:
```
alembic upgrade head
```