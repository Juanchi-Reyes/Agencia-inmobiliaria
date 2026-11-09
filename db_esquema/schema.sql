
-- ============================================================
-- PROYECTO: SISTEMA DE GESTION INMOBILIARIA
-- MOTOR: MariaDB 11.8
-- BASE DE DATOS: inmobiliaria
-- SIN TRIGGERS
-- ============================================================

CREATE DATABASE IF NOT EXISTS inmobiliaria
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE inmobiliaria;


-- ============================================================
-- 1. TABLA: OFICINA
-- Almacena las oficinas de la inmobiliaria.
-- ============================================================

CREATE TABLE oficina (
    id_oficina INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(20)
) ENGINE=InnoDB;


-- ============================================================
-- 2. TABLA: ZONA
-- Almacena las zonas de la ciudad.
-- ============================================================

CREATE TABLE zona (
    id_zona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
) ENGINE=InnoDB;


-- ============================================================
-- 3. TABLA: PROPIETARIO
-- Almacena los propietarios de los inmuebles.
-- ============================================================

CREATE TABLE propietario (
    id_propietario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    telefono VARCHAR(25) NOT NULL
) ENGINE=InnoDB;


-- ============================================================
-- 4. TABLA: CLIENTE
-- Almacena los clientes de la inmobiliaria.
-- ============================================================

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    telefono VARCHAR(25) NULL
) ENGINE=InnoDB;


-- ============================================================
-- 5. TABLA: INMUEBLE
-- Almacena la informacion general de cada inmueble.
-- ============================================================

