-- Table: prior.currency_rate_history

-- DROP TABLE IF EXISTS prior.currency_rate_history;

CREATE TABLE IF NOT EXISTS prior.currency_rate_history
(
    client_currency_code character(5) COLLATE pg_catalog."default" NOT NULL,
    bank_currency_code character(5) COLLATE pg_catalog."default" NOT NULL,
    operation_place_code character(10) COLLATE pg_catalog."default" NOT NULL,
    operation_code character(10) COLLATE pg_catalog."default" NOT NULL,
    currency_rate_list_id integer DEFAULT nextval('prior.currency_rate_list_seq'::regclass),
    valid_from_datetime timestamp with time zone NOT NULL DEFAULT CURRENT_DATE,
    raw_data_timestamp timestamp with time zone,
    insert_timestamp timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT currency_rate_history_pk PRIMARY KEY (client_currency_code, bank_currency_code, operation_place_code, operation_code, valid_from_datetime),
    CONSTRAINT currency_rate_list_id_unique UNIQUE (currency_rate_list_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS prior.currency_rate_history
    OWNER to postgres;

REVOKE ALL ON TABLE prior.currency_rate_history FROM grafana;

GRANT SELECT ON TABLE prior.currency_rate_history TO grafana;

GRANT ALL ON TABLE prior.currency_rate_history TO postgres;