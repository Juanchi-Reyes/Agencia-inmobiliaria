# Guía de instalación, verificación y trabajo en otro computador

**Proyecto:** Agencia Inmobiliaria  
**Repositorio:** https://github.com/Juanchi-Reyes/Agencia-inmobiliaria  
**Sistema principal:** Ubuntu Linux  
**Stack comprobado en el proyecto:** Python 3.14.4, Django 6.1.3, MariaDB Server 11.8.6, Git y Visual Studio Code.  
**Objetivo:** instalar una copia funcional del proyecto en otro computador, diagnosticar fallos y continuar trabajando sin perder cambios.

> **Importante:** esta guía es para una instalación **nueva**, sin datos que necesites conservar. Si la base `inmobiliaria` ya contiene trabajo, **no ejecutes `DROP DATABASE` ni vuelvas a importar `schema.sql`**. Utiliza la sección «Trabajar en una instalación existente».
>
> **Regla de oro:** los comandos de Bash se ejecutan en la **terminal de Ubuntu**, los comandos SQL dentro de **MariaDB**, y los de Django desde el directorio donde está `manage.py`.

## 1. Archivos que utiliza este proyecto

En la rama `main` revisada, el repositorio incluye:

```text
Agencia-inmobiliaria/
├── manage.py
├── requirements.txt
├── config/
│   └── settings.py
├── apps/
│   ├── cuentas/
│   │   ├── models.py
│   │   └── management/commands/crear_roles.py
│   └── inmuebles/
│       └── models.py
└── db_esquema/
    ├── schema.sql
    ├── post_migracion.sql
    └── datos_prueba.sql
```

| Archivo | Función | Cuándo usarlo |
|---|---|---|
| `db_esquema/schema.sql` | Crea las 16 tablas inmobiliarias administradas mediante SQL. | **Antes** de las migraciones de Django y **solo en una base nueva**. |
| `python manage.py migrate` | Crea las tablas que administra Django, incluida la tabla de usuarios `cuentas_usuario`. | Después de importar `schema.sql`. |
| `db_esquema/post_migracion.sql` | Agrega `cliente.usuario_id` y su relación con `cuentas_usuario`. | **Después** de `migrate`; una sola vez. |
| `python manage.py crear_roles` | Crea los grupos **Administrador**, **Vendedor** y **Cliente**, y configura permisos. | Después de `migrate`; puede volver a ejecutarse. |
| `db_esquema/datos_prueba.sql` | Inserta registros académicos de muestra. | Opcional, **una sola vez en una base nueva**. |
| `requirements.txt` | Fija dependencias de Python. | Cada vez que preparas el entorno o cambian las dependencias. |

**Orden obligatorio en una instalación nueva:** `schema.sql` → `migrate` → `post_migracion.sql` → `crear_roles` → crear superusuario → pruebas. Los datos de prueba son opcionales.

## 2. Requisitos y primeras validaciones

Abre una terminal de Ubuntu y ejecuta:

```bash
lsb_release -a
uname -m
git --version
python3 --version
mariadb --version
```

**Qué revisar:**

- `lsb_release -a` identifica Ubuntu; `uname -m` normalmente muestra `x86_64` en PC de 64 bits.
- `git --version` debe mostrar una versión de Git.
- `python3 --version` muestra la versión predeterminada del sistema; el proyecto se desarrolló con **Python 3.14.4**.
- `mariadb --version` informa la versión del **cliente**, no prueba que el servidor esté instalado.

Si falta Git o el soporte para entornos virtuales:

```bash
sudo apt update
sudo apt install -y git python3-venv
```

**Validación:** ejecuta de nuevo `git --version` y `python3 --version`. Si `python3` no es compatible con Django 6.1.3, instala una versión compatible de Python disponible para tu versión de Ubuntu; **no reemplaces a la fuerza el Python del sistema**. Si tienes Python 3.14, verifica `python3.14 --version` y úsalo en los pasos de creación de `.venv`.

## 3. Clonar el proyecto

Sitúate en una carpeta de tu usuario, donde tengas permiso de escritura. **No es necesario usar `/opt/lampp/htdocs` ni iniciar Apache para `runserver`.**

```bash
mkdir -p ~/proyectos
cd ~/proyectos
git clone https://github.com/Juanchi-Reyes/Agencia-inmobiliaria.git
cd Agencia-inmobiliaria
```

