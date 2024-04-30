#!/bin/bash

# This script backups main cluster to  /opt/postgres_backup/main/base_%Y%m%d.tar.bz2 file
# and removes all backup files

#d=`date +"%Yw%Ud%u"`
d=`date +"%Y%m%d"`
fileName="/opt/postgres_backup/main/base_$d.tar.bz2"
echo $fileName 

#sudo -u postgres pg_basebackup -D - -Ft -X fetch | bzip2 > /opt/postgres_backup/main/backup.tar.bz2

sudo -u postgres pg_basebackup -D - -Ft -X fetch | bzip2 > $fileName

find  /opt/postgres_backup/main/ -name "*.tar.bz2" -type f -mtime +10 -exec rm {} \;
