# 🏠 Sistema de Gestión Inmobiliaria

### Proyecto académico — Aplicaciones en Internet

**Universidad Distrital Francisco José de Caldas**  
**Facultad Tecnológica**  
**Tecnología en Sistematización de Datos**

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.1.3-darkgreen?logo=django)
![MariaDB](https://img.shields.io/badge/MariaDB-11.8.6-brown?logo=mariadb)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow?logo=javascript)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-orange)

**Repositorio:** [Juanchi-Reyes/Agencia-inmobiliaria](https://github.com/Juanchi-Reyes/Agencia-inmobiliaria)

---

## 📑 Tabla de contenido

1. [Descripción del proyecto](#1-descripción-del-proyecto)
2. [Objetivos](#2-objetivos)
3. [Tecnologías utilizadas](#3-tecnologías-utilizadas)
4. [Arquitectura del sistema](#4-arquitectura-del-sistema)
5. [Estructura del proyecto](#5-estructura-del-proyecto)
6. [Base de datos](#6-base-de-datos)
7. [Roles y permisos](#7-roles-y-permisos)
8. [Módulos implementados](#8-módulos-implementados)
9. [Módulos pendientes y mejoras](#9-módulos-pendientes-y-mejoras)
10. [Instalación y configuración](#10-instalación-y-configuración)
11. [Ejecución del sistema](#11-ejecución-del-sistema)
12. [Pruebas y validaciones](#12-pruebas-y-validaciones)
13. [Reglas de desarrollo](#13-reglas-de-desarrollo)
14. [Plan de trabajo](#14-plan-de-trabajo)
15. [Equipo de desarrollo](#15-equipo-de-desarrollo)
16. [Estado general y alcance](#16-estado-general-y-alcance)

---

## 1. Descripción del proyecto

El **Sistema de Gestión Inmobiliaria** es una aplicación web desarrollada con Django y MariaDB cuyo propósito es centralizar y automatizar los procesos administrativos y comerciales de una agencia inmobiliaria.

El sistema permite administrar información relacionada con inmuebles, propietarios, clientes, usuarios, ofertas comerciales y visitas, mediante una interfaz web organizada según los permisos y responsabilidades de cada usuario.

La aplicación contempla tres perfiles principales:

- **Administrador:** encargado de la administración general del sistema.
- **Vendedor:** responsable de la gestión comercial de inmuebles, propietarios, clientes y visitas.
- **Cliente:** usuario que consulta inmuebles disponibles, podrá solicitar visitas y consultar sus solicitudes.

El proyecto utiliza una arquitectura web basada en el patrón **Model-View-Template (MVT)** de Django y una base de datos relacional que garantiza la integridad de la información mediante claves primarias, claves foráneas y restricciones.

### Problema que busca resolver

Una agencia inmobiliaria necesita mantener organizada la información de sus propiedades, propietarios, clientes, ofertas y visitas.

Cuando estos procesos se realizan manualmente o mediante herramientas independientes, pueden presentarse dificultades como:

- Duplicidad y desorganización de registros.
- Dificultad para consultar la disponibilidad y características de los inmuebles.
- Falta de centralización de la información comercial.
- Problemas para coordinar visitas.
- Ausencia de controles diferenciados según el personal.
- Dificultad para generar estadísticas de la operación.

El sistema propone integrar estas actividades en una única plataforma web, facilitando la consulta, administración y seguimiento de la información inmobiliaria.

### Alcance

El proyecto es de carácter **académico** y se encuentra en desarrollo.

Su objetivo es construir una aplicación funcional que permita demostrar conocimientos de desarrollo web, programación orientada a objetos, bases de datos relacionales, arquitectura de software, autenticación, autorización y operaciones CRUD.

No se contempla inicialmente la implementación de pagos electrónicos, firma digital de contratos ni procesamiento de transacciones bancarias.

---

## 2. Objetivos

### Objetivo general

Desarrollar un sistema de información web para una agencia inmobiliaria, utilizando Django y MariaDB, que permita centralizar la gestión de inmuebles, propietarios, clientes, ofertas comerciales y visitas, mediante funcionalidades diferenciadas por roles de usuario.

### Objetivos específicos

1. **Diseñar e implementar** una base de datos relacional que permita almacenar y relacionar la información administrativa y comercial de la inmobiliaria, garantizando su integridad y consistencia.

2. **Desarrollar** un sistema de autenticación y autorización que controle el acceso a las funcionalidades según los roles Administrador, Vendedor y Cliente.

3. **Implementar** módulos de gestión de inmuebles, propietarios, clientes y ofertas comerciales que permitan registrar, consultar, modificar y, cuando corresponda, eliminar información.

4. **Desarrollar** un módulo de visitas que permita registrar, consultar y administrar las solicitudes de los clientes.

5. **Incorporar** herramientas de búsqueda y filtrado de inmuebles para facilitar la consulta de propiedades según diferentes criterios.

6. **Implementar** reportes y estadísticas que permitan visualizar información relevante sobre la operación de la agencia.

7. **Diseñar** una interfaz web responsiva y consistente que facilite la interacción de los diferentes tipos de usuarios.

---

## 3. Tecnologías utilizadas

### Backend

| Tecnología | Descripción |
|---|---|
| Python 3.14.4 | Lenguaje principal de programación |
| Django 6.1.3 | Framework para desarrollo web |
| Django ORM | Acceso y manipulación de datos mediante modelos |
| Django Authentication | Autenticación, sesiones y permisos |
| Django Forms | Formularios y validaciones |
| Django Templates | Generación dinámica de páginas HTML |

### Frontend

| Tecnología | Descripción |
|---|---|
| HTML5 | Estructura de las páginas |
| CSS3 | Diseño visual y responsivo |
| JavaScript | Interactividad del lado del cliente |
| Google Material Symbols | Iconografía de la interfaz |
| Django Template Language | Integración de datos del backend en HTML |

### Base de datos

| Tecnología | Descripción |
|---|---|
| MariaDB | Sistema gestor de bases de datos relacional |
| SQL | Definición y consulta de datos |
| InnoDB | Motor de almacenamiento |
| Django ORM | Interacción entre Python y MariaDB |

El desarrollo local se ha realizado con MariaDB 11.8.6. El esquema SQL también se diseñó considerando compatibilidad con MySQL moderno.

### Herramientas de desarrollo

- Visual Studio Code.
- Git.
- GitHub.
- Ubuntu Linux.
- Terminal de Linux.
- Entornos virtuales de Python.
- XAMPP/LAMPP, utilizado durante etapas de configuración.
- MariaDB como servicio del sistema operativo.

### Entorno de desarrollo

El proyecto se ha trabajado principalmente en:

- Sistema operativo: Ubuntu Linux.
- Servidor web de desarrollo: Django.
- Base de datos: MariaDB.
- Puerto habitual de Django: `8000`.
- Puerto habitual de MariaDB: `3306`.

---

## 4. Arquitectura del sistema

El proyecto utiliza el patrón arquitectónico **MVT (Model-View-Template)**, característico de Django.

### Model — Modelo

Representa las entidades y relaciones de la base de datos.

Los modelos permiten consultar, registrar, actualizar y eliminar información mediante el ORM de Django.

Ejemplos:

- Usuario.
- Cliente.
- Propietario.
- Inmueble.
- Oferta.
- Visita.
- Oficina.
- Zona.

### View — Vista

Contiene la lógica que procesa las solicitudes HTTP.

Las vistas reciben las peticiones, comprueban permisos, procesan formularios, ejecutan operaciones y devuelven respuestas.

Ejemplos:

- Registrar un inmueble.
- Editar un propietario.
- Iniciar sesión.
- Consultar ofertas.
- Verificar un código de recuperación.
- Listar visitas.

### Template — Plantilla

Representa la interfaz HTML presentada al usuario.

Las plantillas reciben información de las vistas y la muestran mediante Django Template Language.

### URL Routing

Los archivos `urls.py` relacionan las direcciones del sistema con sus vistas correspondientes.

### Services — Servicios

El proyecto utiliza archivos de servicios para separar las operaciones de negocio de las vistas.

Su propósito es:

- Centralizar procesos.
- Evitar duplicación de código.
- Organizar operaciones complejas.
- Gestionar transacciones.
- Facilitar el mantenimiento y las pruebas.

### Flujo general de una solicitud

```text
Usuario
   |
   v
Navegador web
   |
   v
URL solicitada
   |
   v
urls.py
   |
   v
views.py
   |
   +------> forms.py
   |          |
   |          v
   |      Validaciones
   |
   +------> services.py
   |          |
   |          v
   |       models.py
   |          |
   |          v
   |       MariaDB
   |
   v
Template HTML
   |
   v
Respuesta al navegador
```

El proyecto no requiere que todas sus operaciones utilicen AJAX. La mayoría de los formularios pueden procesarse mediante solicitudes HTTP tradicionales, mientras que JavaScript se utiliza para mejorar la interacción de la interfaz.

---

## 5. Estructura del proyecto

La estructura general del repositorio se organiza de la siguiente manera:

```text
Agencia-inmobiliaria/
│
├── apps/
│   │
│   ├── cuentas/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── crear_roles.py
│   │   │
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── roles.py
│   │   ├── decorators.py
│   │   └── servicios.py
│   │
│   └── inmuebles/
│       ├── migrations/
│       ├── templates/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── services.py
│       └── ofertas_services.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

> Esta estructura presenta los principales archivos de la aplicación. Pueden existir otros directorios, archivos de servicios, recursos estáticos, scripts SQL y documentación complementaria.

### Responsabilidad de los archivos principales

| Archivo | Responsabilidad |
|---|---|
| `manage.py` | Ejecutar comandos administrativos de Django |
| `config/settings.py` | Configuración general del proyecto |
| `config/urls.py` | Enrutamiento principal |
| `models.py` | Representación de entidades |
| `views.py` | Procesamiento de solicitudes |
| `forms.py` | Formularios y validaciones |
| `urls.py` | Definición de endpoints |
| `services.py` | Lógica de negocio |
| `ofertas_services.py` | Operaciones comerciales de ofertas |
| `roles.py` | Identificación de roles |
| `decorators.py` | Restricciones de acceso |
| `templates/` | Interfaces HTML |
| `static/` | Archivos CSS y JavaScript |
| `crear_roles.py` | Configuración de grupos y permisos |

---

## 6. Base de datos

La base de datos principal se denomina:

```sql
inmobiliaria
```

Se utiliza un modelo relacional con tablas especializadas para representar los distintos tipos de inmuebles.

### 6.1. Tablas principales

El esquema inmobiliario contiene las siguientes 16 tablas:

| Tabla | Descripción |
|---|---|
| `oficina` | Oficinas de la inmobiliaria |
| `zona` | Zonas geográficas |
| `propietario` | Propietarios de inmuebles |
| `cliente` | Información comercial de clientes |
| `inmueble` | Información general de las propiedades |
| `oferta` | Ofertas de venta y alquiler |
| `vivienda` | Clasificación de inmuebles residenciales |
| `piso` | Información específica de pisos |
| `casa` | Información específica de casas |
| `villa` | Información específica de villas |
| `local` | Información específica de locales |
| `estancia` | Catálogo de estancias |
| `vivienda_estancia` | Relación entre viviendas y estancias |
| `caracteristica` | Catálogo de características |
| `inmueble_caracteristica` | Características asociadas a inmuebles |
| `visita` | Registro de visitas a propiedades |

Adicionalmente, Django utiliza sus propias tablas para autenticación, permisos, grupos, sesiones y migraciones.

### 6.2. Tipos de inmuebles

El sistema contempla cuatro tipos:

**Piso (`PISO`)**

Inmueble residencial que puede clasificarse según su estado.

**Casa (`CASA`)**

Inmueble residencial con sus correspondientes características y estancias.

**Villa (`VILLA`)**

Inmueble residencial con información adicional, como superficie de parcela y urbanización.

**Local (`LOCAL`)**

Inmueble comercial con atributos como número de puertas, acondicionamiento y distribución diáfana.

### 6.3. Ofertas comerciales

Un inmueble puede contar con ofertas de:

- Venta.
- Alquiler.

El modelo permite registrar modalidades comerciales con precios y condiciones diferenciadas.

La base de datos impide duplicar una misma modalidad para el mismo inmueble.

### 6.4. Integridad referencial

El esquema utiliza:

- Claves primarias.
- Claves foráneas.
- Restricciones `UNIQUE`.
- Restricciones `CHECK`.
- Relaciones uno a muchos.
- Relaciones uno a uno.
- Tablas intermedias para relaciones muchos a muchos.
- Restricciones de eliminación y actualización.

### 6.5. Administración del esquema

Parte del esquema inmobiliario fue creado mediante scripts SQL.

Varios modelos utilizan:

```python
class Meta:
    managed = False
```

Esto significa que Django puede consultar y modificar registros mediante dichos modelos, pero no administra automáticamente la creación y modificación estructural de esas tablas.

Por lo tanto, los cambios de estructura en estas entidades deben coordinarse con los scripts SQL correspondientes.

---

## 7. Roles y permisos

El sistema contempla tres grupos de usuarios.

### 7.1. Administrador

Responsable de la administración general de la plataforma.

Funciones contempladas:

- Gestionar usuarios.
- Asignar roles.
- Activar y desactivar cuentas.
- Gestionar inmuebles.
- Gestionar propietarios.
- Gestionar clientes.
- Gestionar ofertas.
- Administrar visitas.
- Administrar oficinas y zonas.
- Consultar reportes y estadísticas.

Algunas de estas funcionalidades se encuentran pendientes de implementación o integración.

### 7.2. Vendedor

Responsable de las actividades comerciales.

**Permisos esperados al finalizar el proyecto:**

- Consultar inmuebles.
- Registrar inmuebles.
- Modificar inmuebles.
- Consultar propietarios.
- Registrar propietarios.
- Modificar propietarios.
- Consultar clientes.
- Registrar clientes.
- Modificar clientes.
- Registrar visitas.
- Consultar visitas.
- Modificar visitas.
- Eliminar visitas.
- Consultar información comercial.

**Restricciones:**

- No eliminar inmuebles.
- No eliminar clientes.
- No administrar usuarios del sistema.
- No modificar roles o permisos.
- No acceder a configuraciones administrativas restringidas.

La eliminación de propietarios también deberá reservarse al administrador.

### 7.3. Cliente

Usuario interesado en consultar propiedades.

Funciones contempladas:

- Registrarse.
- Iniciar sesión.
- Consultar el catálogo.
- Consultar detalles de inmuebles.
- Recuperar su contraseña mediante el mecanismo académico.
- Solicitar visitas a inmuebles.
- Consultar el estado de sus solicitudes.
- Consultar su información personal.

Las solicitudes de visitas y el portal ampliado del cliente están pendientes.

### 7.4. Matriz de permisos objetivo

| Funcionalidad | Administrador | Vendedor | Cliente |
|---|---|---|---|
| Consultar inmuebles | Sí | Sí | Sí |
| Crear inmuebles | Sí | Sí | No |
| Editar inmuebles | Sí | Sí | No |
| Eliminar inmuebles | Sí | No | No |
| Gestionar usuarios | Sí | No | No |
| Consultar clientes | Sí | Sí | Solo su información |
| Crear clientes | Sí | Sí | Mediante registro |
| Editar clientes | Sí | Sí | Solo su información autorizada |
| Eliminar clientes | Sí | No | No |
| Consultar propietarios | Sí | Sí | No |
| Crear propietarios | Sí | Sí | No |
| Editar propietarios | Sí | Sí | No |
| Eliminar propietarios | Sí | No | No |
| Gestionar oficinas y zonas | Sí | No | No |
| Crear visitas | Sí | Sí | Solicitar |
| Consultar visitas | Sí | Sí | Solo las propias |
| Editar visitas | Sí | Sí | No |
| Eliminar visitas | Sí | Sí | No |
| Consultar reportes | Sí | Según autorización | No |
| Consultar su propia cuenta | Sí | Sí | Sí |
| Editar sus datos personales | Sí | Sí | Sí |
| Cambiar su contraseña | Sí | Sí | Sí |
| Modificar su propio rol | No | No | No |

**Nota:** esta matriz representa el comportamiento esperado al finalizar el desarrollo. Actualmente existen permisos y funcionalidades pendientes de corregir, especialmente en el rol Vendedor.

---

## 8. Módulos implementados

En esta sección se documentan los componentes que ya tienen una implementación en el proyecto.

### 8.1. Autenticación y gestión de sesiones

**Estado: Implementado**

Funcionalidades:

- Inicio de sesión mediante credenciales.
- Registro de usuarios.
- Cierre de sesión.
- Autenticación con Django.
- Redirección según el rol.
- Protección de vistas.
- Manejo de sesiones.
- Validaciones de formularios.

### 8.2. Recuperación de contraseña

**Estado: Implementado; pendiente de validación final**

Se desarrolló un mecanismo académico de recuperación que utiliza un código temporal mostrado en el navegador.

Flujo:

1. El usuario selecciona la opción de recuperar contraseña.
2. Identifica su cuenta.
3. El sistema genera un código de seis dígitos.
4. Se muestra el código de demostración.
5. El usuario introduce el código.
6. Django comprueba su validez.
7. Se permite establecer una nueva contraseña.
8. El usuario regresa al inicio de sesión.

Características:

- Código numérico aleatorio.
- Vigencia de diez minutos.
- Límite de cinco intentos.
- Validación de contraseñas mediante Django.
- Almacenamiento de contraseñas mediante hash.
- Invalidación de códigos utilizados.

**Advertencia:** este mecanismo no verifica la identidad real del titular, ya que el código se muestra al solicitante. Debe utilizarse únicamente en desarrollo local y no publicarse como sistema de recuperación de producción.

### 8.3. Gestión de usuarios

**Estado: Implementado con mejoras pendientes**

Funcionalidades:

- Listado de usuarios.
- Creación de usuarios.
- Edición de usuarios.
- Asignación de grupos.
- Desactivación de cuentas.
- Reactivación de cuentas.
- Restricciones para proteger cuentas administrativas.

**Pendiente:** corregir la captura y sincronización del teléfono al crear o editar usuarios asociados al rol Cliente.

### 8.4. Paneles por rol

**Estado: Implementado parcialmente**

Existen paneles diferenciados para:

- Administrador.
- Vendedor.
- Cliente.

El administrador dispone de indicadores generales relacionados con usuarios, clientes, inmuebles y propietarios.

El vendedor cuenta con un panel propio, pero todavía requiere integración y corrección de accesos a determinadas funcionalidades.

El cliente cuenta con un panel inicial, pendiente de ampliación.

### 8.5. Catálogo público de inmuebles

**Estado: Implementado**

Permite:

- Consultar inmuebles registrados.
- Visualizar propiedades.
- Consultar información general.
- Acceder al detalle de inmuebles.
- Consultar modalidades comerciales disponibles.

**Pendiente:** incorporar búsqueda avanzada, filtros combinados e imágenes de propiedades.

### 8.6. Gestión de inmuebles

**Estado: Implementado con ajustes pendientes**

Incluye:

- Listado administrativo.
- Registro de inmuebles.
- Edición de inmuebles.
- Eliminación autorizada.
- Validación de formularios.
- Identificación mediante referencia.
- Clasificación por tipo.
- Asociación con propietarios.
- Asociación con oficinas y zonas.
- Registro de información específica según el tipo.

El sistema utiliza servicios para centralizar operaciones de creación, actualización y eliminación.

**Pendiente:** garantizar el acceso correcto del vendedor a todas las operaciones autorizadas y restringir la eliminación exclusivamente al administrador.

### 8.7. Gestión de propietarios

**Estado: Implementado con ajustes pendientes**

Incluye rutas y vistas para:

- Listar propietarios.
- Registrar propietarios.
- Consultar detalles.
- Editar propietarios.
- Eliminar propietarios mediante autorización.

**Pendiente:** corregir el acceso del vendedor para permitir consulta, creación y edición, sin eliminación.

### 8.8. Gestión de ofertas comerciales

**Estado: Implementado**

Permite gestionar las ofertas asociadas a los inmuebles.

Funcionalidades:

- Consultar ofertas.
- Registrar ofertas.
- Editar ofertas.
- Eliminar ofertas autorizadas.
- Asociar ofertas a inmuebles.
- Diferenciar venta y alquiler.
- Registrar precios y condiciones comerciales.

La lógica principal está separada en servicios especializados.

### 8.9. Gestión de características y estancias

**Estado: Implementado**

El proyecto cuenta con funcionalidades para administrar los atributos de los inmuebles.

Incluye:

- Asociación de características.
- Modificación de características asignadas.
- Eliminación de asociaciones.
- Asociación de estancias.
- Registro de cantidades.
- Modificación de estancias.
- Catálogos generales de atributos.

### 8.10. Gestión de visitas

**Estado: Implementación parcial; requiere revisión y ampliación**

La base de datos dispone de la entidad `visita` y el proyecto contiene rutas para operaciones relacionadas con visitas.

Las funcionalidades contempladas incluyen:

- Listar visitas.
- Registrar visitas.
- Consultar detalles.
- Administrar información de las visitas.

**Pendiente:** completar y verificar el CRUD, especialmente para el vendedor, e integrar las solicitudes realizadas desde el portal del cliente.

---

## 9. Módulos pendientes y mejoras

Esta sección constituye la hoja de ruta para completar el sistema.

### 9.1. Portal del Cliente y solicitud de visitas

**Estado: Pendiente**

**Prioridad: Alta**

Se ampliará el panel del cliente para ofrecer funcionalidades comerciales.

Requerimientos:

- Mostrar información del cliente autenticado.
- Consultar propiedades disponibles.
- Acceder al detalle de cada inmueble.
- Solicitar una visita desde el detalle.
- Seleccionar fecha y hora.
- Registrar observaciones.
- Asociar la solicitud con el cliente y el inmueble.
- Consultar las visitas solicitadas.
- Mostrar el estado de las solicitudes.
- Impedir que un cliente consulte las visitas de otro.

Se evaluará ampliar la tabla `visita` para incorporar estados como:

- Pendiente.
- Confirmada.
- Realizada.
- Cancelada.

La incorporación de estados requiere una modificación controlada del esquema SQL.

### 9.2. Gestión de oficinas y zonas

**Estado: Pendiente**

**Prioridad: Media**

Se desarrollarán interfaces administrativas para las tablas `oficina` y `zona`.

#### Oficinas

- Listar oficinas.
- Registrar oficinas.
- Consultar detalles.
- Modificar información.
- Eliminar oficinas cuando no existan restricciones de integridad.
- Asociar oficinas con inmuebles.

#### Zonas

- Listar zonas.
- Registrar zonas.
- Consultar detalles.
- Editar zonas.
- Eliminar zonas cuando sea permitido.
- Asociar zonas con inmuebles.

Estas operaciones estarán reservadas al administrador.

### 9.3. Búsqueda avanzada de inmuebles

**Estado: Pendiente**

**Prioridad: Alta**

Se implementará un sistema de filtros para facilitar la búsqueda de propiedades.

Criterios propuestos:

- Referencia.
- Tipo de inmueble.
- Dirección.
- Zona.
- Modalidad comercial.
- Precio mínimo.
- Precio máximo.
- Superficie mínima.
- Superficie máxima.
- Características.
- Estancias.

Se contempla:

- Combinar varios filtros.
- Limpiar filtros.
- Ordenar resultados.
- Mostrar el número de coincidencias.
- Presentar un mensaje cuando no existan resultados.
- Incorporar paginación.

Los filtros deberán realizarse mediante consultas al backend y no depender exclusivamente de JavaScript.

### 9.4. Reportes y estadísticas

**Estado: Pendiente**

**Prioridad: Media**

Se desarrollará un módulo de reportes administrativos con fichas informativas.

#### Fichas de reporte propuestas

- Total de inmuebles.
- Inmuebles por tipo.
- Inmuebles en venta.
- Inmuebles en alquiler.
- Total de propietarios.
- Total de clientes.
- Total de visitas.
- Visitas por periodo.
- Distribución de inmuebles por zona.
- Distribución de inmuebles por oficina.
- Promedios de precios de oferta.

Se contempla utilizar tarjetas estadísticas, tablas y gráficos.

Los reportes deberán obtener la información directamente de la base de datos y respetar los permisos de acceso.

### 9.5. Estandarización de botones e interfaz

**Estado: Pendiente**

**Prioridad: Media**

Se revisará la interfaz para mantener una presentación consistente.

Actividades:

- Unificar botones de crear.
- Unificar botones de editar.
- Unificar botones de eliminar.
- Unificar botones de consultar.
- Unificar botones de guardar.
- Unificar botones de cancelar.
- Mantener tamaños y espacios consistentes.
- Estandarizar iconos.
- Incorporar confirmaciones en acciones destructivas.
- Revisar el diseño responsivo.
- Mejorar los mensajes de validación.
- Mantener coherencia entre paneles.

Los estilos se centralizarán en un único archivo CSS externo.

### 9.6. Corrección del registro de clientes y usuarios

**Estado: Pendiente de corrección**

**Prioridad: Alta**

Se identificó una inconsistencia en la creación de clientes desde la administración.

Actualmente, el registro público permite capturar el teléfono, pero el formulario administrativo de creación de usuarios no solicita adecuadamente ese dato al crear una cuenta con rol Cliente.

#### Correcciones necesarias

- Incorporar el campo teléfono en el formulario administrativo.
- Validar el formato y la longitud.
- Guardar el teléfono en el perfil comercial.
- Mantener sincronizados los datos correspondientes.
- Permitir editar el teléfono.
- Evitar perfiles incompletos.
- Revisar las relaciones entre Usuario y Cliente.
- Validar la creación y edición de usuarios con rol Cliente.

#### Funcionalidades del vendedor

El vendedor deberá poder:

- Consultar clientes.
- Registrar clientes.
- Editar clientes.

No deberá poder eliminar clientes ni administrar los roles de los usuarios.

### 9.7. Gestión de inmuebles para vendedores

**Estado: Pendiente de corrección y validación**

**Prioridad: Alta**

Se corregirán los accesos y permisos del rol Vendedor.

El vendedor deberá poder:

- Listar inmuebles.
- Consultar detalles.
- Registrar inmuebles.
- Editar inmuebles.
- Gestionar sus atributos autorizados.
- Consultar las ofertas relacionadas.

**Restricción obligatoria:** no podrá eliminar inmuebles.

Los controles deben aplicarse tanto en la interfaz como en el backend.

Ocultar un botón no constituye una restricción suficiente.

### 9.8. Gestión completa de visitas para vendedores

**Estado: Pendiente de completar y validar**

**Prioridad: Alta**

Se implementará el CRUD completo de visitas para el vendedor.

Funcionalidades:

- Registrar visitas.
- Consultar visitas.
- Consultar detalles.
- Editar fecha y hora.
- Modificar observaciones.
- Eliminar visitas.
- Asociar clientes e inmuebles.
- Validar la existencia de las entidades relacionadas.
- Evitar registros con datos inválidos.

La eliminación de visitas deberá ejecutarse únicamente mediante solicitudes autorizadas y con confirmación.

### 9.9. Corrección de permisos y navegación del vendedor

**Estado: Pendiente**

**Prioridad: Alta**

Se identificaron problemas de acceso a las funciones de inmuebles y propietarios desde el panel del vendedor.

Actividades:

- Revisar los permisos del grupo Vendedor.
- Revisar los decoradores de las vistas.
- Revisar las condiciones de acceso.
- Corregir enlaces del panel.
- Habilitar la gestión autorizada de inmuebles.
- Habilitar la gestión autorizada de propietarios.
- Evitar errores HTTP 403 en operaciones permitidas.
- Mantener los errores HTTP 403 en operaciones restringidas.
- Verificar que las reglas se apliquen a solicitudes directas por URL.

### 9.10. Almacenamiento de imágenes de inmuebles

**Estado: Pendiente**

**Prioridad: Alta**

Se incorporará soporte para imágenes asociadas a los inmuebles.

#### Requerimientos

- Permitir subir imágenes desde formularios.
- Almacenar los archivos en el sistema de archivos.
- Guardar en MariaDB únicamente la ruta o referencia del archivo.
- Asociar cada imagen con un inmueble.
- Mostrar imágenes en el catálogo.
- Mostrar imágenes en el detalle.
- Permitir actualizar imágenes.
- Permitir eliminar imágenes.
- Validar formatos y tamaños.

#### Diseño propuesto

Se podrá incorporar una tabla específica:

```sql
CREATE TABLE inmueble_imagen (
    id_imagen INT AUTO_INCREMENT PRIMARY KEY,
    id_inmueble INT NOT NULL,
    ruta_imagen VARCHAR(255) NOT NULL,
    es_principal BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_imagen_inmueble
        FOREIGN KEY (id_inmueble)
        REFERENCES inmueble(id_inmueble)
        ON DELETE CASCADE
);
```

Este esquema es una propuesta y todavía no forma parte de la estructura implementada.

Los archivos podrán almacenarse en un directorio como:

```text
media/
└── inmuebles/
    ├── propiedad_001/
    ├── propiedad_002/
    └── propiedad_003/
```

Se deberá configurar el manejo de archivos multimedia de Django mediante `MEDIA_ROOT` y `MEDIA_URL`.


### 9.11. Mi cuenta — Perfil de usuario

**Estado: Pendiente**

**Prioridad: Alta**

Se implementará un módulo de gestión del perfil personal, disponible para todos los usuarios autenticados, independientemente de su rol.

El objetivo es permitir que cada usuario pueda consultar y actualizar su información personal sin necesidad de solicitar la intervención de un administrador.

#### Acceso al módulo

Se incorporará un icono de cuenta en el `header` principal de la aplicación, utilizando Google Material Symbols.

El icono estará visible para los usuarios autenticados de los tres roles:

- Administrador.
- Vendedor.
- Cliente.

Al seleccionar el icono, se mostrará un menú con las siguientes opciones:

- **Mi cuenta:** acceder al perfil personal.
- **Cerrar sesión:** finalizar la sesión actual.

El icono y sus opciones deberán conservar una apariencia consistente en los diferentes paneles.

#### Información del perfil

La sección **Mi cuenta** mostrará los datos disponibles del usuario autenticado:

- Nombre.
- Apellidos, si se almacenan por separado.
- Nombre de usuario.
- Correo electrónico.
- Número de teléfono.
- Rol asignado.
- Estado de la cuenta.
- Fecha de registro, si está disponible.

La información deberá obtenerse directamente de la base de datos, utilizando la sesión del usuario autenticado.

#### Consulta de información

El usuario podrá visualizar sus datos personales mediante una interfaz organizada y de fácil comprensión.

El sistema deberá:

- Identificar automáticamente al usuario autenticado.
- Mostrar únicamente la información correspondiente a su cuenta.
- Presentar los datos de manera clara.
- Permitir acceder al formulario de edición.
- Mantener el diseño visual utilizado en el resto de la aplicación.

#### Actualización de datos personales

Se incorporará un formulario que permita modificar los datos personales autorizados.

**Campos editables propuestos:**

- Nombre.
- Apellidos.
- Correo electrónico.
- Número de teléfono.

El formulario deberá cargar automáticamente la información existente y permitir guardar los cambios.

**Campos restringidos:**

- Identificador del usuario.
- Rol asignado.
- Permisos.
- Estado de activación.
- Información administrativa del sistema.

Estos campos no podrán modificarse desde el perfil personal.

#### Cambio de contraseña

Se incorporará una opción para cambiar la contraseña desde la cuenta del usuario.

El procedimiento deberá:

1. Solicitar la contraseña actual.
2. Validar que corresponda al usuario autenticado.
3. Solicitar una nueva contraseña.
4. Solicitar la confirmación de la nueva contraseña.
5. Verificar que ambas contraseñas coincidan.
6. Aplicar las validaciones de seguridad de Django.
7. Guardar la nueva contraseña mediante hash.
8. Mostrar un mensaje de confirmación.

El cambio de contraseña deberá realizarse mediante los mecanismos de autenticación de Django.

#### Relación entre Usuario y Cliente

Cuando el usuario autenticado pertenezca al rol Cliente, el módulo deberá mantener la consistencia entre su cuenta y su registro comercial.

En particular:

- El nombre deberá mantenerse sincronizado cuando corresponda.
- El número de teléfono deberá actualizarse en el registro de cliente.
- La actualización deberá respetar la relación entre ambas entidades.
- Se deberán evitar registros duplicados.
- Los cambios deberán realizarse mediante operaciones controladas.

Para los usuarios Administrador y Vendedor, se utilizará la información disponible en sus respectivos registros, sin crear perfiles comerciales innecesarios.

#### Validaciones y seguridad

El módulo deberá cumplir las siguientes condiciones:

- Requerir una sesión activa.
- Impedir el acceso a perfiles de otros usuarios mediante modificación de URL.
- Validar los campos obligatorios.
- Validar el formato del correo electrónico.
- Validar el formato y longitud del teléfono.
- Evitar conflictos con nombres de usuario o correos que deban ser únicos.
- Utilizar protección CSRF.
- Mostrar mensajes de error y confirmación.
- No permitir modificar roles ni permisos desde el perfil.
- Utilizar las herramientas de Django para el cambio de contraseña.

#### Interfaz propuesta

Se desarrollarán las siguientes vistas:

**1. Mi cuenta**

Página que presenta la información del usuario autenticado.

**2. Editar perfil**

Formulario para modificar los datos personales permitidos.

**3. Cambiar contraseña**

Formulario para actualizar la contraseña mediante validación de la contraseña actual.

#### Resultado esperado

Al finalizar este módulo, cualquier usuario autenticado podrá acceder a su perfil desde el icono de cuenta ubicado en el `header`, consultar sus datos personales, actualizar su información y cambiar su contraseña de forma segura, sin alterar sus permisos o rol dentro del sistema.

---

## 10. Instalación y configuración

### 10.1. Requisitos previos

Para trabajar con el proyecto se necesita:

- Python compatible con las dependencias del repositorio.
- MariaDB.
- Git.
- Un editor de código.
- Acceso a una terminal.
- Los scripts SQL de inicialización.
- Las dependencias declaradas en `requirements.txt`.

Se recomienda utilizar Ubuntu Linux para reproducir el entorno original de desarrollo.

### 10.2. Clonar el repositorio

```bash
git clone https://github.com/Juanchi-Reyes/Agencia-inmobiliaria.git
```

Ingresar al directorio:

```bash
cd Agencia-inmobiliaria
```

### 10.3. Crear el entorno virtual

```bash
python3 -m venv .venv
```

Activarlo:

```bash
source .venv/bin/activate
```

El indicador `(.venv)` debería aparecer en la terminal.

### 10.4. Instalar dependencias

```bash
python -m pip install --upgrade pip
```

```bash
python -m pip install -r requirements.txt
```

### 10.5. Iniciar MariaDB

```bash
sudo systemctl start mariadb
```

Verificar:

```bash
sudo systemctl status mariadb --no-pager
```

El servicio debe aparecer como:

```text
active (running)
```

### 10.6. Crear la base de datos

Ingresar a MariaDB:

```bash
sudo mariadb
```

Crear la base de datos:

```sql
CREATE DATABASE IF NOT EXISTS inmobiliaria
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Crear un usuario de desarrollo si todavía no existe:

```sql
CREATE USER 'inmobiliaria_user'@'localhost'
IDENTIFIED BY 'CONTRASENA_LOCAL_SEGURA';
```

Asignar privilegios:

```sql
GRANT ALL PRIVILEGES
ON inmobiliaria.*
TO 'inmobiliaria_user'@'localhost';
```

```sql
FLUSH PRIVILEGES;
```

La contraseña anterior es un marcador de ejemplo. Debe reemplazarse por una contraseña propia.

### 10.7. Importar el esquema SQL

Se deben utilizar los archivos SQL incluidos en el proyecto para crear las tablas inmobiliarias.

Ejemplo:

```bash
mariadb -u inmobiliaria_user -p inmobiliaria < ruta/al/schema.sql
```

Si existe un archivo de datos de prueba:

```bash
mariadb -u inmobiliaria_user -p inmobiliaria < ruta/al/datos_prueba.sql
```

**Importante:** las rutas son ilustrativas. Deben reemplazarse por las ubicaciones reales de los scripts dentro del repositorio.

Antes de importar, verificar si el esquema contiene instrucciones `CREATE DATABASE`, `USE` o restricciones que requieran una versión específica de MariaDB.

### 10.8. Configurar variables de entorno

Crear un archivo `.env` local según la configuración requerida por `config/settings.py`.

Ejemplo orientativo:

```dotenv
DB_NAME=inmobiliaria
DB_USER=inmobiliaria_user
DB_PASSWORD=CONTRASENA_LOCAL_SEGURA
DB_HOST=127.0.0.1
DB_PORT=3306
```

Los nombres de variables deben coincidir con los utilizados realmente por `settings.py`.

No publicar contraseñas reales ni claves privadas en GitHub.

### 10.9. Aplicar migraciones

Ejecutar:

```bash
python manage.py migrate
```

Este comando aplica las migraciones administradas por Django.

Las tablas inmobiliarias definidas con `managed = False` deben existir previamente en MariaDB.

### 10.10. Configurar roles

Ejecutar:

```bash
python manage.py crear_roles
```

Resultado esperado:

```text
Roles y permisos configurados correctamente.
```

Este comando crea o actualiza los grupos:

- Administrador.
- Vendedor.
- Cliente.

**Nota:** actualmente el comando configura permisos de usuarios e inmuebles. Deberá ampliarse para cubrir correctamente los permisos de clientes, propietarios y visitas.

### 10.11. Configuración posterior a las migraciones

Si el repositorio contiene un script o procedimiento `post_migracion`, se deberá ejecutar siguiendo su documentación específica.

Su objetivo es completar la configuración de relaciones, datos iniciales u otros elementos necesarios después de aplicar las migraciones.

No se debe ejecutar un procedimiento de inicialización sin verificar previamente su contenido.

### 10.12. Crear un superusuario

```bash
python manage.py createsuperuser
```

Completar los datos solicitados.

Esta cuenta permite acceder a la administración interna de Django.

No debe confundirse automáticamente con un usuario del grupo comercial Administrador.

---

## 11. Ejecución del sistema

### 11.1. Activar el entorno

```bash
source .venv/bin/activate
```

### 11.2. Verificar la configuración

```bash
python manage.py check
```

Resultado esperado:

```text
System check identified no issues (0 silenced).
```

### 11.3. Iniciar el servidor

```bash
python manage.py runserver
```

### 11.4. Acceder a la aplicación

Abrir:

```text
http://127.0.0.1:8000/
```

### Rutas principales

| Funcionalidad | Ruta |
|---|---|
| Inicio | `/` |
| Catálogo de inmuebles | `/inmuebles/` |
| Gestión de inmuebles | `/inmuebles/gestion/` |
| Registro | `/cuentas/registro/` |
| Inicio de sesión | `/cuentas/login/` |
| Panel principal | `/cuentas/panel/` |
| Panel administrador | `/cuentas/panel/administrador/` |
| Panel vendedor | `/cuentas/panel/vendedor/` |
| Panel cliente | `/cuentas/panel/cliente/` |
| Gestión de usuarios | `/cuentas/usuarios/` |
| Recuperación de contraseña | `/cuentas/recuperar/` |
| Gestión de propietarios | `/inmuebles/gestion/propietarios/` |
| Gestión de visitas | `/inmuebles/gestion/visitas/` |

Algunas rutas requieren autenticación y permisos específicos.

---

## 12. Pruebas y validaciones

Antes de considerar un módulo terminado, deben realizarse pruebas funcionales.

### 12.1. Autenticación

- [ ] Registro de usuario válido.
- [ ] Inicio de sesión correcto.
- [ ] Rechazo de credenciales incorrectas.
- [ ] Cierre de sesión.
- [ ] Redirección por rol.
- [ ] Restricción de páginas protegidas.
- [ ] Recuperación de contraseña.
- [ ] Rechazo de códigos expirados.

### 12.2. Usuarios y clientes

- [ ] Creación de usuario Administrador.
- [ ] Creación de usuario Vendedor.
- [ ] Creación de usuario Cliente.
- [ ] Captura correcta del teléfono.
- [ ] Asociación Usuario-Cliente.
- [ ] Edición de usuarios.
- [ ] Activación y desactivación.
- [ ] Restricción de operaciones según permisos.

### 12.3. Inmuebles

- [ ] Registro de Piso.
- [ ] Registro de Casa.
- [ ] Registro de Villa.
- [ ] Registro de Local.
- [ ] Edición de inmuebles.
- [ ] Validación de campos obligatorios.
- [ ] Asociación de propietarios.
- [ ] Asociación de oficinas.
- [ ] Asociación de zonas.
- [ ] Asociación de características.
- [ ] Gestión de ofertas.
- [ ] Restricción de eliminación para vendedores.

### 12.4. Visitas

- [ ] Registro de visita.
- [ ] Consulta de visitas.
- [ ] Edición de visita.
- [ ] Eliminación autorizada.
- [ ] Asociación con clientes.
- [ ] Asociación con inmuebles.
- [ ] Validación de fechas.
- [ ] Solicitud desde el portal del cliente.
- [ ] Restricción de acceso a visitas ajenas.

### 12.5. Interfaz

- [ ] Diseño responsivo.
- [ ] Navegación por rol.
- [ ] Estandarización de botones.
- [ ] Validación visual de formularios.
- [ ] Mensajes de éxito y error.
- [ ] Visualización de imágenes.
- [ ] Compatibilidad con navegadores modernos.

Las casillas anteriores representan una lista de verificación. No deben marcarse como completadas sin ejecutar las pruebas correspondientes.

---

## 13. Reglas de desarrollo

Para mantener la organización y consistencia del proyecto, se establecen las siguientes convenciones.

### 13.1. Separación de responsabilidades

- Los modelos representan entidades.
- Los formularios validan entradas.
- Las vistas procesan solicitudes.
- Los servicios implementan operaciones de negocio.
- Las plantillas presentan información.
- Los archivos JavaScript gestionan interactividad.
- Los archivos CSS gestionan estilos.

### 13.2. Estilos

El proyecto mantendrá un único archivo CSS externo principal.

No se utilizarán:

```html
<style>
```

ni estilos en línea mediante el atributo `style`.

### 13.3. Iconografía

Se utilizarán preferentemente los iconos de Google Fonts Material Symbols.

### 13.4. Seguridad

- Validar datos en el backend.
- Utilizar protección CSRF.
- Comprobar autenticación.
- Verificar permisos por operación.
- No confiar exclusivamente en restricciones visuales.
- Almacenar contraseñas mediante hash.
- Evitar publicar credenciales.
- No habilitar `DEBUG=True` en producción.
- Restringir la recuperación académica de contraseñas al entorno local.

### 13.5. Base de datos

- Mantener integridad referencial.
- Evitar duplicación de información.
- Utilizar transacciones cuando corresponda.
- No modificar tablas sin actualizar el esquema SQL.
- Documentar cambios estructurales.
- Crear respaldos antes de cambios importantes.

### 13.6. Git y GitHub

Se recomienda utilizar commits descriptivos.

Ejemplos:

```bash
git commit -m "feat: agregar gestion de visitas"
```

```bash
git commit -m "fix: corregir permisos de vendedor"
```

```bash
git commit -m "refactor: estandarizar botones"
```

```bash
git commit -m "docs: actualizar README"
```

Antes de subir cambios:

```bash
git status
```

```bash
git add .
```

```bash
git commit -m "descripcion del cambio"
```

```bash
git push
```

Cada integrante debe revisar los archivos modificados antes de realizar un commit.

---

## 14. Plan de trabajo

Se propone el siguiente orden de implementación para completar el sistema.

### Etapa 1 — Correcciones fundamentales

**Prioridad: Alta**

- [ ] Corregir el registro del teléfono de clientes.
- [ ] Corregir permisos del vendedor.
- [ ] Habilitar gestión de inmuebles para vendedores.
- [ ] Habilitar gestión de propietarios para vendedores.
- [ ] Habilitar gestión de clientes para vendedores.

**Resultado esperado:** funcionamiento correcto de los procesos administrativos y comerciales existentes.

### Etapa 2 — Gestión de visitas

**Prioridad: Alta**

- [ ] Completar CRUD de visitas.
- [ ] Configurar permisos del vendedor.
- [ ] Validar fechas y relaciones.
- [ ] Integrar solicitudes desde el portal del cliente.

**Resultado esperado:** administración completa de visitas y solicitudes.

### Etapa 3 — Portal del cliente

**Prioridad: Alta**

- [ ] Ampliar panel.
- [ ] Crear formulario de solicitud.
- [ ] Mostrar visitas propias.
- [ ] Incorporar estados.
- [ ] Validar acceso a información personal.

**Resultado esperado:** portal funcional para los clientes registrados.

### Etapa 4 — Catálogo e imágenes

**Prioridad: Alta**

- [ ] Implementar carga de imágenes.
- [ ] Guardar rutas en MariaDB.
- [ ] Mostrar galerías.
- [ ] Implementar búsqueda avanzada.
- [ ] Incorporar filtros combinados.

**Resultado esperado:** catálogo inmobiliario más completo.

### Etapa 5 — Administración complementaria

**Prioridad: Media**

- [ ] CRUD de oficinas.
- [ ] CRUD de zonas.
- [ ] Validaciones de integridad.
- [ ] Integración con formularios de inmuebles.

**Resultado esperado:** administración de catálogos y entidades auxiliares.

### Etapa 6 — Reportes e interfaz

**Prioridad: Media**

- [ ] Crear fichas estadísticas.
- [ ] Incorporar reportes.
- [ ] Estandarizar botones.
- [ ] Mejorar mensajes.
- [ ] Revisar diseño responsivo.

**Resultado esperado:** sistema visualmente consistente y con herramientas de consulta administrativa.

### Etapa 7 — Pruebas finales

- [ ] Validar todos los módulos.
- [ ] Comprobar permisos por rol.
- [ ] Revisar integridad de datos.
- [ ] Ejecutar pruebas de formularios.
- [ ] Probar el sistema en otro computador.
- [ ] Verificar instalación desde cero.
- [ ] Actualizar documentación.
- [ ] Preparar demostración académica.

### Etapa 8 — Perfil personal y gestión de cuenta

**Prioridad: Alta**

- [ ] Incorporar el icono de cuenta en el header.
- [ ] Crear el menú desplegable de cuenta.
- [ ] Implementar la vista "Mi cuenta".
- [ ] Mostrar la información del usuario autenticado.
- [ ] Crear el formulario de edición de perfil.
- [ ] Permitir actualizar nombre, correo y teléfono.
- [ ] Sincronizar la información entre Usuario y Cliente.
- [ ] Implementar el cambio de contraseña.
- [ ] Validar los permisos y la seguridad.
- [ ] Comprobar el funcionamiento para los tres roles.

**Resultado esperado:** todos los usuarios podrán consultar y actualizar su información personal desde una sección centralizada de cuenta.
---

## 15. Equipo de desarrollo

Proyecto desarrollado por estudiantes de la **Universidad Distrital Francisco José de Caldas — Facultad Tecnológica**, del programa **Tecnología en Sistematización de Datos**.

| Integrante | Código estudiantil |
|---|---|
| Juan Nicolas Reyes | 20242578031 |
| Sthepanny Nayleth Tonneti | 20241578047 |
| Andres Leonardo Fonseca | 20242578009 |
| Carlos Mauricio Pinilla | 20212578154 |
| Evelyn Tatiana Valencia | 20241578219 |

**Asignatura:** Aplicaciones en Internet  
**Institución:** Universidad Distrital Francisco José de Caldas  
**Facultad:** Facultad Tecnológica  
**Programa:** Tecnología en Sistematización de Datos  
**Año:** 2026

---

## 16. Estado general y alcance

**Estado actual: En desarrollo**

El proyecto dispone de una base funcional que integra:

- Autenticación y roles.
- Gestión de usuarios.
- Paneles diferenciados.
- Catálogo de inmuebles.
- Gestión administrativa de propiedades.
- Gestión de propietarios.
- Ofertas comerciales.
- Características y estancias.
- Estructura para gestión de visitas.
- Recuperación académica de contraseña.

Todavía deben completarse y corregirse los módulos indicados en la hoja de ruta, especialmente los permisos del vendedor, el registro de clientes, las visitas, el portal del cliente, las imágenes y los reportes.

### Criterios para considerar el proyecto terminado

El sistema se considerará funcionalmente completo cuando:

1. Los tres roles puedan acceder únicamente a las operaciones autorizadas.
2. Todos los módulos CRUD definidos funcionen correctamente.
3. Los clientes puedan consultar propiedades y solicitar visitas.
4. Los vendedores puedan gestionar inmuebles, propietarios, clientes y visitas dentro de sus permisos.
5. El administrador pueda gestionar los módulos correspondientes.
6. Los inmuebles puedan tener imágenes asociadas.
7. La búsqueda avanzada funcione con filtros combinados.
8. Los reportes presenten información correcta.
9. La interfaz mantenga consistencia visual.
10. La instalación y ejecución puedan reproducirse en otro computador siguiendo la documentación.
11. Mi cuenta — Perfil de usuario.

### Proyección

El sistema podrá ampliarse posteriormente con funcionalidades como:

- Notificaciones automáticas.
- Historial de actividad.
- Gestión documental.
- Exportación de reportes.
- Paneles analíticos avanzados.
- Despliegue en servidores de producción.
- Recuperación de contraseñas mediante correo verificado.

Estas características no forman parte del alcance obligatorio actual.

---

## 📌 Información del repositorio

**Nombre:** Agencia-inmobiliaria  
**Tipo:** Proyecto académico  
**Arquitectura:** Django MVT  
**Backend:** Python y Django  
**Frontend:** HTML, CSS y JavaScript  
**Base de datos:** MariaDB  
**Control de versiones:** Git y GitHub  
**Estado:** En desarrollo

**Repositorio oficial:**

https://github.com/Juanchi-Reyes/Agencia-inmobiliaria

---

**Universidad Distrital Francisco José de Caldas**  
**Facultad Tecnológica — Tecnología en Sistematización de Datos**  
**Proyecto académico de Aplicaciones en Internet — 2026**
