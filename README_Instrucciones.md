
# 🏠 Agencia Inmobiliaria

Sistema web de gestión inmobiliaria desarrollado como proyecto académico utilizando **Python, Django y MariaDB**.

La aplicación permite administrar inmuebles, propietarios, clientes, ofertas comerciales, visitas, características, estancias y usuarios con distintos roles.

## 1. Tecnologías utilizadas

El proyecto se ha desarrollado originalmente con:

| Tecnología | Versión |
|---|---|
| Python | 3.14.4 |
| Django | 6.1.3 |
| MariaDB | 11.8.6 |
| Sistema operativo | Ubuntu |
| Editor | Visual Studio Code |
| Control de versiones | Git y GitHub |
| Extensión recomendada | Git Graph |

Se recomienda utilizar versiones iguales o compatibles con las originales.

Las dependencias de Python se encuentran en `requirements.txt`.

## 2. Funcionalidades implementadas

- Registro e inicio de sesión.
- Administración de usuarios.
- Roles: Administrador, Vendedor y Cliente.
- Gestión de inmuebles.
- Ofertas de venta y alquiler.
- Catálogo público de propiedades.
- Gestión de propietarios.
- Gestión de clientes.
- Gestión de visitas.
- Administración de características y estancias.
- Paneles administrativos según el rol.

### Funcionalidades pendientes

- Gestión de oficinas y zonas.
- Portal del cliente y solicitud de visitas.
- Búsqueda avanzada de inmuebles.
- Reportes y estadísticas.
- Recuperación de contraseña.
- Subida y visualización de imágenes de inmuebles.

---

# 3. Requisitos previos

Antes de comenzar, el computador debe tener:

1. Git.
2. Visual Studio Code.
3. Python compatible con el proyecto.
4. MariaDB compatible con la base de datos.
5. Acceso al repositorio de GitHub.
6. El respaldo SQL de la base de datos académica.

Extensiones recomendadas de Visual Studio Code:

- Python (Microsoft).
- Pylance (Microsoft).
- Git Graph.

> IMPORTANTE: El proyecto utiliza tablas de MariaDB existentes. Varias están definidas con `managed = False` en Django, por lo que no se crean automáticamente mediante migraciones.

---

# 4. Descargar el proyecto desde GitHub

## Opción A: utilizando Visual Studio Code

1. Abrir Visual Studio Code.
2. Presionar `Ctrl + Shift + P`.
3. Buscar `Git: Clone`.
4. Seleccionar la opción.
5. Pegar la URL del repositorio.
6. Elegir la carpeta donde se descargará.
7. Abrir el proyecto clonado.

## Opción B: utilizando la terminal

Ejecutar:

```bash
git clone URL_DEL_REPOSITORIO
```

Reemplazar `URL_DEL_REPOSITORIO` por la dirección real del proyecto en GitHub.

Entrar a la carpeta descargada:

```bash
cd Agencia-inmobiliaria
```

El nombre de la carpeta puede variar según el repositorio.

Todos los comandos posteriores deben ejecutarse desde la carpeta donde se encuentra `manage.py`.

---

# 5. Configurar Python

## 5.1. Comprobar la versión instalada

En Linux:

```bash
python3 --version
```

En Windows:

```powershell
py --version
```

El proyecto fue desarrollado originalmente con Python 3.14.4.

Se recomienda utilizar esa versión o una compatible con las dependencias de `requirements.txt`.

Si Python no está instalado, debe instalarse antes de continuar.

## 5.2. Crear un entorno virtual

Cada computador debe crear su propio entorno virtual.

No es necesario copiar la carpeta `.venv` desde otro equipo.

### Linux / Ubuntu

```bash
python3 -m venv .venv
```

Activar el entorno:

```bash
source .venv/bin/activate
```

### Windows / PowerShell

