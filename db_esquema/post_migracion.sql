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
