-- Table: raw.prior_web_content

-- DROP TABLE IF EXISTS "raw".prior_web_content;

CREATE TABLE IF NOT EXISTS "raw".prior_web_content
(
    record_id integer NOT NULL DEFAULT nextval('raw.prior_web_content_record_id_seq'::regclass),
    content character varying COLLATE pg_catalog."default",
    insert_timestamp timestamp without time zone,
    CONSTRAINT prior_web_content_pkey PRIMARY KEY (record_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "raw".prior_web_content
    OWNER to postgres;