**Validaciones:**

```bash
pwd
ls -la
git remote -v
git branch --show-current
git status
```

**Resultados esperados:**

- `ls` muestra `manage.py`, `requirements.txt`, `config`, `apps` y `db_esquema`.
- `git remote -v` muestra `https://github.com/Juanchi-Reyes/Agencia-inmobiliaria.git` para `fetch`/`push`.
- `git branch --show-current` debería mostrar `main` en una clonación normal.
- `git status` indica `On branch main` y, si no has editado nada, `working tree clean`.

Si la carpeta ya existe y fue clonada antes, **no vuelvas a clonar encima**: entra en ella y comprueba `git status` antes de `git pull`.

## 4. Crear el entorno virtual de Python

Desde la carpeta que contiene `manage.py`, ejecuta **una** de estas opciones:

```bash
# Si el comando predeterminado es la versión compatible:
python3 -m venv .venv

# Alternativa si instalaste específicamente Python 3.14:
# python3.14 -m venv .venv
```

Activa el entorno:

```bash
source .venv/bin/activate
```

**Validaciones:**

```bash
which python
python --version
python -m pip --version
```

**Resultado esperado:** la terminal normalmente comienza con `(.venv)`; `which python` apunta a una ruta terminada en `/Agencia-inmobiliaria/.venv/bin/python`.

> Si aparece `No module named venv` o falla `ensurepip`, instala el paquete de entornos virtuales que corresponda a la versión de Python que utilizas y crea nuevamente `.venv`.

## 5. Instalar las dependencias de Python

Antes de instalar `mysqlclient`, incorpora las librerías que necesita para compilarse en Ubuntu:

```bash
sudo apt update
sudo apt install -y build-essential pkg-config python3-dev libmariadb-dev libmariadb-dev-compat
```

Si usas un Python 3.14 instalado por separado, comprueba que sus archivos de desarrollo estén disponibles; `python3-dev` por sí solo puede corresponder a otra versión.

Con `.venv` activo:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Según el archivo revisado, se instalan **Django 6.1.3**, **mysqlclient 2.3.0**, **python-dotenv 1.2.4**, `asgiref` y `sqlparse`.

**Validaciones:**

```bash
python -m django --version
python -m pip show mysqlclient
python -c "import MySQLdb; print('mysqlclient funciona')"
```

**Resultados esperados:** Django imprime `6.1.3`; `pip show` muestra información de `mysqlclient`; el último comando imprime `mysqlclient funciona`.

**Error conocido:** si aparece `pkg-config: not found`, verifica que instalaste `pkg-config`, `libmariadb-dev` y un compilador; repite `pip install -r requirements.txt`. Si el error menciona `Python.h`, falta el paquete de desarrollo de la versión **exacta** de Python activa.

## 6. Distinguir cliente MariaDB, servidor de Ubuntu y MariaDB de XAMPP

Este fue uno de los errores más importantes al migrar el proyecto: tener el cliente MariaDB 11.8 **no significa** que exista un servidor 11.8 funcionando.

```bash
mariadb --version
command -v mariadbd || true
mariadbd --version
sudo systemctl status mariadb --no-pager
```

**Interpretación:**

- `mariadb --version`: versión del cliente.
- `mariadbd --version`: versión del ejecutable del servidor, si existe.
- `systemctl status`: indica si MariaDB está registrado como servicio y si está activo.
- `Unit mariadb.service could not be found` indica que **no existe ese servicio**, aunque puedas usar el cliente.

Si tienes XAMPP instalado, comprueba por separado:

```bash
sudo /opt/lampp/lampp status
/opt/lampp/bin/mysql --version
```

En el equipo original, el MariaDB incluido en XAMPP era **10.4.32**, mientras que el servidor nuevo necesario para la configuración comprobada era **11.8.6**. Ambos no deben intentar ocupar simultáneamente el puerto `3306`.

Si XAMPP MySQL está encendido, detén **solo ese servicio**:

```bash
sudo /opt/lampp/lampp stopmysql
```

**No uses `sudo /opt/lampp/lampp stop` si quieres conservar Apache funcionando.** Para desarrollar con `python manage.py runserver`, Apache no es necesario.

## 7. Instalar o activar MariaDB Server 11.8

Primero revisa qué versión ofrece Ubuntu:

