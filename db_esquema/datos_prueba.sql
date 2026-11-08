
-- ============================================================
-- PROYECTO: SISTEMA DE GESTION INMOBILIARIA
-- INSERCION DE DATOS DE PRUEBA
-- ============================================================

USE inmobiliaria;

START TRANSACTION;


-- ============================================================
-- 1. OFICINAS
-- Datos ficticios para pruebas.
-- ============================================================

INSERT INTO oficina (
    id_oficina,
    nombre,
    direccion,
    telefono
)
VALUES
(1, 'Oficina Centro', 'Direccion de prueba 1', '600111222'),
(2, 'Oficina Norte', 'Direccion de prueba 2', '600333444');


-- ============================================================
-- 2. ZONAS
-- ============================================================

INSERT INTO zona (
    id_zona,
    nombre,
    descripcion
)
VALUES
(1, 'Capuchinos', 'Zona de Capuchinos'),
(2, 'Avenida Valencia', 'Zona de Avenida Valencia'),
(3, 'El Pantano', 'Zona de El Pantano');


-- ============================================================
-- 3. PROPIETARIOS
-- ============================================================

INSERT INTO propietario (
    id_propietario,
    nombre,
    telefono
)
VALUES
(1, 'Luis Herranz', '964223344'),
(2, 'Carmela Aparicio', '964221144'),
(3, 'Gemma Lopez', '963456789');


-- ============================================================
-- 4. CLIENTES
-- ============================================================

INSERT INTO cliente (
    id_cliente,
    nombre,
    telefono
)
VALUES
(1, 'Marcela Torres', NULL),
(2, 'Carlos Jara', NULL),
(3, 'Antonio Ruiz', NULL),
(4, 'Felipe Ulloa', NULL),
(5, 'Carmen Fez', NULL);


-- ============================================================
-- 5. INMUEBLES
-- Se insertan los cuatro inmuebles originales.
-- ============================================================

INSERT INTO inmueble (
    id_inmueble,
    referencia,
    tipo,
    direccion,
    superficie_m2,
    descripcion,
    id_propietario,
    id_oficina_gestion,
    id_oficina_llaves,
    id_zona
)
VALUES

-- INMUEBLE 1234: PISO DE OCASION
(
    1,
    '1234',
    'PISO',
    'C/Lerida 24, zona Capuchinos',
    90,
    '3 habitaciones, 1 bano, cocina, 5 armarios empotrados, puerta blindada, parquet, totalmente reformado y todo exterior.',
    1,
    1,
    NULL,
    1
),

-- INMUEBLE 9876: VILLA
(
    2,
    '9876',
    'VILLA',
    'Urb. Las Palmas 8A, Benicasim',
    140,
    '2 habitaciones, 3 banos, 5 armarios empotrados, terraza de 40 m2, gas ciudad y calefaccion central.',
    2,
    1,
    NULL,
    NULL
),

-- INMUEBLE 5678: LOCAL
(
    3,
    '5678',
    'LOCAL',
    'C/Ricardo Catala 12, zona Av. Valencia',
    40,
    'Local diafano, con altillo de 10 m2, vado, agua, luz y chaflan.',
    1,
    2,
    NULL,
    2
),

-- INMUEBLE 3456: CASA
(
    4,
    '3456',
    'CASA',
    'Ctra. Alcora 43, zona El Pantano',
    104,
    'Casa de 2 alturas, 3 habitaciones, cocina, bano, salon, solarium y plaza de garaje.',
    3,
    2,
    NULL,
    3
);


-- ============================================================
-- 6. OFERTAS
-- ============================================================

INSERT INTO oferta (
    id_oferta,
    id_inmueble,
    modalidad,
    precio,
    a_convenir
)
VALUES

-- Piso: venta
(1, 1, 'VENTA', 14000000, FALSE),

-- Villa: venta a convenir
(2, 2, 'VENTA', NULL, TRUE),

-- Local: venta y alquiler
(3, 3, 'VENTA', 6000000, FALSE),
(4, 3, 'ALQUILER', 50000, FALSE),

-- Casa: venta
(5, 4, 'VENTA', 8000000, FALSE);


-- ============================================================
-- 7. VIVIENDAS
-- ============================================================

INSERT INTO vivienda (
    id_inmueble,
    tipo
)
VALUES
(1, 'PISO'),
(2, 'VILLA'),
(4, 'CASA');


-- ============================================================
-- 8. PISOS
-- ============================================================

INSERT INTO piso (
    id_inmueble,
    tipo,
    estado
)
VALUES
(1, 'PISO', 'OCASION');


-- ============================================================
-- 9. CASAS
-- ============================================================

