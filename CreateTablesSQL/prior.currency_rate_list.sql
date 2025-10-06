-- Table: prior.currency_rate_list

-- DROP TABLE IF EXISTS prior.currency_rate_list;

CREATE TABLE IF NOT EXISTS prior.currency_rate_list
(
    currency_rate_list_id integer,
    currency_buy_rate numeric(10,4) NOT NULL,
    buy_rate_coefficient smallint NOT NULL DEFAULT 1,
    currency_sell_rate numeric(10,4) NOT NULL,
    sell_rate_coefficient smallint NOT NULL DEFAULT 1,
    low_limit_amount numeric(10,0) NOT NULL DEFAULT 0,
    high_limit_amount numeric(10,4) DEFAULT NULL::numeric,
    insert_timestamp timestamp with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT currency_rate_fk FOREIGN KEY (currency_rate_list_id)
        REFERENCES prior.currency_rate_history (currency_rate_list_id) MATCH FULL
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS prior.currency_rate_list
    OWNER to postgres;

REVOKE ALL ON TABLE prior.currency_rate_list FROM grafana;

GRANT SELECT ON TABLE prior.currency_rate_list TO grafana;

GRANT ALL ON TABLE prior.currency_rate_list TO postgres;