```bash
sudo apt update
apt-cache policy mariadb-server
```

**Validación:** `Candidate:` indica la versión que instalaría `apt`. **Si no es la versión compatible que deseas, no supongas que `apt install` instalará 11.8**; configura el repositorio adecuado para tu versión de Ubuntu utilizando la documentación oficial de MariaDB, o verifica la compatibilidad del servidor ofrecido.

Si el paquete candidato es el deseado:

```bash
sudo apt install -y mariadb-server
sudo systemctl enable --now mariadb
sudo systemctl status mariadb --no-pager
```

**Resultado esperado:** el estado del servicio contiene `Active: active (running)`.

Comprueba la **versión del servidor**, no solo la del cliente:

```bash
sudo mariadb -e "SELECT VERSION();"
```

En la instalación de referencia debería mostrar una cadena que empieza por `11.8.6-MariaDB`.

Comprueba el puerto:

```bash
sudo ss -ltnp | grep ':3306' || true
```

**Esperado:** una línea `LISTEN` para el puerto `3306` cuando el servidor escucha por TCP. Si no aparece, revisa la configuración de escucha; una conexión por socket todavía podría funcionar.

Si aparece `Unit mariadb.service could not be found`, comprueba qué paquetes están instalados:

```bash
dpkg -l | grep -E 'mariadb-(server|client)'
command -v mariadbd || true
```

Si el servicio no existe, no continúes con la importación hasta completar la instalación del servidor.

## 8. Crear base de datos y usuario de la aplicación

**Esta sección es para una base nueva.** En Ubuntu normalmente se accede como administrador con:

```bash
sudo mariadb
```

La terminal cambia a un prompt similar a `MariaDB [(none)]>`: **a partir de aquí los comandos son SQL**.

```sql
CREATE DATABASE IF NOT EXISTS inmobiliaria
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'inmobiliaria_user'@'127.0.0.1'
IDENTIFIED BY 'CAMBIAR_POR_CONTRASENA_LOCAL';

GRANT ALL PRIVILEGES ON inmobiliaria.*
TO 'inmobiliaria_user'@'127.0.0.1';

SHOW DATABASES LIKE 'inmobiliaria';
SHOW GRANTS FOR 'inmobiliaria_user'@'127.0.0.1';
EXIT;
```

> Sustituye `CAMBIAR_POR_CONTRASENA_LOCAL` por una contraseña elegida en ese equipo. Si ya creaste ese usuario con otra contraseña, `CREATE USER IF NOT EXISTS` **no la cambia**. Puedes emplear `ALTER USER 'inmobiliaria_user'@'127.0.0.1' IDENTIFIED BY 'NUEVA_CONTRASENA';` con privilegios administrativos. Algunos equipos pueden utilizar la cuenta `'inmobiliaria_user'@'localhost'`; inspecciona las cuentas y utiliza una que coincida con tu método de conexión.

**Validación real de permisos y conexión TCP:**

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria
```

Introduce la contraseña cuando aparezca `Enter password:`. Si todo funciona, verás `MariaDB [inmobiliaria]>`. Ejecuta:

```sql
SELECT DATABASE();
SELECT VERSION();
EXIT;
```

**Esperado:** `DATABASE()` devuelve `inmobiliaria`; `VERSION()` indica la versión real del servidor.

**Error `Access denied for user`:** verifica usuario, contraseña y host (`127.0.0.1` frente a `localhost`). **No cambies la contraseña `root` de XAMPP para resolver un problema de credenciales del servidor de Ubuntu**; son instalaciones distintas.

## 9. Configurar `.env` para la conexión Django–MariaDB

`config/settings.py` ya ejecuta `load_dotenv(BASE_DIR / ".env")` y toma de allí `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT`. **No es necesario reemplazar el bloque `DATABASES` de `settings.py`.**

En la raíz del proyecto, verifica que existe `.env` y edítalo en VS Code. Para la conexión local, los valores necesarios son:

```dotenv
DB_NAME=inmobiliaria
DB_USER=inmobiliaria_user
DB_PASSWORD=CAMBIAR_POR_CONTRASENA_LOCAL
DB_HOST=127.0.0.1
DB_PORT=3306
```

Conserva cualquier otra variable que utilice el proyecto. Si la contraseña contiene caracteres especiales, comprueba la sintaxis aceptada por `python-dotenv`.

**Atención de seguridad:** en la versión del repositorio inspeccionada, `.env` **aparece versionado en Git** y `.gitignore` no lo excluye. No hagas un commit de tus credenciales locales. Para corregir el repositorio compartido más adelante, agrega `.env` a `.gitignore`, crea un `.env.example` sin contraseñas y retira `.env` del seguimiento con `git rm --cached .env`; si se publicaron credenciales reales, rótalas. Esta recomendación no impide usar el proyecto académico localmente.

Comprueba si tus cambios en `.env` aparecen en Git:

```bash
git status --short
```

**Esperado:** si aparece `M .env`, **no incluyas ese archivo en un commit**.

## 10. Instalar las 16 tablas inmobiliarias (`schema.sql`)

Comprueba primero que el script está presente:

```bash
ls -l db_esquema/schema.sql db_esquema/post_migracion.sql
```

**Advertencia:** `schema.sql` contiene instrucciones `CREATE TABLE`; está pensado para una base recién creada y **no** se debe ejecutar sobre una base ya preparada.

**Importar desde la raíz del repositorio:**

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria < db_esquema/schema.sql
```

