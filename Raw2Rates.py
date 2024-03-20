# The script does following:
# 1. Check the latest timestamp of raw data that was loaded to  prior.currency_rate_history 
# 2. Selects one by one raw data records from raw.prior_web_content
# 3. Scraps currency data from raw data record
# 4. Loads currency data into  prior.currency_rate_history table if this data are not already there
#
# leotepl@gmail.com

import datetime
import psycopg2
import argparse

from ScrapCurrRatesPrior import scrapCurrRatesPrior 
from LoadDF2DB import loadDF2DB

# parse command line arguments

parser= argparse.ArgumentParser(description='Pull front page from prior.by')
parser.add_argument('env',metavar='1',type=str,nargs='?',help='environment, prod or dev')
args=parser.parse_args()

print(parser.prog+": "+datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")+" started on "+args.env )

# define constants (SQL statements used later)

getLastUpdateTS="""
select max(raw_data_timestamp) from prior.currency_rate_history
"""
getNewRawData="""
select 
 record_id
,content
,insert_timestamp
from raw.prior_web_content
where insert_timestamp > %(last_load_timestamp)s 
"""

try:

# get timestamp of the last raw data record 

    with  psycopg2.connect(dbname="currency_rates_"+args.env\
                           , user="postgres"\
                           , host="127.0.0.1"\
                           , port="5432") as conn:
        with  conn.cursor(getLastUpdateTS) as cur:
            cur.execute(getLastUpdateTS)
            row=cur.fetchone()

            if row[0] is None:          # if the raw data table is empty then use '2000-01-01 00:00:00.0+03:00' timestamp
                ts='2000-01-01 00:00:00.0+03:00'
                print(parser.prog+": Raw data table is empty setting last raw data record timestamp to: ", ts)
            else:
                ts=row[0]
                print(parser.prog+": Last raw data record timestamp: ", ts)

# get raw data records received after selected timestam 

    with  psycopg2.connect(dbname="currency_rates_"+args.env\
                           , user="postgres"\
                           , host="127.0.0.1"\
                           , port="5432") as conn:
        with  conn.cursor() as cur:
            # execute the INSERT statement
            cur.execute(getNewRawData,{'last_load_timestamp':ts})
            for row in cur:             # loop by selected raw records
                
                content=row[1] #.replace('\r\n','\n')
                timestamp=row[2]
                print(parser.prog+": Processing raw record with timestamp: ", timestamp)


                df=scrapCurrRatesPrior(content)      # scrap currency data from raw record into dataframe

                if df.shape[0]>0:
                    loadDF2DB(df,timestamp,args.env)     # load data from dataframe to database
                else:
                    print(parser.prog+": No currency rates data found in the raw record.")
                
except (Exception, psycopg2.DatabaseError) as error:
    print(parser.prog+": Exception:",error)