```powershell
py -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide ejecutar el script de activación, se puede utilizar CMD:

```cmd
.venv\Scripts\activate.bat
```

### Comprobar la activación

La terminal normalmente mostrará:

```text
(.venv)
```

Esto indica que el entorno virtual está activo.

---

# 6. Instalar dependencias de Python

Con el entorno virtual activado, ejecutar:

```bash
python -m pip install --upgrade pip
```

Después instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Este comando instala las bibliotecas necesarias para ejecutar el proyecto.

Comprobar la versión de Django:

```bash
python -m django --version
```

Si aparece un error al instalar alguna dependencia, verificar la versión de Python y los paquetes requeridos por el sistema operativo.

---

# 7. Instalar y configurar MariaDB

## 7.1. Comprobar si MariaDB está instalado

Ejecutar:

```bash
mariadb --version
```

La versión utilizada originalmente fue MariaDB 11.8.6.

Se recomienda trabajar con MariaDB 11.8.x para mantener un entorno similar al original.

No es obligatorio actualizar si la versión instalada es compatible y permite importar y utilizar correctamente la base de datos.

## 7.2. Instalar MariaDB si es necesario

### Ubuntu

Consultar los paquetes disponibles:

```bash
apt policy mariadb-server
```

La versión ofrecida por los repositorios de Ubuntu puede ser diferente de la utilizada originalmente.

Si se necesita MariaDB 11.8, utilizar el repositorio oficial de MariaDB correspondiente a la versión de Ubuntu instalada, siguiendo su documentación.

No instalar ni actualizar MariaDB en computadores institucionales sin autorización.

### Windows

Instalar una versión compatible de MariaDB utilizando el instalador oficial.

Durante la instalación:

1. Configurar la contraseña del administrador.
2. Identificar el puerto del servidor.
3. Comprobar que el servicio de MariaDB esté funcionando.

## 7.3. Iniciar MariaDB

En Ubuntu, cuando se utiliza una instalación mediante el servicio del sistema:

```bash
sudo systemctl start mariadb
```

Comprobar su estado:

```bash
sudo systemctl status mariadb
```

Si MariaDB está instalado mediante XAMPP, iniciar el servidor desde XAMPP en lugar de utilizar `systemctl`.

## 7.4. Conectarse al servidor

Ejemplo:

```bash
mariadb -u root -p
```

Introducir la contraseña configurada.

En algunas instalaciones de Ubuntu se utiliza:

```bash
sudo mariadb
```

Comprobar la versión del servidor:

```sql
SELECT VERSION();
```

---

# 8. Preparar la base de datos

La aplicación utiliza una base de datos relacional en MariaDB.

El esquema original contiene 16 tablas preexistentes relacionadas con:

- Inmuebles.
- Viviendas, pisos, casas, villas y locales.
- Propietarios.
- Oficinas.
- Zonas.
- Ofertas comerciales.
- Características.
- Estancias.
- Clientes.
- Visitas.

Django también utiliza tablas adicionales para usuarios, grupos, permisos, sesiones y migraciones.

## 8.1. Obtener el respaldo SQL

Solicitar al responsable del proyecto el archivo de respaldo de la base de datos académica.

Este respaldo debe contener el esquema necesario y, si se requiere, los registros ficticios utilizados para las pruebas.

El archivo puede tener un nombre como:

```text
respaldo_inmobiliaria.sql
```

No se debe asumir que este archivo existe en GitHub: comprobar que haya sido compartido.

## 8.2. Crear o restaurar la base de datos

Si el respaldo incluye las instrucciones `CREATE DATABASE` y `USE`, puede importarse directamente:

```bash
mariadb -u root -p < respaldo_inmobiliaria.sql
```

Si el respaldo no incluye la creación de la base de datos, primero crearla desde MariaDB:

```sql
CREATE DATABASE nombre_base_datos
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Después importar el respaldo:

```bash
mariadb -u root -p nombre_base_datos < respaldo_inmobiliaria.sql
```

Reemplazar `nombre_base_datos` por el nombre real configurado para el proyecto.

IMPORTANTE: utilizar un respaldo apropiado para el tipo de importación. No importar dos veces las mismas tablas sin revisar previamente su contenido.

## 8.3. Verificar las tablas

Conectarse a MariaDB:

```bash
mariadb -u root -p
```

Seleccionar la base de datos:

```sql
USE nombre_base_datos;
```

Consultar las tablas:

```sql
SHOW TABLES;
```

Comprobar los inmuebles:

```sql
SELECT * FROM inmueble;
```

Comprobar los clientes:

```sql
SELECT * FROM cliente;
```

Si aparecen las tablas esperadas, la importación se ha realizado correctamente.

---

# 9. Configurar la conexión de Django con MariaDB