**Resultado esperado:** si no hay error SQL, normalmente vuelve al prompt sin imprimir nada.

Valida el número de tablas de negocio:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "SELECT COUNT(*) AS total FROM information_schema.tables WHERE table_schema='inmobiliaria';"
```

**Esperado en este punto:** `total = 16`, siempre que la base estuviera vacía y aún no hayas hecho migraciones.

También puedes listarlas:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "SHOW TABLES;"
```

Entre ellas deben aparecer `cliente`, `inmueble`, `oferta`, `visita`, `oficina`, `propietario`, `vivienda`, `piso`, `casa`, `villa` y `local`.

**Por qué aún no existe `cliente.usuario_id`:** este campo **no está en `schema.sql`**; se añade después mediante `post_migracion.sql` cuando ya existe la tabla de usuarios de Django.

## 11. Validar Django y crear sus tablas (`migrate`)

Activa `.venv` si aún no lo está y asegúrate de estar junto a `manage.py`:

```bash
source .venv/bin/activate
python manage.py check
```

**Resultado esperado:**

```text
System check identified no issues (0 silenced).
```

Prueba la conexión real con el motor SQL:

```bash
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Conexion Django-MariaDB correcta')"
```

**Esperado:** `Conexion Django-MariaDB correcta`.

Revisa las migraciones:

```bash
python manage.py showmigrations
```

**Esperado:** aparecen aplicaciones como `admin`, `auth`, `contenttypes`, `sessions` y `cuentas`; en una base nueva algunas migraciones aparecerán con `[ ]`.

Aplícalas:

```bash
python manage.py migrate
```

**Resultado esperado:** aparecen líneas `Applying ... OK`, sin `OperationalError` ni `ProgrammingError`.

**Verifica que Django creó el usuario personalizado:**

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "SHOW TABLES LIKE 'cuentas_usuario';"
```

**Esperado:** una fila con `cuentas_usuario`. Si no existe, **no ejecutes `post_migracion.sql`**; revisa primero el error de migraciones.

> Las tablas de `apps/inmuebles/models.py` tienen `managed = False`: **Django no las crea ni altera automáticamente**. Las 16 tablas inmobiliarias provienen de `schema.sql`.

## 12. Agregar `cliente.usuario_id` (`post_migracion.sql`)

Este archivo contiene `ALTER TABLE cliente`, crea una relación única y apunta a `cuentas_usuario(id)`. Su función es unir el cliente comercial con su cuenta Django.

**Antes de ejecutarlo, comprueba que la columna todavía no exista:**

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "SHOW COLUMNS FROM cliente LIKE 'usuario_id';"
```

**Esperado antes de aplicar el script:** no devuelve ninguna fila de columna. Si ya aparece `usuario_id`, **no ejecutes el script otra vez**.

Ejecuta:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria < db_esquema/post_migracion.sql
```

**Resultado esperado:** como el script termina con `SHOW TABLES`, imprime el listado de tablas; no debe mostrar errores.

Valida la columna:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "DESCRIBE cliente;"
```

**Esperado:** una fila `usuario_id` de tipo `bigint(20)` (la presentación exacta puede variar), que acepta `NULL` y tiene una restricción única.

