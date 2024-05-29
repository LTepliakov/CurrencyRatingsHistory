#!/bin/bash

# Cleans raw data records eleder then 10 days  from raw.prior_web_content staging table 

script_name=$(basename "$0")
today=$(date +%Y-%m-%d+%T)

# Cleaning old raws from the staging table

echo "$script_name : $today :  main cluster. Cleaning old raw records"
psql -h localhost -p 5432 -d currency_rates_prod -U postgres -c "delete from raw.prior_web_content WHERE insert_timestamp < NOW() - INTERVAL '10 days';"

# Clenaing old compressed files from RawFilesBackup/ folder

find  /opt/CurrencyRatingAnalysis/RawFilesBackup/ -name "prior_page*.html.gz" -type f -mtime +30 -exec rm {} \;
