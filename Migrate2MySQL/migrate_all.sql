
-- Before export and load:

-- mysql is configured with --secure-file-priv=/var/lib/mysql-files/
-- This folder is owned by mysql user id and has rwx permissions only for owner
-- Added rwx permission to gorup and added leonid to mysql group.
-- Placed csv data files to /var/lib/mysql-files/



-- Create MySQL tables

DROP TABLE IF EXISTS prior.currency_rate_list;
CREATE TABLE prior.currency_rate_list (
    currency_rate_list_id int,
    currency_buy_rate numeric(10,4) NOT NULL,
    buy_rate_coefficient smallint DEFAULT 1 NOT NULL,
    currency_sell_rate numeric(10,4) NOT NULL,
    sell_rate_coefficient smallint DEFAULT 1 NOT NULL,
    low_limit_amount numeric(10,0) DEFAULT 0 NOT NULL,
    high_limit_amount numeric(10,4) DEFAULT NULL,
    insert_timestamp timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
,   PRIMARY KEY (currency_rate_list_id,low_limit_amount)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS prior.currency_rate_history;
CREATE TABLE prior.currency_rate_history (
    client_currency_code varchar(5) NOT NULL,
    bank_currency_code varchar(5) NOT NULL,
    operation_place_code varchar(10) NOT NULL,
    operation_code varchar(10) NOT NULL,
    currency_rate_list_id int, 
    valid_from_datetime timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    raw_data_timestamp timestamp,
    insert_timestamp timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL
,   PRIMARY KEY (client_currency_code,bank_currency_code,operation_place_code,operation_code,valid_from_datetime)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS prior.prior_web_content;
CREATE TABLE prior.prior_web_content (
    record_id int,
    content mediumtext,
    insert_timestamp timestamp
, PRIMARY KEY(record_id)
) ENGINE=InnoDB;


-- Load exported data from csv  files to created tables


LOAD DATA INFILE '/var/lib/mysql-files/currency_rates_history_prod.csv'
INTO TABLE prior.currency_rate_history
FIELDS TERMINATED BY ','
       ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/var/lib/mysql-files/currency_rate_list_prod.csv'
INTO TABLE prior.currency_rate_list
FIELDS TERMINATED BY ','
       ENCLOSED BY '"'
LINES TERMINATED BY '\n';

LOAD DATA INFILE '/var/lib/mysql-files/prior_web_content_prod.csv'
INTO TABLE prior.prior_web_content
FIELDS TERMINATED BY ','
       ENCLOSED BY '`'
LINES TERMINATED BY '\n';

-- Set up constraints on filled tables

CREATE UNIQUE INDEX idx_unique_currency_rate_history_currency_rate_list_id ON prior.currency_rate_history (currency_rate_list_id);

select max(currency_rate_list_id) into @max_currency_rate_list_id from prior.currency_rate_history;

SET @sql_query = CONCAT('ALTER TABLE prior.currency_rate_history AUTO_INCREMENT = ', @max_currency_rate_list_id+1);
PREPARE stmt FROM @sql_query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

ALTER TABLE prior.currency_rate_history MODIFY COLUMN currency_rate_list_id INT AUTO_INCREMENT;

-- 

select max(record_id) into @max_record_id  from prior.prior_web_content;

SET @sql_query = CONCAT('ALTER TABLE prior.prior_web_content AUTO_INCREMENT = ', @max_record_id+1);
PREPARE stmt FROM @sql_query;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

ALTER TABLE  prior.prior_web_content  MODIFY COLUMN record_id INT AUTO_INCREMENT;

--

ALTER TABLE prior.currency_rate_list ADD CONSTRAINT currency_rate_fk FOREIGN KEY (currency_rate_list_id)
REFERENCES prior.currency_rate_history (currency_rate_list_id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