Valida la relación:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "SHOW CREATE TABLE cliente\G"
```

**Esperado:** aparecen `uq_cliente_usuario` y `fk_cliente_usuario`, con una referencia a `cuentas_usuario`.

**Error conocido `Unknown column 'cliente.usuario_id' in 'SELECT'`:** indica que omitiste este paso o estás conectado a otra base. Se manifestaba al entrar a **Gestión de clientes** y **Gestión de visitas**. **No cambies el HTML ni el template por este error**; verifica la estructura SQL.

**Error `Table 'cuentas_usuario' doesn't exist`:** se ejecutó el `post_migracion.sql` antes de `migrate`. Primero termina las migraciones.

**Error `Duplicate column name 'usuario_id'`:** ya se había ejecutado; no lo repitas. Verifica el resultado con `DESCRIBE cliente`.

## 13. Crear grupos y permisos (`crear_roles`)

El repositorio **sí trae** el comando de Django `apps/cuentas/management/commands/crear_roles.py`.

Ejecuta:

```bash
python manage.py crear_roles
```

**Resultado esperado exacto según el comando del repositorio:**

```text
Roles y permisos configurados correctamente.
```

Este comando crea o recupera los grupos `Administrador`, `Vendedor` y `Cliente`, y asigna permisos para inmuebles y usuarios según cada rol.

**Validación:**

```bash
python manage.py shell -c "from django.contrib.auth.models import Group; print(list(Group.objects.order_by('name').values_list('name', flat=True)))"
```

**Esperado:**

```text
['Administrador', 'Cliente', 'Vendedor']
```

**Error conocido `Group matching query does not exist` en `/cuentas/usuarios/crear/`:** la vista busca el nombre de grupo usando `Group.objects.get(name=rol)`; ocurre si no ejecutaste `crear_roles` después de restaurar la base. **La solución es ejecutar el comando del proyecto**, no crear los grupos manualmente sin permisos.

El comando `crear_roles` se puede repetir después de una migración que agregue permisos, porque utiliza `get_or_create` y `permissions.set(...)`; ten en cuenta que **restablece** los permisos de estos tres grupos a los que define el código.

## 14. Crear un administrador de prueba

En una base nueva, los usuarios de la instalación anterior **no existen**, porque el código Git no contiene los registros de MariaDB.

```bash
python manage.py createsuperuser
```

**Resultado esperado:** Django solicita datos como `Username`, `Email address` y `Password`, y finalmente confirma la creación del superusuario. Las contraseñas no se muestran al escribir.

Comprueba que existe al menos un superusuario:

```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(is_superuser=True).count())"
```

**Esperado:** un número igual o superior a `1` si creaste un superusuario.

> El modelo de autenticación es `cuentas.Usuario` (personalizado con correo único). Un superusuario se reconoce como Administrador en la lógica de roles del proyecto.

## 15. Datos de prueba (opcional)

El repositorio contiene `db_esquema/datos_prueba.sql`, con oficinas, zonas, propietarios, clientes, inmuebles y otros registros ficticios. **Solo debes cargarlo una vez** y en una base sin esos datos.

Comprueba primero si ya hay inmuebles:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria -e "SELECT COUNT(*) AS inmuebles FROM inmueble;"
```

Si la base está recién instalada, lo esperado es `0`. Si quieres insertar los datos de prueba:

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria < db_esquema/datos_prueba.sql
```

**Validación:** repite el `SELECT COUNT(*)`. En el script inspeccionado se crean **4 inmuebles de ejemplo**.

> Si ya habías ejecutado `datos_prueba.sql` o tienes datos propios, no vuelvas a importarlo: puede fallar con claves primarias duplicadas o insertar datos repetidos en otros catálogos.

## 16. Ejecutar y comprobar el sitio

Desde la carpeta del proyecto, con `.venv` activado:

```bash
python manage.py runserver
```

**Resultado esperado (representativo):**

```text
System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
```

Abre **http://127.0.0.1:8000/** en el navegador. Este servidor de desarrollo **no necesita que Apache o XAMPP estén funcionando**.

Pruebas funcionales sugeridas:

1. La página principal carga, y el CSS y JavaScript se muestran correctamente.
2. El inicio de sesión con el superusuario funciona.
3. Se abre el panel administrativo.
4. **Gestión de clientes** (`/inmuebles/gestion/clientes/`) carga sin el error de `usuario_id`.
5. **Gestión de visitas** (`/inmuebles/gestion/visitas/`) carga sin el mismo error.
6. **Crear usuario** (`/cuentas/usuarios/crear/`) permite registrar un usuario de prueba y asignar un rol, sin error `Group matching query does not exist`.
7. Si insertaste `datos_prueba.sql`, el catálogo y las listas muestran registros.

**Para detener Django:** `Ctrl + C` en su terminal. Puedes mantener el servicio MariaDB activo para la próxima vez.

## 17. Trabajar en una instalación existente, sin reinstalar nada

Cada vez que enciendas el computador:

```bash
# 1. Abre la carpeta local del repositorio:
cd ~/proyectos/Agencia-inmobiliaria

# 2. Comprueba la rama y los cambios locales:
git status

# 3. Trae cambios remotos solo después de revisar git status:
git pull

# 4. Activa el entorno:
source .venv/bin/activate

# 5. Comprueba que MariaDB está activo:
sudo systemctl is-active mariadb

# 6. Inicia Django:
python manage.py runserver
```

**Resultados esperados:** `git status` muestra el estado de la rama; `systemctl is-active` imprime `active`; Django anuncia `http://127.0.0.1:8000/`.

Si MariaDB no está activo:

```bash
sudo systemctl start mariadb
```

**No repitas** `schema.sql`, `post_migracion.sql`, `datos_prueba.sql`, `createsuperuser` ni la creación de la base cada día. Reinstala dependencias solo cuando cambie `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Si llegan nuevas migraciones con el código remoto, **revisa qué cambian** antes de ejecutar `python manage.py migrate`. Si llegan scripts SQL nuevos, aplícalos solo una vez, siguiendo su propia guía.

## 18. Git y GitHub en dos computadores

**Antes de editar:**

```bash
git status
git pull
```

**Después de editar, probar y verificar:**

```bash
python manage.py check
git status
git diff
```

Agrega **solo los archivos de código o documentación que deseas publicar**, por ejemplo:

```bash
git add apps/ config/ db_esquema/ README_Instrucciones.md
git status
git commit -m "fix: actualizar modulo de clientes"
git push
```

Ajusta la lista de rutas según los archivos realmente modificados. **No agregues `.env`, contraseñas, copias de la base de datos ni `.venv`**.

**Advertencia importante:** GitHub sincroniza el **código y scripts SQL versionados**, no los registros nuevos almacenados localmente en MariaDB. Un inmueble creado desde un computador **no aparece automáticamente** en la base del otro. Para compartir datos, utiliza un respaldo importado conscientemente o define un mecanismo de sincronización.

Si colaboras en equipo, cada persona puede trabajar en una rama y abrir un pull request; evita sobrescribir cambios ajenos o usar `git push --force` sin coordinación.

## 19. Consultas y respaldos de MariaDB

**Abrir la consola SQL:**

```bash
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria
```

**Consultas útiles dentro de MariaDB:**

```sql
SHOW TABLES;
DESCRIBE cliente;
SELECT COUNT(*) FROM cliente;
SELECT COUNT(*) FROM inmueble;
SELECT * FROM inmueble LIMIT 10;
SELECT VERSION();
EXIT;
```

**Crear un respaldo completo desde la terminal de Ubuntu:**

```bash
mkdir -p ~/respaldos_inmobiliaria
mariadb-dump -h 127.0.0.1 -u inmobiliaria_user -p --single-transaction inmobiliaria > ~/respaldos_inmobiliaria/respaldo_inmobiliaria.sql
ls -lh ~/respaldos_inmobiliaria/
```

**Esperado:** el archivo `.sql` existe y su tamaño es mayor que cero. El respaldo incluye estructura y datos existentes, incluidas tablas de Django (salvo que se hayan excluido expresamente). **No subas respaldos de datos personales o credenciales a GitHub**.

Restaurar un respaldo **no es lo mismo** que importar `schema.sql`. Si el respaldo es completo, revisa primero qué incluye y prepara una base de destino apropiada; **no ejecutes a continuación `schema.sql` ni `post_migracion.sql` a ciegas**, porque podrían intentar crear columnas y tablas ya restauradas.

## 20. Diagnóstico rápido de errores encontrados

| Error o síntoma | Causa probable | Comprobación o solución |
|---|---|---|
| `/bin/sh: pkg-config: not found` al instalar `mysqlclient` | Faltan herramientas/librerías de compilación. | Sección 5: instalar `build-essential`, `pkg-config`, `libmariadb-dev` y archivos de desarrollo de Python. |
| `Unit mariadb.service could not be found` | Solo hay cliente o no se registró el servidor. | Secciones 6–7: revisar paquetes, `mariadbd` y servicio. |
| Cliente 11.8 pero XAMPP 10.4 | Son productos/instalaciones distintas. | Verifica el servidor real con `SELECT VERSION()` y detén XAMPP MySQL si compite por `3306`. |
| `Access denied for user ...` | Usuario, clave o host incorrectos. | Probar conexión TCP y revisar `.env` y `SHOW GRANTS`. |
| `Can't connect to MySQL server` | Servidor detenido, puerto o host incorrecto. | `sudo systemctl status mariadb`; `sudo ss -ltnp | grep ':3306'`. |
| `No module named django` | `.venv` desactivado o dependencias no instaladas. | `source .venv/bin/activate` y `pip install -r requirements.txt`. |
| `Table ... doesn't exist` | Script SQL o migraciones faltantes. | `SHOW TABLES` y verificar orden de secciones 10–12. |
| `Unknown column 'cliente.usuario_id'` | Falta `post_migracion.sql`. | Comprobar `cuentas_usuario` y `DESCRIBE cliente`; aplicar script **solo si falta**. |
| `Group matching query does not exist` | Grupos de Django vacíos después de recrear la BD. | `python manage.py crear_roles`. |
| `Duplicate column name 'usuario_id'` | Se ejecutó `post_migracion.sql` dos veces. | No repetir; `DESCRIBE cliente`. |
| `Table ... already exists` al importar | Se está cargando el esquema en una BD ya creada. | Detenerse; comprobar contenido, respaldar y evitar importaciones duplicadas. |
| `Address already in use` en puerto 8000 | Otro proceso ocupa el puerto Django. | `python manage.py runserver 8001` y abrir `http://127.0.0.1:8001/`. |
| El sitio abre pero falla una operación | Falta verificar datos, columnas, roles o permisos. | Seguir prueba funcional de sección 16 y revisar el traceback. |
| `git pull` muestra conflictos | Modificaciones locales compiten con remotas. | Revisar `git status` y resolver conflictos; no borrar cambios sin respaldo. |

