-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 1.1.0-beta1
-- PostgreSQL version: 16.0
-- Project Site: pgmodeler.io
-- Model Author: ---
-- object: scott | type: ROLE --
-- DROP ROLE IF EXISTS scott;
CREATE ROLE scott WITH 
	SUPERUSER
	INHERIT
	LOGIN
	 PASSWORD '********';
-- ddl-end --


-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: currency_rates_dev | type: DATABASE --
-- DROP DATABASE IF EXISTS currency_rates_dev;
CREATE DATABASE currency_rates_dev
	ENCODING = 'UTF8'
	LC_COLLATE = 'en_US.UTF-8'
	LC_CTYPE = 'en_US.UTF-8'
	TABLESPACE = pg_default
	OWNER = postgres;
-- ddl-end --


-- object: raw | type: SCHEMA --
-- DROP SCHEMA IF EXISTS raw CASCADE;
CREATE SCHEMA raw;
-- ddl-end --
ALTER SCHEMA raw OWNER TO postgres;
-- ddl-end --

-- object: prior | type: SCHEMA --
-- DROP SCHEMA IF EXISTS prior CASCADE;
CREATE SCHEMA prior;
-- ddl-end --
ALTER SCHEMA prior OWNER TO postgres;
-- ddl-end --

SET search_path TO pg_catalog,public,raw,prior;
-- ddl-end --

-- object: raw.prior_web_content_record_id_seq | type: SEQUENCE --
-- DROP SEQUENCE IF EXISTS raw.prior_web_content_record_id_seq CASCADE;
CREATE SEQUENCE raw.prior_web_content_record_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;

-- ddl-end --
ALTER SEQUENCE raw.prior_web_content_record_id_seq OWNER TO postgres;
-- ddl-end --

-- object: raw.prior_web_content | type: TABLE --
-- DROP TABLE IF EXISTS raw.prior_web_content CASCADE;
CREATE TABLE raw.prior_web_content (
	record_id integer NOT NULL DEFAULT nextval('raw.prior_web_content_record_id_seq'::regclass),
	content character varying,
	insert_timestamp timestamp,
	CONSTRAINT prior_web_content_pkey PRIMARY KEY (record_id)
);
-- ddl-end --
ALTER TABLE raw.prior_web_content OWNER TO postgres;
-- ddl-end --

-- object: prior.currency_rate_history | type: TABLE --
-- DROP TABLE IF EXISTS prior.currency_rate_history CASCADE;
CREATE TABLE prior.currency_rate_history (
	client_currency_code character(5) NOT NULL,
	bank_currency_code character(5) NOT NULL,
	operation_place_code char(10) NOT NULL,
	operation_code char(10) NOT NULL,
	currency_buy_rate numeric(10,4) NOT NULL,
	buy_rate_coefficient smallint NOT NULL DEFAULT 1,
	currency_sell_rate numeric(10,4) NOT NULL,
	sell_rate_coefficient smallint NOT NULL DEFAULT 1,
	low_limit_amount numeric(10,4) DEFAULT null,
	high_limit_amount numeric(10,4) DEFAULT null,
	valid_from_datetime timestamptz NOT NULL DEFAULT current_date,
	insert_timestamp timestamptz NOT NULL DEFAULT current_date,
	CONSTRAINT currency_rate_history_pk PRIMARY KEY (client_currency_code,bank_currency_code,operation_place_code,operation_code,valid_from_datetime)
);
-- ddl-end --
ALTER TABLE prior.currency_rate_history OWNER TO postgres;
-- ddl-end --


