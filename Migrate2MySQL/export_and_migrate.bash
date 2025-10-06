#!/usr/bin/bash


# This script migrates database tables used in Currency Rating Analysis  project from Postgresql database to MySQL
# It is assumed that prior database already created on MySQL side.

# Before export and load:
# 
# mysql is configured with --secure-file-priv=/var/lib/mysql-files/
# This folder is owned by mysql user id and has rwx permissions only for owner
# Added rwx permission to gorup and added leonid to mysql group.
# In order to keep this change permanent (not affected by package updates etc. ) i did following:
# sudo systemctl edit mysql
#
# added two lines:
#[Service]
#ExecStartPre=/bin/chmod 770 /var/lib/mysql-files
#
#sudo systemctl daemon-reexec
#sudo systemctl restart mysql

# Placed csv data files to /var/lib/mysql-files/

# Exporting data from Postgresql to csv viles

# By  sed 's/+03"/"/g' on output pipe we remove timezone form timestamps, because MySQL does not support timestamp with timezone.
# Exporting web content table we use back quote '\`' to avoid confusion with multiple double quotes present in html content.

psql -U postgres -c "COPY prior.currency_rate_history TO STDOUT WITH (FORMAT CSV, NULL 'NULL', FORCE_QUOTE *)" currency_rates_prod | sed 's/+03"/"/g' > /var/lib/mysql-files/currency_rates_history_prod.csv
psql -U postgres -c "COPY prior.currency_rate_list    TO STDOUT WITH (FORMAT CSV, NULL 'NULL', FORCE_QUOTE *)" currency_rates_prod | sed 's/+03"/"/g' > /var/lib/mysql-files/currency_rate_list_prod.csv
psql -U postgres -c "COPY raw.prior_web_content       TO STDOUT WITH (FORMAT CSV, NULL 'NULL', QUOTE '\`', FORCE_QUOTE *)" currency_rates_prod | sed 's/+03"/"/g' > /var/lib/mysql-files/prior_web_content_prod.csv

# Running SQL script to set up tables on MySQL side and load them with data.

mysql -u leonid < /home/leonid/Projects/Private/CurrencyRatingAnalysis/Migrate2MySQL/migrate_all.sql

# Clean up csv files after all is done
cd /var/lib/mysql-files/
rm currency_rates_history_prod.csv currency_rate_list_prod.csv prior_web_content_prod.csv
