-- =============================================================================
-- Mercado Pago: retención de horarios y confirmación idempotente de pagos.
-- Aplicar después de 07_catalogo_servicios.sql.
-- =============================================================================

BEGIN
    EXECUTE IMMEDIATE q'[
        CREATE TABLE mercadopago_intents (
            referencia_externa VARCHAR2(36) NOT NULL,
            id_preferencia VARCHAR2(100),
            id_pago_mp VARCHAR2(40),
            id_reserva NUMBER,
            fecha_evento DATE NOT NULL,
            hora_inicio VARCHAR2(5) NOT NULL,
            duracion_minutos NUMBER(3) NOT NULL,
            contrato_json CLOB NOT NULL,
            monto_total NUMBER(10,2) NOT NULL,
            monto_pago NUMBER(10,2) NOT NULL,
            estado VARCHAR2(20) NOT NULL,
            expira_en TIMESTAMP NOT NULL,
            init_point VARCHAR2(1000),
            fecha_creacion TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
            CONSTRAINT pk_mp_intents PRIMARY KEY (referencia_externa),
            CONSTRAINT uq_mp_preferencia UNIQUE (id_preferencia),
            CONSTRAINT uq_mp_pago UNIQUE (id_pago_mp),
            CONSTRAINT uq_mp_reserva UNIQUE (id_reserva),
            CONSTRAINT fk_mp_intent_reserva FOREIGN KEY (id_reserva)
                REFERENCES eventos_reservas(id_reserva),
            CONSTRAINT ck_mp_intent_estado CHECK (
                estado IN (
                    'CREANDO', 'PENDIENTE', 'APROBADO', 'RECHAZADO',
                    'ERROR', 'REQUIERE_REVISION'
                )
            )
        )
    ]';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -955 THEN RAISE; END IF;
END;
/

BEGIN
    FOR constraint_row IN (
        SELECT constraint_name
        FROM user_constraints
        WHERE table_name = 'EVENTOS_RESERVAS'
          AND constraint_type = 'C'
          AND UPPER(search_condition_vc) LIKE '%METODO_PAGO_PREFERIDO%'
          AND UPPER(search_condition_vc) LIKE '%IN (%'
    ) LOOP
        EXECUTE IMMEDIATE
            'ALTER TABLE eventos_reservas DROP CONSTRAINT "'
            || REPLACE(constraint_row.constraint_name, '"', '""')
            || '"';
    END LOOP;

    EXECUTE IMMEDIATE q'[
        ALTER TABLE eventos_reservas
        ADD CONSTRAINT ck_reserva_metodo_pago
        CHECK (metodo_pago_preferido IN (
            'TRANSFERENCIA', 'EFECTIVO', 'TARJETA_CREDITO',
            'MERCADOPAGO', 'PRUEBA', 'PENDIENTE'
        ))
    ]';
END;
/

BEGIN
    EXECUTE IMMEDIATE
        'CREATE INDEX ix_mp_intent_schedule '
        || 'ON mercadopago_intents (estado, expira_en, fecha_evento)';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -955 THEN RAISE; END IF;
END;
/
