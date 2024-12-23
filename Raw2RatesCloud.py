# This script scraps currency rates data from raw page and loads in to Postgres database on the cloud
# It is run as a step on GitHub action.
#
# leotepl@gmail.com
#

import datetime
import glob
import os
import re
from ScrapCurrRatesPrior import scrapCurrRatesPrior 
from LoadDF2DB import loadDF2DB 


# defining constants

timestamp_mask=re.compile('.*prior_page_(\d\d\d\d-\d\d-\d\d)_(\d\d:\d\d:\d\d)\.html')  # regex to extract time stamp from file name

# function to extract timestamp when raw file was created from file name

def file_name_timestamp(f):
    m=timestamp_mask.match(f)
    return (m.group(1)+' '+m.group(2))+'+00:00'  # timestamp on file name is in GMT


with open("html_file_name.txt",'r') as in_file:       
    html_file_name=in_file.read()          # read content form the raw file 

timestamp=file_name_timestamp(html_file_name)    # extract timestamp from raw file name

with open(html_file_name,'r') as in_file:       
    content=in_file.read()          # read content form the raw file 

df=scrapCurrRatesPrior(content)     # get currency rate information into pandas dataframe

if df.shape[0]>0:
    loadDF2DB(df,timestamp,'ep-cold-hall-a260hgk8.eu-central-1.aws.neon.tech','5432','PriorRates','PriorRates_owner')   # load data from dataframe to database
else:
    print(" No currency rates data found in the file.")