Abrir el archivo `settings.py` del paquete principal de configuración de Django.

Buscar la variable:

```python
DATABASES
```

Comprobar que sus valores correspondan al servidor MariaDB del computador.

Ejemplo de referencia:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "nombre_base_datos",
        "USER": "usuario_mariadb",
        "PASSWORD": "contrasena_local",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

Este ejemplo NO debe reemplazar automáticamente la configuración existente.

Cada computador puede utilizar un usuario, contraseña o puerto diferente.

Si se modifican valores locales en un archivo versionado, no incluir accidentalmente esas modificaciones en un commit.

Mantener la `SECRET_KEY` requerida por Django y comprobar que la configuración sea válida.

---

# 10. Verificar el proyecto

Con el entorno virtual activado, ejecutar desde la raíz:

```bash
python manage.py check
```

Si la configuración es correcta, Django debería mostrar:

```text
System check identified no issues (0 silenced).
```

Después comprobar las migraciones:

```bash
python manage.py showmigrations
```

Si la base de datos es nueva y se han importado únicamente las tablas académicas, ejecutar las migraciones correspondientes a las aplicaciones administradas por Django:

```bash
python manage.py migrate
```

ATENCIÓN:

- Las tablas con `managed = False` deben existir previamente.
- Si se restauró una base de datos completa que incluye las tablas y el historial de migraciones de Django, comprobar su estado antes de ejecutar nuevas migraciones.
- No utilizar `makemigrations` como sustituto de importar el esquema SQL original.

---

# 11. Ejecutar la aplicación

Desde la carpeta que contiene `manage.py`, con el entorno virtual activado:

```bash
python manage.py runserver --noreload
```

Abrir el navegador en:

```text
http://127.0.0.1:8000/
```

Para detener el servidor:

```text
Ctrl + C
```

Debido a que se utiliza `--noreload`, después de modificar archivos Python es necesario detener y volver a iniciar el servidor para aplicar los cambios.

Los cambios en plantillas y archivos estáticos pueden requerir actualizar el navegador.

---

# 12. Acceder al sistema

La aplicación tiene tres roles:

## Administrador

Puede administrar usuarios, inmuebles, propietarios, clientes, visitas y demás módulos autorizados.

## Vendedor

Puede gestionar los registros comerciales permitidos por sus permisos, pero tiene restricciones en determinadas operaciones administrativas.

## Cliente

Puede iniciar sesión y consultar las funcionalidades públicas o habilitadas para su rol.

Las cuentas existentes estarán disponibles únicamente si se restauraron los registros correspondientes de la base de datos.

Si se trabaja con una base de datos nueva, puede ser necesario crear las cuentas y configurar los grupos y permisos del proyecto.

No utilizar cuentas de prueba con contraseñas compartidas en entornos públicos.

---

# 13. Trabajar con Git y GitHub

El proyecto utiliza Git para registrar cambios y GitHub para compartirlos.

## 13.1. Antes de comenzar a trabajar

Abrir Visual Studio Code y la carpeta del proyecto.

Abrir una terminal y ejecutar:

```bash
git status
```

Descargar los cambios más recientes:

```bash
git pull
```

Es recomendable hacerlo antes de modificar archivos, especialmente si otros compañeros trabajan en el mismo repositorio.

## 13.2. Realizar cambios

Modificar los archivos necesarios desde Visual Studio Code.

Antes de guardar cambios en Git, comprobar que el proyecto siga funcionando:

```bash
python manage.py check
```

Probar también las funcionalidades modificadas en el navegador.

## 13.3. Crear un commit desde Visual Studio Code

1. Abrir la sección Source Control.
2. Revisar los archivos modificados.
3. Seleccionar los archivos que se van a incluir.
4. Agregarlos mediante Stage Changes.
5. Escribir un mensaje descriptivo.
6. Pulsar Commit.

Ejemplos de mensajes:

```text
feat: agregar gestion de oficinas
fix: corregir formulario de clientes
style: mejorar diseño del catalogo
```

## 13.4. Subir los cambios a GitHub

Después del commit, utilizar:

```bash
git push
```

O pulsar Push / Sync Changes en Visual Studio Code.

Git Graph permite visualizar los commits, las ramas y el historial del proyecto.

## 13.5. Descargar cambios realizados por otros compañeros

Antes de continuar trabajando:

```bash
git pull
```

Esto descarga e integra los cambios remotos en la rama actual.

Si existen modificaciones locales que entran en conflicto con los cambios remotos, será necesario resolverlas antes de continuar.

---

# 14. Trabajar desde varios computadores

## En el computador de casa

1. Abrir el proyecto.
2. Ejecutar `git pull`.
3. Activar `.venv`.
4. Iniciar MariaDB.
5. Ejecutar Django.
6. Desarrollar las funcionalidades.
7. Probar los cambios.
8. Crear un commit.
9. Ejecutar `git push`.

## En el computador de la universidad

La primera vez:

1. Clonar el repositorio.
2. Instalar Python y las dependencias.
3. Crear `.venv`.
4. Preparar MariaDB.
5. Restaurar la base de datos.
6. Configurar `settings.py`.
7. Comprobar Django.
8. Iniciar el servidor.

Las siguientes veces:

1. Abrir el repositorio local.
2. Ejecutar `git pull`.
3. Activar `.venv`.
4. Iniciar MariaDB.
5. Ejecutar Django.
6. Continuar desarrollando.
7. Crear commit y hacer push.

IMPORTANTE:

GitHub sincroniza el código fuente, pero NO sincroniza automáticamente los registros de MariaDB.

Si se modifica la estructura de la base de datos, esos cambios deben documentarse y compartirse mediante migraciones o scripts SQL apropiados.

Si se necesitan los mismos datos de prueba en otro computador, debe realizarse una exportación e importación controlada de la base de datos.

---

# 15. Problemas frecuentes

## Error: No module named django

El entorno virtual puede estar desactivado o las dependencias no están instaladas.

Solución:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows se debe utilizar el comando de activación correspondiente.

## Error: Can't connect to MySQL server

Comprobar:

- Que MariaDB esté iniciado.
- Que el puerto sea correcto.
- Que el usuario exista.
- Que la contraseña sea correcta.
- Que `settings.py` apunte al servidor adecuado.

## Error: Table doesn't exist

Comprobar que se haya importado correctamente el esquema de la base de datos.

Las tablas académicas con `managed = False` no se crean automáticamente con `migrate`.

## Error: Access denied for user

Revisar las credenciales y los permisos del usuario de MariaDB.

## Error: Address already in use

El puerto 8000 puede estar ocupado.

Se puede iniciar Django en otro puerto:

```bash
python manage.py runserver 8001 --noreload
```

Después abrir:

```text
http://127.0.0.1:8001/
```

## Error después de descargar cambios

Comprobar si `requirements.txt` fue actualizado.

Si hay nuevas dependencias:

```bash
python -m pip install -r requirements.txt
```

Si hay cambios en la base de datos, revisar las instrucciones de actualización correspondientes.

---

# 16. Recomendaciones de trabajo

- Hacer `git pull` antes de comenzar.
- Realizar commits pequeños y descriptivos.
- No subir la carpeta `.venv`.
- No modificar directamente las tablas sin documentar los cambios.
- No sobrescribir bases de datos que contengan trabajo de otros compañeros.
- Probar los módulos antes de subir cambios.
- Mantener actualizado este README.
- No publicar credenciales utilizadas en servicios reales.

---

# 17. Estado del desarrollo

## Módulos completados

- [x] Autenticación básica.
- [x] Roles y permisos.
- [x] Administración de usuarios.
- [x] Gestión de inmuebles.
- [x] Ofertas comerciales.
- [x] Catálogo público.
- [x] Gestión de propietarios.
- [x] Gestión de clientes.
- [x] Gestión de visitas.
- [x] Características y estancias.

## Módulos pendientes

- [ ] Gestión de oficinas y zonas.
- [ ] Portal del cliente y solicitud de visitas.
- [ ] Búsqueda avanzada de inmuebles.
- [ ] Reportes y estadísticas.
- [ ] Recuperación de contraseña.
- [ ] Subida de imágenes para inmuebles.

---

# 18. Naturaleza del proyecto

Este sistema se desarrolla con fines exclusivamente académicos.

Los registros utilizados para pruebas deben ser ficticios.

La configuración actual corresponde a un entorno de desarrollo y no debe utilizarse directamente como configuración de producción.

---

**Agencia Inmobiliaria — Proyecto académico en desarrollo.**