## 21. Lista de verificación final

- [ ] Estoy dentro del repositorio correcto y existe `manage.py`.
- [ ] Python es compatible y `.venv` está activado.
- [ ] `pip install -r requirements.txt` terminó correctamente.
- [ ] `python -m django --version` devuelve `6.1.3` en el entorno de referencia.
- [ ] MariaDB **Server** está activo y `SELECT VERSION()` devuelve la versión esperada.
- [ ] No hay conflicto entre MariaDB de Ubuntu y MySQL/MariaDB de XAMPP.
- [ ] Django usa las credenciales locales correctas de `.env`.
- [ ] Las 16 tablas de `schema.sql` están creadas.
- [ ] `python manage.py migrate` terminó sin errores.
- [ ] Existe `cuentas_usuario`.
- [ ] Existe `cliente.usuario_id` y su clave foránea.
- [ ] `python manage.py crear_roles` terminó correctamente.
- [ ] Existen los grupos Administrador, Cliente y Vendedor.
- [ ] Existe una cuenta administradora.
- [ ] `python manage.py check` pasa sin errores.
- [ ] El sitio carga y las secciones de clientes, visitas y creación de usuarios funcionan.
- [ ] No voy a subir `.env`, contraseñas ni respaldos a GitHub.

---

**Secuencia resumida para una base de datos totalmente nueva:**

```bash
# Ejecutar desde la raíz del repositorio, después de crear la BD,
# configurar .env y activar .venv.

mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria < db_esquema/schema.sql
python manage.py check
python manage.py migrate
mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria < db_esquema/post_migracion.sql
python manage.py crear_roles
python manage.py createsuperuser
# Opcional, solo en BD nueva:
# mariadb -h 127.0.0.1 -u inmobiliaria_user -p inmobiliaria < db_esquema/datos_prueba.sql
python manage.py runserver
```

**Fin de la guía.**