INSERT INTO casa (
    id_inmueble,
    tipo
)
VALUES
(4, 'CASA');


-- ============================================================
-- 10. VILLAS
-- ============================================================

INSERT INTO villa (
    id_inmueble,
    tipo,
    superficie_parcela_m2,
    urbanizacion
)
VALUES
(2, 'VILLA', 820, 'Las Palmas');


-- ============================================================
-- 11. LOCALES
-- ============================================================

INSERT INTO `local` (
    id_inmueble,
    tipo,
    numero_puertas,
    es_diafano,
    esta_acondicionado
)
VALUES
(3, 'LOCAL', NULL, TRUE, NULL);


-- ============================================================
-- 12. ESTANCIAS
-- Catalogo de tipos de estancias.
-- ============================================================

INSERT INTO estancia (
    id_estancia,
    nombre
)
VALUES
(1, 'Habitaciones'),
(2, 'Banos'),
(3, 'Aseos'),
(4, 'Cocinas'),
(5, 'Salones'),
(6, 'Terrazas'),
(7, 'Plazas de garaje');


-- ============================================================
-- 13. VIVIENDA_ESTANCIA
-- Cantidad de cada estancia por vivienda.
-- ============================================================

INSERT INTO vivienda_estancia (
    id_inmueble,
    id_estancia,
    cantidad
)
VALUES

-- Piso 1234
(1, 1, 3),
(1, 2, 1),
(1, 4, 1),

-- Villa 9876
(2, 1, 2),
(2, 2, 3),
(2, 6, 1),

-- Casa 3456
(4, 1, 3),
(4, 2, 1),
(4, 4, 1),
(4, 5, 1),
(4, 7, 1);


-- ============================================================
-- 14. CARACTERISTICAS
-- Catalogo de caracteristicas.
-- ============================================================

INSERT INTO caracteristica (
    id_caracteristica,
    nombre
)
VALUES
(1, 'Armarios empotrados'),
(2, 'Puerta blindada'),
(3, 'Parquet'),
(4, 'Totalmente reformado'),
(5, 'Todo exterior'),
(6, 'Terraza'),
(7, 'Gas ciudad'),
(8, 'Calefaccion central'),
(9, 'Altillo'),
(10, 'Vado'),
(11, 'Agua'),
(12, 'Luz'),
(13, 'Chaflan'),
(14, 'Dos alturas'),
(15, 'Solarium');


-- ============================================================
-- 15. INMUEBLE_CARACTERISTICA
-- Caracteristicas asociadas a cada inmueble.
-- ============================================================

INSERT INTO inmueble_caracteristica (
    id_inmueble,
    id_caracteristica,
    detalle
)
VALUES

-- PISO 1234
(1, 1, '5 armarios empotrados'),
(1, 2, NULL),
(1, 3, NULL),
(1, 4, NULL),
(1, 5, NULL),

-- VILLA 9876
(2, 1, '5 armarios empotrados'),
(2, 6, 'Terraza de 40 m2'),
(2, 7, NULL),
(2, 8, NULL),

-- LOCAL 5678
(3, 9, 'Altillo de 10 m2'),
(3, 10, NULL),
(3, 11, NULL),
(3, 12, NULL),
(3, 13, NULL),

-- CASA 3456
(4, 14, 'Casa de 2 alturas'),
(4, 15, NULL);


-- ============================================================
-- 16. VISITAS
-- Fechas y horas de las fichas originales.
-- ============================================================

INSERT INTO visita (
    id_visita,
    id_inmueble,
    id_cliente,
    fecha_hora,
    comentario
)
VALUES

-- VISITAS DEL PISO 1234
(
    1,
    1,
    1,
    '2001-02-12 19:00:00',
    'Baño pequeño; piso alto'
),

(
    2,
    1,
    2,
    '2001-03-21 12:00:00',
    NULL
),

-- VISITA DE LA VILLA 9876
(
    3,
    2,
    3,
    '2001-05-22 09:30:00',
    'Interesado'
),

-- VISITAS DE LA CASA 3456
(
    4,
    4,
    4,
    '2001-01-13 17:00:00',
    'No es lo que busca'
),

(
    5,
    4,
    5,
    '2001-05-05 17:30:00',
    'Le gusta'
),

(
    6,
    4,
    5,
    '2001-05-23 19:45:00',
    'Buscara financiacion'
);


-- ============================================================
-- FINALIZAR TRANSACCION
-- ============================================================

COMMIT;


-- ============================================================
-- COMPROBACION GENERAL
-- ============================================================

SELECT
    referencia,
    tipo,
    direccion,
    superficie_m2
FROM inmueble
ORDER BY referencia;

-- ============================================================
-- FIN DE LA INSERCION DE DATOS
-- ============================================================