CREATE TABLE inmueble (
    id_inmueble INT AUTO_INCREMENT PRIMARY KEY,

    referencia VARCHAR(20) NOT NULL UNIQUE,

    tipo ENUM(
        'PISO',
        'CASA',
        'VILLA',
        'LOCAL'
    ) NOT NULL,

    direccion VARCHAR(255) NOT NULL,

    superficie_m2 DECIMAL(10,2) NOT NULL,

    descripcion TEXT NULL,

    id_propietario INT NOT NULL,

    id_oficina_gestion INT NOT NULL,

    id_oficina_llaves INT NULL,

    id_zona INT NULL,

    -- Clave candidata para relaciones de especializacion
    UNIQUE KEY uq_inmueble_tipo (
        id_inmueble,
        tipo
    ),

    CONSTRAINT fk_inmueble_propietario
        FOREIGN KEY (id_propietario)
        REFERENCES propietario(id_propietario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_inmueble_oficina_gestion
        FOREIGN KEY (id_oficina_gestion)
        REFERENCES oficina(id_oficina)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_inmueble_oficina_llaves
        FOREIGN KEY (id_oficina_llaves)
        REFERENCES oficina(id_oficina)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    -- RESTRICT permite conservar chk_zona_villa
    CONSTRAINT fk_inmueble_zona
        FOREIGN KEY (id_zona)
        REFERENCES zona(id_zona)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,

    CONSTRAINT chk_superficie_inmueble
        CHECK (superficie_m2 > 0),

    -- Una villa no puede tener una zona asignada
    CONSTRAINT chk_zona_villa
        CHECK (
            tipo <> 'VILLA'
            OR id_zona IS NULL
        )

) ENGINE=InnoDB;


-- ============================================================
-- 6. TABLA: OFERTA
-- Almacena las ofertas de venta y alquiler.
-- Un inmueble puede tener una o ambas modalidades.
-- ============================================================

CREATE TABLE oferta (
    id_oferta INT AUTO_INCREMENT PRIMARY KEY,

    id_inmueble INT NOT NULL,

    modalidad ENUM(
        'VENTA',
        'ALQUILER'
    ) NOT NULL,

    precio DECIMAL(15,2) NULL,

    a_convenir BOOLEAN NOT NULL DEFAULT FALSE,

    -- Impide repetir la misma modalidad para un inmueble
    UNIQUE KEY uq_inmueble_modalidad (
        id_inmueble,
        modalidad
    ),

    CONSTRAINT fk_oferta_inmueble
        FOREIGN KEY (id_inmueble)
        REFERENCES inmueble(id_inmueble)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_precio_oferta
        CHECK (
            precio IS NULL
            OR precio >= 0
        ),

    CONSTRAINT chk_oferta_convenir
        CHECK (
            a_convenir = FALSE
            OR (
                modalidad = 'VENTA'
                AND precio IS NULL
            )
        )

) ENGINE=InnoDB;


-- ============================================================
-- 7. TABLA: VIVIENDA
-- Especializacion de INMUEBLE para viviendas.
-- ============================================================

CREATE TABLE vivienda (
    id_inmueble INT PRIMARY KEY,

    -- Mismo ENUM que inmueble para compatibilidad
    -- con la clave foranea compuesta
    tipo ENUM(
        'PISO',
        'CASA',
        'VILLA',
        'LOCAL'
    ) NOT NULL,

    -- Una vivienda no puede ser un local
    CONSTRAINT chk_tipo_vivienda
        CHECK (
            tipo IN ('PISO', 'CASA', 'VILLA')
        ),

    UNIQUE KEY uq_vivienda_tipo (
        id_inmueble,
        tipo
    ),

    CONSTRAINT fk_vivienda_inmueble
        FOREIGN KEY (id_inmueble, tipo)
        REFERENCES inmueble(id_inmueble, tipo)
        ON DELETE CASCADE
        ON UPDATE RESTRICT

) ENGINE=InnoDB;


-- ============================================================
-- 8. TABLA: PISO
-- Especializacion de VIVIENDA.
-- ============================================================

CREATE TABLE piso (
    id_inmueble INT PRIMARY KEY,

    tipo ENUM(
        'PISO',
        'CASA',
        'VILLA',
        'LOCAL'
    ) NOT NULL DEFAULT 'PISO',

    CONSTRAINT chk_tipo_piso
        CHECK (tipo = 'PISO'),

    estado ENUM(
        'NUEVO',
        'OCASION'
    ) NOT NULL,

    CONSTRAINT fk_piso_vivienda
        FOREIGN KEY (id_inmueble, tipo)
        REFERENCES vivienda(id_inmueble, tipo)
        ON DELETE CASCADE
        ON UPDATE RESTRICT

) ENGINE=InnoDB;


-- ============================================================
-- 9. TABLA: CASA
-- Especializacion de VIVIENDA.
-- ============================================================

CREATE TABLE casa (
    id_inmueble INT PRIMARY KEY,

    tipo ENUM(
        'PISO',
        'CASA',
        'VILLA',
        'LOCAL'
    ) NOT NULL DEFAULT 'CASA',

    CONSTRAINT chk_tipo_casa
        CHECK (tipo = 'CASA'),

    CONSTRAINT fk_casa_vivienda
        FOREIGN KEY (id_inmueble, tipo)
        REFERENCES vivienda(id_inmueble, tipo)
        ON DELETE CASCADE
        ON UPDATE RESTRICT

) ENGINE=InnoDB;


-- ============================================================
-- 10. TABLA: VILLA
-- Especializacion de VIVIENDA.
-- ============================================================

CREATE TABLE villa (
    id_inmueble INT PRIMARY KEY,

    tipo ENUM(
        'PISO',
        'CASA',
        'VILLA',
        'LOCAL'
    ) NOT NULL DEFAULT 'VILLA',

    CONSTRAINT chk_tipo_villa
        CHECK (tipo = 'VILLA'),

    superficie_parcela_m2 DECIMAL(10,2) NOT NULL,

    urbanizacion VARCHAR(150) NOT NULL,

    CONSTRAINT fk_villa_vivienda
        FOREIGN KEY (id_inmueble, tipo)
        REFERENCES vivienda(id_inmueble, tipo)
        ON DELETE CASCADE
        ON UPDATE RESTRICT,

    CONSTRAINT chk_superficie_parcela
        CHECK (superficie_parcela_m2 > 0)

) ENGINE=InnoDB;


-- ============================================================
-- 11. TABLA: LOCAL
-- Especializacion de INMUEBLE.
-- ============================================================

CREATE TABLE `local` (
    id_inmueble INT PRIMARY KEY,

    tipo ENUM(
        'PISO',
        'CASA',
        'VILLA',
        'LOCAL'
    ) NOT NULL DEFAULT 'LOCAL',

    CONSTRAINT chk_tipo_local
        CHECK (tipo = 'LOCAL'),

    numero_puertas INT NULL,

    es_diafano BOOLEAN NULL,

    esta_acondicionado BOOLEAN NULL,

    CONSTRAINT fk_local_inmueble
        FOREIGN KEY (id_inmueble, tipo)
        REFERENCES inmueble(id_inmueble, tipo)
        ON DELETE CASCADE
        ON UPDATE RESTRICT,

    CONSTRAINT chk_numero_puertas
        CHECK (
            numero_puertas IS NULL
            OR numero_puertas >= 0
        )

) ENGINE=InnoDB;


-- ============================================================
-- 12. TABLA: ESTANCIA
-- Catalogo de tipos de estancias.
-- ============================================================

CREATE TABLE estancia (
    id_estancia INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(50) NOT NULL UNIQUE

) ENGINE=InnoDB;


-- ============================================================
-- 13. TABLA: VIVIENDA_ESTANCIA
-- Relacion N:M entre VIVIENDA y ESTANCIA.
-- ============================================================

CREATE TABLE vivienda_estancia (
    id_inmueble INT NOT NULL,

    id_estancia INT NOT NULL,

    cantidad INT NOT NULL,

    PRIMARY KEY (
        id_inmueble,
        id_estancia
    ),

    CONSTRAINT fk_ve_vivienda
        FOREIGN KEY (id_inmueble)
        REFERENCES vivienda(id_inmueble)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_ve_estancia
        FOREIGN KEY (id_estancia)
        REFERENCES estancia(id_estancia)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_cantidad_estancia
        CHECK (cantidad > 0)

) ENGINE=InnoDB;


-- ============================================================
-- 14. TABLA: CARACTERISTICA
-- Catalogo de caracteristicas de los inmuebles.
-- ============================================================

CREATE TABLE caracteristica (
    id_caracteristica INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL UNIQUE

) ENGINE=InnoDB;


-- ============================================================
-- 15. TABLA: INMUEBLE_CARACTERISTICA
-- Relacion N:M entre INMUEBLE y CARACTERISTICA.
-- ============================================================

CREATE TABLE inmueble_caracteristica (
    id_inmueble INT NOT NULL,

    id_caracteristica INT NOT NULL,

    detalle VARCHAR(255) NULL,

    PRIMARY KEY (
        id_inmueble,
        id_caracteristica
    ),

    CONSTRAINT fk_ic_inmueble
        FOREIGN KEY (id_inmueble)
        REFERENCES inmueble(id_inmueble)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_ic_caracteristica
        FOREIGN KEY (id_caracteristica)
        REFERENCES caracteristica(id_caracteristica)
        ON DELETE RESTRICT
        ON UPDATE CASCADE

) ENGINE=InnoDB;


-- ============================================================
-- 16. TABLA: VISITA
-- Relaciona CLIENTE con INMUEBLE.
-- Almacena fecha, hora y comentario.
-- ============================================================

CREATE TABLE visita (
    id_visita INT AUTO_INCREMENT PRIMARY KEY,

    id_inmueble INT NOT NULL,

    id_cliente INT NOT NULL,

    fecha_hora DATETIME NOT NULL,

    comentario TEXT NULL,

    CONSTRAINT fk_visita_inmueble
        FOREIGN KEY (id_inmueble)
        REFERENCES inmueble(id_inmueble)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_visita_cliente
        FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
        ON DELETE RESTRICT
        ON UPDATE CASCADE

) ENGINE=InnoDB;


-- ============================================================
-- FIN DEL ESQUEMA
-- ============================================================


--USE inmobiliaria;

ALTER TABLE cliente
ADD COLUMN usuario_id BIGINT(20) NULL,
ADD CONSTRAINT uq_cliente_usuario
    UNIQUE (usuario_id),
ADD CONSTRAINT fk_cliente_usuario
    FOREIGN KEY (usuario_id)
    REFERENCES cuentas_usuario(id)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT;

SHOW TABLES;
